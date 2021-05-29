from wsgiref.simple_server import make_server
from views import todo
from util import HTTPException, NotFound
import re


ROUTES = [
    (r'/todo/$', 'GET', todo.get_all),
    (r'/todo/$', 'POST', todo.post),
    (r'/todo/(?P<todo_id>\d+)/$', 'GET', todo.get),
    (r'/todo/(?P<todo_id>\d+)/$', 'DELETE', todo.delete),
    (r'/todo/(?P<todo_id>\d+)/$', 'PUT', todo.put),
]


def route(method, path):
    for r in ROUTES:
        m = re.compile(r[0]).match(path)
        if m and r[1] == method:
            url_vars = m.groupdict()
            return r[2], url_vars
    raise NotFound


def app(env, start_response):
    method = env['REQUEST_METHOD'].upper()
    path = env['PATH_INFO'] or '/'
    try:
        callback, kwargs = route(method, path)
        return callback(env, start_response, **kwargs)
    except HTTPException as e:
        return e(env, start_response)


if __name__ == '__main__':
    httpd = make_server('', 5000, app)
    httpd.serve_forever()
