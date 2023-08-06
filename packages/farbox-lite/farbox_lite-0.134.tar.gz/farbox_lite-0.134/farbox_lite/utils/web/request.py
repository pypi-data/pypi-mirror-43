#coding: utf8
# 没有放在website.utils中，是因为这两个函数，在backend中会被用到
import base64
from flask import request, escape, g
import re, urlparse
import user_agents
from farbox_lite.utils import smart_unicode





def cache_in_request(func):
    # 缓存到 g 这个空间中，但是要注意变量名的前缀，不要冲突
    def _func(*args, **kwargs):
        attr_name = func.__name__
        if attr_name.startswith('get_'):
            attr_name = attr_name.replace('get_', '', 1)
        if not hasattr(g, attr_name):
            attr_value = func()
            setattr(g, attr_name, attr_value)
        return getattr(g, attr_name, None)
    return _func




def has_file_in_request():
    """request中是否有文件内容"""
    if request.files or 'raw_content' in request.form or 'base64' in request.form:
        return True
    elif 'file' in request.form:
        return True
    else:
        return False


def get_content_in_file():
    """提取request的文件内容，常和has_file_in_request配合使用"""
    if hasattr(g, 'cached_file_content'): # 已经处理过了，不重复处理
        return g.cached_file_content
    if 'file' in request.form:
        # txt会被requests发送的时候，当做POST内的数据处理
        # 也包括中文名的PDF文件.. 因为是一起发送出来的，主要是客户端的上传、同步逻辑的对应
        file_content = request.form['file']
    elif 'file' in request.files:
        file_content = request.files['file'].read()
    elif request.files: # 只取一个文件
        file_content = request.files[request.files.keys()[0]].read()
    elif 'raw_content' in request.form:
        file_content = request.form.get('raw_content')
    elif 'base64' in request.form:
        content = request.form.get('base64')
        if ',' in content[:50]:
            head, content = content.split(',', 1)
        try:
            file_content = base64.b64decode(content)
        except:
            file_content = ''
    else:
        file_content = ''
    g.cached_file_content = file_content
    return file_content


def has_args(args):
    for arg in args:
        if not request.args.get(arg):
            return False
    return True

def get_args(args, lower=False):
    values = []
    for arg in args:
        value = request.args.get(arg, '')
        if lower:
            value = value.lower()
        values.append(value)
    return values


def get_language(environ=None):
    # todo 可以在 cookie 中尝试也读取, lang
    try:
        if request.args.get('lang'): # 可以通过GET的防止强制指定
            lang = request.args.get('lang')
            return lang.replace('-', '_')
        environ = environ or request.environ
    except RuntimeError:
        return ''
    raw_lang = environ.get('HTTP_ACCEPT_LANGUAGE', '')
    if not raw_lang:
        return ''
    lang_c = re.search(r'[a-z]{2}-[a-z]{2}', raw_lang , re.I)
    if lang_c:
        lang = lang_c.group().lower()
    else:
        lang = ''
    return lang.replace('-', '_')



def get_referrer_host(referrer=None):
    try:
        referrer = referrer or request.referrer
    except RuntimeError:
        return ''
    if referrer:
        try:
            host = urlparse.urlparse(referrer).netloc
            return host.lower()
        except:
            return ''
    else:
        return ''


def get_user_agent():
    if hasattr(g, 'user_agent'):
        return g.user_agent
    u = user_agents.parse(request.environ.get('HTTP_USER_AGENT', ''))
    g.user_agent = u
    return u


def safe_get(key): # from request.form
    value = request.form.get(key)
    if value:
        value = smart_unicode(escape(value))
    else:
        value = ''
    if key == 'site':
        if value and '://' not in value:
            value = 'http://' + value
    return value


def set_g_default(key, default):
    if not hasattr(g, 'g_defaults'):
        g.g_defaults = {}
    return g.g_defaults.setdefault(key, default)



def get_visitor_ip():
    # 得到访客的 ip
    if request.remote_addr: # 比如 nginx 过来的，proxy-pass & 走 unix socket 的缘故，remote_addr 会是空的, 而是打到 X-Forwarded-For 上
        return request.remote_addr
    else:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR') or ''
        if ip:
            return ip
        elif request.access_route:
            return request.access_route[-1].strip()
        else:
            return ''


def is_normal_request():
    user_agent = request.headers.get('User-Agent', '')
    if not user_agent:
        return False
    if re.search(r'(python|rails|urllib|ezooms|fetcher|monitor|spider|feed|bot|http|@)', user_agent, re.I) or \
        'MSIE 6.0' in user_agent or re.search(r'referr?er\.', request.host, re.I):
        # 类似爬虫之类的
        return False
    elif  len(user_agent) < 20:
        return False
    # at last
    return True
