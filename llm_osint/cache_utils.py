from typing import Callable
import hashlib
import pickle
import re
import os

MAX_CACHE_VAL_LEN = 20

cache_options = {
    "cache": True,
    "cache_dir": "cache"
}

def cache_func(func: Callable) -> Callable:
    def wrap(*args, **kwargs):
        os.makedirs(cache_options["cache_dir"], exist_ok=True)
        args_str = "".join([str(arg) for arg in args if isinstance(arg, (str, int))] + [str(kwargs.get(key)) for key in kwargs if isinstance(kwargs[key], (str, int))])
        cache_val = re.sub("[^\w\d]", "", args_str)
        if len(cache_val) > MAX_CACHE_VAL_LEN:
            cache_val = str(int(hashlib.md5(cache_val.encode("utf-8")).hexdigest(), 16))
        cache_key = func.__name__ + "_" + cache_val
        cache_fn = os.path.join(cache_options["cache_dir"], cache_key)
        if os.path.exists(cache_fn) and cache_options["cache"]:
            with open(cache_fn, "rb") as f:
                return pickle.load(f)
        else:
            result = func(*args, **kwargs)
            with open(cache_fn, "wb") as f:
                pickle.dump(result, f)
            return result

    return wrap
