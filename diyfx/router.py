import re
import sys

from webob import exc
from webob import Request

import diyfx

class Router(object):
    def __init__(self):
        self.routes = []

    def add_route(self, template, controller, **vars):
        regex = re.compile(diyfx.template_to_regex(template))
        if isinstance(controller, basestring):
            controller = self._load_controller(controller)
        self.routes.append((regex, controller, vars))

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)

    def _load_controller(self, controller):
        mod_name, func_name = controller.split(':', 1)
        __import__(mod_name)
        mod = sys.modules[mod_name]
        func = getattr(mod, func_name)
        return func
