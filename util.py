class HTTPException(Exception):
    pass


class NotFound(HTTPException):
    def __call__(self, env, start_response):
        start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
        return [b'404 Not Found']


class BadRequest(HTTPException):
    def __call__(self, env, start_response):
        start_response('400 Bad Requet', [('Content-type', 'text/plain; charset=utf-8')])
        return [b'400 Bad Request']
