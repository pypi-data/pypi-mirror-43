# coding: utf8
from __future__ import absolute_import
import inspect
from farbox_lite.utils import smart_str, smart_unicode
from farbox_lite.utils.functional import cached_property


def get_functions_in_a_file_obj(obj):
    obj_filepath = inspect.getmodule(obj).__file__
    functions = []
    sub_functions = inspect.getmembers(obj, inspect.isfunction)
    for sub_function_name, sub_function in sub_functions:
        if sub_function_name.startswith('_') and not sub_function_name.startswith('__') and not sub_function_name=='_': # 以_开头的函数名，不做处理
            # __开头的比较特殊，为了跟系统内置的名称区分开来，比如__int，可能就是一个 int 的调用
            continue
        _real_function = getattr(sub_function, 'original_func', None)  # 可能是被 wrapper 的函数
        real_function = _real_function or sub_function
        if inspect.getmodule(real_function).__file__==obj_filepath:
            functions.append((sub_function_name, sub_function))

            sub_function.arg_spec = inspect.getargspec(real_function)
            sub_function.doc = (inspect.getdoc(real_function) or '').strip()

            if sub_function_name.startswith('__'):
                func_name = sub_function_name
                if func_name != '_':
                    func_name = sub_function_name.lstrip('_')
                functions.append((func_name, sub_function))
    return dict(functions)




class AttrFunc(object):
    # value.int -> to_int(value)
    # value.int(9) -> to_int(value, 9)
    # value.int() -> to_int(value)
    def __init__(self, func):
        self.func = func
        self.is_attr_func = True

    @cached_property
    def default_value(self):
        try:
            return self.func()
        except:
            return smart_unicode(self.func)


    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __repr__(self):
        return smart_unicode(self.default_value)

    def __unicode__(self):
        return smart_unicode(self.default_value)

    def __str__(self):
        return smart_str(self.default_value)

    def __nonzero__(self):
        return bool(self.func)


    def __add__(self, other):
        # 对相加的特殊处理
        if other is None:
            other = ''
        if isinstance(other, (str, unicode)):
            return '%s%s' % (self.default_value, other)
        else:
            return self.default_value + other

    def __mul__(self, other):
        if other is None:
            return ''
        else:
            return self.default_value * other



# 声明了数据类型，这样可以判断meta_class, 多一个 list 对应
metas = {
    'int': int,
    'float': float,
    'str': str,
    'unicode': unicode,
    'tuple': tuple,
    'list': list,
    'dict': dict,
}

def get_lazy_obj(func, first_arg=None, *default_args, **default_kwargs):
    # 这是对函数做了一个非常特殊的处理，可以被当做变量处理，但是同时，也可以作为函数，继续当做函数调用。
    # 推测函数最后的返回类型
    func_name = func.func_name
    meta = metas.get(func_name.rsplit('-')[-1])
    if not meta:
        func_doc = func.func_doc or ''
        if func_doc: # func_doc的第一行声明了数据类型
            meta = metas.get(func_doc.split('\n')[0].strip())
    if not meta:
        meta = object

    class LazyFunc(meta):
        # value.int -> to_int(value)
        # value.int(9) -> to_int(value, 9)
        # value.int() -> to_int(value)
        def __init__(self):
            self.is_lazy_func_obj = True
            self.func = func
            self.first_arg = first_arg
            meta.__init__(self)

        @cached_property
        def default_value(self):
            if not self.func: # 特殊情况，相当于对常量做了包裹
                return self.first_arg
            if default_args and first_arg is None:
                value = func(*default_args, **default_kwargs)
            else:
                if first_arg is None and not default_args and not default_kwargs:
                    # 比如 [1,2,3].json 的调用，json 本身只接受一个参数（which curried already）
                    #if hasattr(func, 'original_func') and hasattr(func.original_func, 'arg_spec') and func.original_func.arg_spec:
                    #    # 比如 posts.group('??') 这种必须要有参数的
                    #    value = ''
                    #elif hasattr(func, 'arg_spec') and func.arg_spec:
                    #    value = ''
                    try:
                        value = func()
                    except: # 很可能是没有参数是不能运行的状态
                        value = ''
                else:
                    value = func(first_arg, *default_args, **default_kwargs)
            return value


        def __call__(self, *args, **kwargs):
            if not self.func: # 函数为空
                return self.default_value

            if not args and not kwargs:
                return self.default_value
            else: # 有参数传入
                if self.first_arg is None:
                    args = list(args)
                else:
                    args = [self.first_arg] + list(args)
                return self.func(*args, **kwargs)

        def __repr__(self):
            return smart_unicode(self.default_value)

        def __unicode__(self):
            return smart_unicode(self.default_value)

        def __str__(self):
            return smart_str(self.default_value)

        def __nonzero__(self):
            return bool(self.default_value)

        def __eq__(self, other):
            return other == self.default_value

        def __add__(self, other):
            # 对相加的特殊处理
            if other is None:
                other = ''
            if isinstance(other, (str, unicode)):
                return '%s%s' % (self.default_value, other)
            else:
                return self.default_value + other

        def __mul__(self, other):
            if other is None:
                return ''
            else:
                return self.default_value * other

    obj = LazyFunc()

    the_func = func
    if hasattr(func, 'original_func'): # curry 过的
        the_func = func.original_func
    if getattr(the_func, 'is_just_property', None):
        # 仅仅是 property, 比如.length, 这样可以保证数据属性的 ok
        return obj.default_value

    return obj


def value_to_lazy_obj(value):
    return get_lazy_obj(func=None, first_arg=value)



