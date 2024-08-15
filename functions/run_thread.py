import threading

def run_in_thread(function):
    """
    Decorator to run a function in a separate thread.

    This decorator allows a function to be executed asynchronously in a new thread. The decorated
    function will run concurrently with other threads in the application.

    Parameters:
        function (callable): The function to be run in a separate thread.

    Returns:
        callable: A wrapper function that starts the decorated function in a new thread.
    """
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return wrapper
