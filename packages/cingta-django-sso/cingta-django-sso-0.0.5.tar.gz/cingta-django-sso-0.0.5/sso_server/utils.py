#coding=utf-8
from functools import wraps
import hashlib
from io import StringIO
import os
import traceback
from urllib.parse import urlparse


#捕获最后的异常
def cap_exception(return_func=None):
    def out_wraps(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                fp = StringIO()
                traceback.print_exc(file=fp)
                msg = fp.getvalue()
                with open("sso_error.log", "a+", encoding="utf-8") as f:
                    f.write(msg)
                    f.write(os.linesep)
                return return_func if not return_func else return_func()

        return wrapper

    return out_wraps

#判断是ip还是域名
def gain_domain(addr):
    result = urlparse(addr)
    netloc = result.netloc
    if netloc.replace(".", "").isdigit():
        return netloc
    else:
        dot_index = netloc.find(".")
        return netloc[dot_index:]
    
def getdefault():
    try:
        rs = "12345"
    except:
        rs = ""
    return hashlib.md5(rs.encode(encoding='utf_8', errors='strict')).hexdigest()
        