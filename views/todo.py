from models.todo import Todo, TodoNotFound
from util import BadRequest, NotFound
import json


def todo_to_dict(todo):
    return {'id': todo.id, 'content': todo.content}


class ValidationError(Exception):
    pass


def validate_todo(todo_dict):
    if 'content' not in todo_dict:
        raise ValidationError

    if type(todo_dict['content']) is not str:
        raise ValidationError


def get_all(env, start_response):
    todos = Todo.get_all()
    todos_dict = [todo_to_dict(todo) for todo in todos]
    todos_json = json.dumps(todos_dict, ensure_ascii=False).encode('utf-8')

    start_response('200 OK', [('Content-type', 'application/json; charset=utf-8')])
    return [todos_json]


def post(env, start_response):
    try:
        content_length = int(env.get('CONTENT_LENGTH', 0) or 0)
        todo_dict = json.loads(env['wsgi.input'].read(content_length))
        validate_todo(todo_dict)

        todo_id = Todo(todo_dict['content']).insert()

        start_response('201 Created', [('Location', f'/todo/{todo_id}/')])
        return []
    except (json.JSONDecodeError, ValidationError):
        raise BadRequest


def get(env, start_response, todo_id):
    try:
        todo_dict = todo_to_dict(Todo.get(int(todo_id)))
        todo_json = json.dumps(todo_dict, ensure_ascii=False).encode('utf-8')

        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8')])
        return [todo_json]
    except TodoNotFound:
        raise NotFound


def put(env, start_response, todo_id):
    try:
        content_length = int(env.get('CONTENT_LENGTH', 0) or 0)
        todo_dict = json.loads(env['wsgi.input'].read(content_length))
        validate_todo(todo_dict)

        todo = Todo.get(int(todo_id))
        todo.content = todo_dict['content']
        todo.update()

        start_response('204 No Content', [])
        return []
    except (json.JSONDecodeError, ValidationError):
        raise BadRequest
    except TodoNotFound:
        raise NotFound


def delete(env, start_response, todo_id):
    try:
        Todo.get(int(todo_id)).delete()

        start_response('204 No Content', [])
        return []
    except TodoNotFound:
        raise NotFound
