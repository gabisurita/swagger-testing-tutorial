import unittest

from bravado.client import SwaggerClient, SwaggerMappingError
from bravado.swagger_model import load_file
from jsonschema.exceptions import ValidationError


class TestSwaggerBravado(unittest.TestCase):

    def setUp(self):
        self.client = SwaggerClient.from_spec(load_file('swagger.yaml'))

    def test_hello_validate_required_fields(self):
        get_hello = self.client.hello.get_hello
        self.assertRaises(SwaggerMappingError, get_hello)

    def test_hello_validate_name_type(self):
        get_hello = self.client.hello.get_hello
        self.assertRaises(ValidationError, get_hello, name={})

    def test_get_hello_200(self):
        get_hello = self.client.hello.get_hello
        response = get_hello(name='Gabi').result()
        self.assertEquals(response.hello, 'Gabi')
