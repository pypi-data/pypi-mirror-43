#coding=utf-8
from functools import wraps
from io import StringIO
import os
import traceback


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