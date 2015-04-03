import re
import unittest
from webob import Request
from webob import Response

import diyfx
from diyfx import router

def fake_controller(environ, start_response):
    pass

def fake_app(environ, start_response):
    pass

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = router.Router()

    def test_add_route(self):
        self.router.add_route('/', fake_app)
        self.assertEqual(1, len(self.router.routes))
        route = self.router.routes[0]
        self.assertEqual(re.compile(diyfx.template_to_regex('/')),
                         route[0])
        self.assertEqual(fake_app, route[1])
        self.assertEqual({}, route[2])

    def test_add_route_with_dynamic_load_controller(self):
        self.router.add_route('/', 'tests.test_router:fake_controller')
        self.assertEqual(1, len(self.router.routes))
        route = self.router.routes[0]
        self.assertEqual(fake_controller.__name__,
                         route[1].__name__)

    def test_add_route_with_vars(self):
        vars = {'var_name': 'var_value'}
        self.router.add_route('/', fake_app, **vars)
        self.assertEqual(1, len(self.router.routes))
        route = self.router.routes[0]
        self.assertEqual(vars, route[2])

    def test_call(self):
        def fake_app(environ, start_response):
            resp = Response(body='fake_app')
            return resp(environ, start_response)

        self.router.add_route('/', fake_app)
        req = Request.blank('/')
        resp = req.get_response(self.router)
        self.assertEqual('fake_app', resp.body)
