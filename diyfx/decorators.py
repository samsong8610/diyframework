from webob import Request, Response
from webob import exc

def controller(func):
    def _wrapper(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException as e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return _wrapper

def rest_controller(cls):
    def _wrapper(environ, start_response):
        req = Request(environ)
        try:
            controller = cls(req)
            action = req.urlvars.get('action')
            if action:
                action += '_' + req.method.lower()
            else:
                action = req.method.lower()
            try:
                method = getattr(controller, action)
            except AttributeError:
                raise exc.HTTPNotFound('No action %s' % action)
            resp = method(req, **req.urlvars)
        except exc.HTTPException as e:
            resp = e
        if not isinstance(resp, Response):
            resp = Response(body=unicode(resp))
        return resp(environ, start_response)
    return _wrapper
