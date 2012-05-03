# coding: utf-8

'''
  Utilitários para filtrar entrada de métodos http
'''
    
def method_not_allowed_view(request, *args, **kwargs):
    return HttpResponseNotAllowed("405 Method Not Allowed")

def http_method(*methods):
    methods = map(lambda m: m.lower(), methods)
    def __method_wrapper(f):
        this_module = __import__(__name__)
        chain = getattr(this_module, f.__name__, method_not_allowed_view)
        base_view_func = lambda request, *args, **kwargs: \
            f(request, *args, **kwargs) if request.method.lower() in methods \
                                        else chain(request, *args, **kwargs)
        setattr(this_module, f.__name__, base_view_func)
        return base_view_func
    return __method_wrapper