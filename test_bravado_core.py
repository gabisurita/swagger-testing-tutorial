import unittest
from webtest import TestApp
import yaml

from bravado_core.spec import Spec
from bravado_core.resource import build_resources
from bravado_core.request import IncomingRequest, unmarshal_request
from bravado_core.response import OutgoingResponse, validate_response
from bravado_core.swagger20_validator import ValidationError

from app import setup


class TestSwaggerBravadoCore(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(setup())

        self.spec_dict = yaml.load(open('swagger.yaml'))
        self.spec = Spec.from_dict(self.spec_dict)
        self.resources = build_resources(self.spec)

    def create_bravado_request(self):
        """Auxiliary method to create a blank Bravado request."""

        request = IncomingRequest()
        request.path = {}
        request.query = {}
        request._json = {}
        request.json = lambda: request._json

        return request

    def cast_bravado_response(self, response):
        """Auxiliary method to cast webtest response as Bravado response."""

        resp = OutgoingResponse()
        resp.text = response.body
        resp.headers = response.headers
        # Drop charset (it's a bug on Pyramid <= 1.7.3)
        resp.content_type = response.headers.get('Content-Type').split(';')[0]
        resp.json = lambda: response.json

        return resp

    def test_hello_validate_required_fields(self):
        op = self.resources['hello'].get_hello
        request = self.create_bravado_request()

        self.assertRaises(ValidationError, unmarshal_request, request, op)

    def test_hello_validate_name_type(self):
        op = self.resources['hello'].get_hello
        request = self.create_bravado_request()
        request.path = {'name': {}}

        self.assertRaises(ValidationError, unmarshal_request, request, op)

    def test_get_hello_200(self):
        op = self.resources['hello'].get_hello
        request = self.create_bravado_request()
        request.path = {'name': 'Gabi'}
        params = unmarshal_request(request, op)

        response = self.app.get(op.path_name.format(**params))
        response = self.cast_bravado_response(response)

        schema = self.spec.deref(op.op_spec['responses']['200'])

        validate_response(schema, op, response)
        self.assertEquals(response.json()['hello'], 'Gabi')
