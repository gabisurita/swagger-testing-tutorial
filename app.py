from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config


@view_config(route_name='hello', renderer='json')
def hello_view(request):
    return {'hello': request.matchdict['name']}


def setup():
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = setup()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
