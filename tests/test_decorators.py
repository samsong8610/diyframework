import unittest
from webob import Request, Response
from webob import exc

from diyfx import decorators as dec
from diyfx import router

class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.router = router.Router()

    def test_controller(self):
        self.router.add_route('/', _fake_dec_controller)
        req = Request.blank('/')
        resp = req.get_response(self.router)
        self.assertIsInstance(resp, Response)
        self.assertEqual('fake_controller', resp.body)

    def test_controller_raise_exception(self):
        self.router.add_route('/', _fake_dec_controller_raise_exception)
        req = Request.blank('/')
        resp = req.get_response(self.router)
        self.assertIsInstance(resp, Response)
        self.assertTrue('501 Not Implemented' in resp.body)

    def test_rest_controller(self):
        self.router.add_route('/', FakeRestController)
        req = Request.blank('/')
        resp = req.get_response(self.router)
        self.assertEqual('get', resp.body)
        req.method = 'POST'
        req.body = 'p=post'
        resp = req.get_response(self.router)
        self.assertEqual('post', resp.body)
        self.router.add_route('/{action}', FakeRestController)
        req = Request.blank('/plus')
        req.method = 'POST'
        req.body = 'op1=1&op2=1'
        resp = req.get_response(self.router)
        self.assertEqual('2', resp.body)


@dec.controller
def _fake_dec_controller(req):
    return 'fake_controller'


@dec.controller
def _fake_dec_controller_raise_exception(req):
    raise exc.HTTPNotImplemented()

@dec.rest_controller
class FakeRestController(object):
    def __init__(self, req):
        self.request = req

    def get(self, req):
        return 'get'

    def post(self, req):
        return req.params['p']

    def plus_post(self, req, **kwargs):
        return int(self.request.params['op1']) + int(self.request.params['op2'])
