import functools


def with_retry(tries: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = Exception()
            for _ in range(tries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
            raise last_error

        return wrapper

    return decorator
