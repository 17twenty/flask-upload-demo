import datetime
import json
import flask
from werkzeug.exceptions import default_exceptions, HTTPException
from flask import make_response, abort as flask_abort, request


def json_super_serial(obj):
    """
    Override to allow for serialising things that aren't serializable by the
    normal json unmarshalling code.
    Currently supports:
     - datetime.datetime
     - anything implementing to_json
    """
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, datetime.date):
        serial = obj.isoformat()
        return serial

    # Our custom types can expose a to_json method to do stuff with
    json_func = getattr(obj, "to_json", None)
    if callable(json_func):
        return json_func()

    raise TypeError(
        "Type '" + str(type(obj)) + "' not serializable - consider adding a 'to_json' method to your object")


def jsonify(obj):
    return json.dumps(obj, default=json_super_serial)


def json_response_data(
        result=None, message=None, status_code=200, error_code=None
):
    """Generate our 'standard' JSON response.

    Usually you'd want to use json_response below, which generates
    a Flask response object. But I think George wanted this for
    testing or something.
    """
    # An exception without an error code
    if not status_code:
        status_code = 500

    # All 2xx status codes are success.
    success = (status_code / 100 == 2)
    assert not (success and error_code), "Successful errors aren't allowed"

    response = {'status': 'success' if success else 'error'}

    if message:
        response['message'] = message

    if result is not None:
        response['result'] = result

    if not success:
        response['error_code'] = str(error_code)

    return jsonify(response)


def json_response(
        result=None, message=None, status_code=200, error_code=None
):
    """Generate our 'standard' JSON response.

    Which is a little crazy, because it complies with both the old
    status:success and status:error stuff as well as the new
    "let's return sensible HTTP codes" plan.

    Note that any 2xx status is success, so we don't expect
    an error code (and will throw an AssertionError if you give us one!).
    And if the status_code is not 2xx, you should provide an error code,
    since str(None) looks ugly.

    :param message: Message to be passed along (English, human)
    :param status_code: HTTP status code to return
    :param result: Output to the user, usually a thrift object.
    :param error_code: Stringifiable enum-style code (probably an enum?)
    """
    if not status_code:
        status_code = 500

    return flask.current_app.response_class(
        response=json_response_data(
            result, message, status_code, error_code
        ),
        mimetype='application/json',
        status=status_code
    )


def json_abort(status_code, body=None, headers={}):
    """
    Content negiate the error response.

    """

    if 'text/html' in request.headers.get("Accept", ""):
        error_cls = HTTPException
    else:
        error_cls = JSONHTTPException

    class_name = error_cls.__name__
    bases = [error_cls]
    attributes = {'code': status_code}

    if status_code in default_exceptions:
        # Mixin the Werkzeug exception
        bases.insert(0, default_exceptions[status_code])

    error_cls = type(class_name, tuple(bases), attributes)
    flask_abort(make_response(error_cls(body), status_code, headers))
