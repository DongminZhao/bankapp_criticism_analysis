import zlib
from bs4 import BeautifulSoup
from urllib import request
import json


def praseHtml(url):
    req = request.urlopen(url)
    return BeautifulSoup(req.read().decode('UTF-8'), "html.parser")


def praseJson(url, timeout= 10):
    # req = request.urlopen(url, timeout=timeout)
    # data = req.read().decode()
    # return json.loads(data)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=url, headers=headers)
    data = request.urlopen(req).read().decode('UTF-8')
    return json.loads(data)


def praseGzipJson(url):
    req = request.urlopen(url)

    result = zlib.decompress(req.read(), 16 + zlib.MAX_WBITS).decode()
    return json.loads(result)

