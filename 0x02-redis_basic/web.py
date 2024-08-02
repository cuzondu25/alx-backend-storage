#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """ Decorator counting how number of times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cache_key = "cache:" + url
        cache_data = store.get(cache_key)
        if cache_data:
            return cache_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cache_key, html)
        store.expire(cache_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text
