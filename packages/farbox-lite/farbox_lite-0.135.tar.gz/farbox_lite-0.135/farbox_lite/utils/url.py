#coding: utf8
import json, urllib
from farbox_lite.utils import smart_str, smart_unicode
from urlparse import urlparse, parse_qs

def get_base_url(url):
    url = url.strip()
    u = urlparse(url)
    return '%s://%s/' % (u.scheme, u.netloc)

def get_url_path(url): # like /xxx
    u = urlparse(url)
    return u.path


def get_host_from_url(url):
    if not url:
        return
    url = url.strip()
    u = urlparse(url)
    result = u.netloc
    if result:
        result = result.lower().strip()
    return result


def is_same_url(url1, url2, check_GET=False):
    if not isinstance(url1, (str, unicode)):
        return False
    if not isinstance(url2, (str, unicode)):
        return False
    if url1.startswith('https://'):
        url1 = url1.replace('https://', 'http://', 1)
    if url2.startswith('https://'):
        url2 = url1.replace('https://', 'http://', 1)
    url1 = smart_unicode(url1)
    url2 = smart_unicode(url2)
    if check_GET:
        return url1==url2
    else: # 构建两个url去除GET参数后的
        url1 = url1.split('?')[0].rstrip('/').rstrip()
        url2 = url2.split('?')[0].rstrip('/').rstrip()
        return url1==url2



def get_get_var(url, key):
    u = urlparse(url)
    query = u.query
    if not query:
        return
    else:
        qs = parse_qs(query)
        value = qs.get(key)
        if isinstance(value, (list, tuple)) and len(value)==1:
            return value[0]
        else:
            return value

def get_GET_dict_data(query_string):
    qs = parse_qs(query_string)
    dict_data = {}
    for k, v in qs.items():
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        dict_data[k] = v
    return dict_data



def join_url(url, **params):
    if not params:
        return url
    for key in params:
        value = params[key]
        if isinstance(value, dict):
            params[key] = json.dumps(value)
        elif isinstance(value, unicode):
            params[key] = value.encode('utf8')
        elif value is True:
            params[key] = 'true'
        else:
            params[key] = smart_str(value)

    url_parts = url.split('?', 1)
    if len(url_parts) == 2:
        # 合并原来的 GET 参数
        url, url_q = url_parts
        GET_dict_data = get_GET_dict_data(url_q)
        for k, v in GET_dict_data.items():
            if k not in params:
                params[k] = v

    p_strings = urllib.urlencode(params)

    url += '?'+p_strings
    return url


def encode_url_arg(arg):
    if '%' in arg: # 认为已经encode过了的
        return arg
    try:
        return urllib.quote(arg)
    except:
        return arg

def decode_url_arg(arg):
    try:
        return urllib.unquote(arg)
    except:
        return arg