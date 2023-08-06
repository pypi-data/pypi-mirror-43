"""
Helper for webscraping.
Locally caches downloaded pages.
As opposed to requests_cache it should be able to handle multithreading.
The line below enables caching and sets the cached files path:
    >>> set_cache_path('./example-cache')
    >>> first_call_response = open_url('https://www.google.ch/search?q=what+time+is+it')

Subsequent calls for the same URL returns the cached data:
    >>> import time
    >>> time.sleep(60)
    >>> second_call_response = open_url('https://www.google.ch/search?q=what+time+is+it')
    >>> first_call_response == second_call_response
    True

"""
import logging
import os

import itertools
import threading

from datetime import datetime, timedelta
from time import sleep

import requests
import hashlib

from shutil import rmtree

__CACHE_FILE_PATH = None
__EXPIRY_DAYS = None
__MAX_NODE_FILES = 0x100
__REBALANCING_LIMIT = 0x200
__HEADERS_CHROME = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


__rebalancing = threading.Condition()
__requests_session = None
__last_request = None

__all__ = ['open_url', 'set_cache_path', 'empty_cache', 'get_cache_filename', 'invalidate_key', 'is_cached']


def get_requests_session():
    """
    Underlying requests session.

    :return:
    """
    return __requests_session


def get_last_request():
    """
    Last request.

    :return:
    """
    return __last_request


def set_cache_path(cache_file_path, max_node_files=None, rebalancing_limit=None, expiry_days=10):
    """
    Required for enabling caching.

    :param cache_file_path:
    :param max_node_files:
    :param rebalancing_limit:
    :param expiry_days:
    :return:
    """
    global __CACHE_FILE_PATH
    global __MAX_NODE_FILES
    global __REBALANCING_LIMIT
    global __EXPIRY_DAYS

    __EXPIRY_DAYS = expiry_days

    if max_node_files is not None:
        __MAX_NODE_FILES = max_node_files

    if rebalancing_limit is not None:
        __REBALANCING_LIMIT = rebalancing_limit

    cache_file_path_full = os.path.abspath(cache_file_path)
    __CACHE_FILE_PATH = cache_file_path_full
    if not os.path.exists(__CACHE_FILE_PATH):
        os.makedirs(__CACHE_FILE_PATH)

    logging.debug('setting cache path: %s', cache_file_path_full)
    invalidate_expired_entries()


def invalidate_expired_entries(as_of_date=None):
    """
    :param as_of_date: fake current date (for dev only)
    :return:
    """
    index_name = _index_name()
    if not os.path.exists(index_name):
        return

    if as_of_date is None:
        as_of_date = datetime.today()

    expiry_date = as_of_date - timedelta(days=__EXPIRY_DAYS)
    with open(index_name, 'r') as index_file:
        expired_keys = list()
        lines = index_file.readlines()
        for line in lines:
            if len(line.strip()) == 0:
                continue

            yyyymmdd, key_md5, key_commas = line.strip().split(' ')
            key = key_commas[1:-1]
            key_date = datetime.strptime(yyyymmdd, '%Y%m%d')
            if expiry_date > key_date:
                logging.debug('expired entry for key "%s" (%s)', key_md5[:-1], key)
                expired_keys.append(key)

    _remove_from_cache_multiple(expired_keys)


def is_cache_used():
    return __CACHE_FILE_PATH is not None


def _get_directories_under(path):
    return (node for node in os.listdir(path) if os.path.isdir(os.path.join(path, node)))


def _get_files_under(path):
    return (node for node in os.listdir(path)
            if os.path.isfile(os.path.join(path, node)) and node != 'index'
            )


def _generator_count(a_generator):
    return sum(1 for item in a_generator)


def _divide_node(path, nodes_path):
    level = len(nodes_path)
    new_node_sup_init = 'FF' * 20
    new_node_inf_init = '7F' + 'FF' * 19
    if level > 0:
        new_node_sup = nodes_path[-1]
        new_node_diff = (int(new_node_sup_init, 16) - int(new_node_inf_init, 16)) >> level
        new_node_inf = '%0.40X' % (int(new_node_sup, 16) - new_node_diff)

    else:
        new_node_sup = new_node_sup_init
        new_node_inf = new_node_inf_init

    new_path_1 = os.path.sep.join([path] + nodes_path + [new_node_inf.lower()])
    new_path_2 = os.path.sep.join([path] + nodes_path + [new_node_sup.lower()])
    return os.path.abspath(new_path_1), os.path.abspath(new_path_2)


def rebalance_cache_tree(path, nodes_path=None):
    if not nodes_path:
        nodes_path = list()

    current_path = os.path.sep.join([path] + nodes_path)
    files_node = _get_files_under(current_path)
    rebalancing_required = _generator_count(itertools.islice(files_node, __MAX_NODE_FILES + 1)) > __MAX_NODE_FILES
    if rebalancing_required:
        new_path_1, new_path_2 = _divide_node(path, nodes_path)
        logging.info('rebalancing required, creating nodes: %s and %s', os.path.abspath(new_path_1), os.path.abspath(new_path_2))
        with __rebalancing:
            logging.info('lock acquired: rebalancing started')
            if not os.path.exists(new_path_1):
                os.makedirs(new_path_1)

            if not os.path.exists(new_path_2):
                os.makedirs(new_path_2)

            for filename in _get_files_under(current_path):
                file_path = os.path.sep.join([current_path, filename])
                if file_path <= new_path_1:
                    logging.debug('moving %s to %s', filename, new_path_1)
                    os.rename(file_path, os.path.sep.join([new_path_1, filename]))

                else:
                    logging.debug('moving %s to %s', filename, new_path_2)
                    os.rename(file_path, os.path.sep.join([new_path_2, filename]))

        logging.info('lock released: rebalancing completed')

    for directory in _get_directories_under(current_path):
        rebalance_cache_tree(path, nodes_path + [directory])


def find_node(digest, path=None):
    if not path:
        path = __CACHE_FILE_PATH

    directories = sorted(_get_directories_under(path))

    if not directories:
        return path

    else:
        target_directory = None
        for directory_name in directories:
            if digest <= directory_name:
                target_directory = directory_name
                break

        if not target_directory:
            raise Exception('Inconsistent cache tree: expected directory "%s" not found', target_directory)

        return find_node(digest, path=os.path.sep.join([path, target_directory]))


def get_cache_filename(key):
    """

    :param key: text uniquely identifying the associated content (typically a full url)
    :return: hashed version of the input key
    """
    key = str(key)
    hash_md5 = hashlib.md5()
    hash_md5.update(key.encode('utf-8'))
    digest = hash_md5.hexdigest()
    target_node = find_node(digest)
    cache_filename = os.sep.join([target_node, digest])
    return cache_filename


def is_cached(key):
    """
    Checks if specified cache key (typically a full url) corresponds to an entry in the cache.

    :param key:
    :return:
    """
    cache_filename = get_cache_filename(key)
    return os.path.exists(cache_filename)


def file_size(filename):
    count = -1
    with open(filename) as file_lines:
        for count, line in enumerate(file_lines):
            pass

    return count + 1


def _index_name():
    return os.path.sep.join([__CACHE_FILE_PATH, 'index'])


def _add_to_cache(key, value):
    __rebalancing.acquire()
    try:
        logging.debug('adding to cache: %s', key)
        filename = get_cache_filename(key)
        index_name = _index_name()
        today = datetime.today().strftime('%Y%m%d')
        with open(filename, 'w', encoding='utf-8') as cache_content:
            cache_content.write(value)

        if not os.path.exists(index_name):
            with open(index_name, 'w') as index_file:
                filename_digest = filename.split(os.path.sep)[-1]
                index_file.write('%s %s: "%s"\n' % (today, filename_digest, key))

        else:
            with open(index_name, 'a') as index_file:
                filename_digest = filename.split(os.path.sep)[-1]
                index_file.write('%s %s: "%s"\n' % (today, filename_digest, key))

    finally:
        __rebalancing.notify_all()
        __rebalancing.release()

    if file_size(index_name) % __REBALANCING_LIMIT == 0:
        logging.debug('rebalancing cache')
        rebalance_cache_tree(__CACHE_FILE_PATH)


def _get_from_cache(key):
    __rebalancing.acquire()
    try:
        logging.debug('reading from cache: %s', key)
        with open(get_cache_filename(key), 'r', encoding='utf-8') as cache_content:
            content = cache_content.read()

    finally:
        __rebalancing.notify_all()
        __rebalancing.release()

    return content


def _remove_from_cache_multiple(keys):
    __rebalancing.acquire()
    try:
        index_name = _index_name()
        with open(index_name, 'r') as index_file:
            lines = index_file.readlines()
            for key in keys:
                filename = get_cache_filename(key)
                filename_digest = filename.split(os.path.sep)[-1]
                logging.info('removing key %s from cache' % key)
                try:
                    os.remove(filename)

                except FileNotFoundError:
                    logging.warning('corrupted cache index: broken reference to file %s', filename)

                lines = [line for line in lines if line.split(' ')[1] != filename_digest + ':']

        with open(index_name, 'w') as index_file:
            index_file.writelines(lines)

    finally:
        __rebalancing.notify_all()
        __rebalancing.release()


def _remove_from_cache(key):
    _remove_from_cache_multiple([key])


def read_cached(read_func, key):
    """
    :param read_func: function getting the data that will be cached
    :param key: key associated to the cache entry
    :return:
    """
    logging.debug('reading for key: %s', key)
    if is_cache_used():
        if not is_cached(key):
            content = read_func(key)
            _add_to_cache(key, content)

        content = _get_from_cache(key)

    else:
        # straight access
        content = read_func(key)

    return content


def invalidate_key(key):
    if is_cache_used():
        _remove_from_cache(key)


def rebalance_cache():
    if is_cache_used():
        rebalance_cache_tree(__CACHE_FILE_PATH)


def empty_cache():
    """
    Removing cache content.
    :return:
    """
    if is_cache_used():
        for node in os.listdir(__CACHE_FILE_PATH):
            node_path = os.path.sep.join([__CACHE_FILE_PATH, node])
            if os.path.isfile(node_path):
                os.remove(node_path)

            else:
                rmtree(node_path, ignore_errors=True)

        if os.path.exists(_index_name()):
            os.remove(_index_name())


def open_url(url, rejection_marker=None, throttle=None):
    """
    Opens specified url. Caching is used if initialized with set_cache_path().
    :param url: target url
    :param rejection_marker: raises error if response contains specified marker
    :param throttle: waiting period before sending request
    :return: remote response as text
    """
    global __requests_session

    if __requests_session is None:
        __requests_session = requests.Session()

    def inner_open_url(request_url):
        global __last_request
        logging.debug('session cookies: %s', __requests_session.cookies)
        if throttle:
            sleep(throttle)

        response = __requests_session.get(request_url, headers=__HEADERS_CHROME)
        response_text = response.text
        __last_request = response.request
        if rejection_marker is not None and rejection_marker in response_text:
            raise RuntimeError('rejected, failed to load url %s', request_url)

        return response_text

    content = read_cached(inner_open_url, url)
    return content
