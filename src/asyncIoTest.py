import asyncio
import time 


def background(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if callable(f):
            return loop.run_in_executor(None, f, *args, **kwargs)
        else:
            raise TypeError('Task must be a callable')    
    return wrapped

@background
def testDontWait():
    time.sleep(4)
    print(3)

print(1)
testDontWait()
print(2)
time.sleep(5)
