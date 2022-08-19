from src.views import index, detail, create_source


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/detail/', detail, name='details')
    app.router.add_post('/source/', create_source, name='create_source')
    app.router.add_post('/currency/', create_source, name='create_currency')
