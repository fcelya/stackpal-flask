from app import app
from flask import request, make_response, abort
from app.utils import openai_request_code, openai_request_code_test, log_error

@app.route('/api/optimizer', methods=["POST", "GET"])
def optimizer():
    """
    The request body must have the following information
    language: 'Python', 'JavaScript', etc.
    user: The user id, or 0 if it is a guest
    code: A string containing the code
    """
    if request.method == "POST":
        request_data = request.json
        k = request_data.keys()
        if "language" in k and "user" in k and "code" in k:
            try:
                optimized_response = openai_request_code(code = request_data["code"], language = request_data["language"])
                response = make_response(optimized_response)
            except Exception as e:
                log_error(request,e)
                abort(500)
        else:
            response = make_response(("The request did not contain 'language', 'user' and 'code' in the request body",400))
        
    elif request.method == "GET":
        response = make_response("Aquí puedes optimizar tu código")
    print(response)
    return response

@app.route('/api/optimizer/test', methods=["POST", "GET"])
def optimizer_test():
    """
    This is a test version of the optimizer api, where the answer code is mocked up
    The request body must have the following information
    language: 'Python', 'JavaScript', etc.
    user: The user id, or 0 if it is a guest
    code: A string containing the code
    """
    if request.method == "POST":
        request_data = request.json
        k = request_data.keys()
        if "language" in k and "user" in k and "code" in k:
            optimized_response = openai_request_code_test(code = request_data["code"], language = request_data["language"])
            response = make_response(optimized_response)
        else:
            response = make_response(("The request did not contain 'language', 'user' and 'code' in the request body",400))
        
    elif request.method == "GET":
        response = make_response("Aquí puedes optimizar tu código")
    print(response)
    return response

@app.route("/500error")
def error_test():
    try:
        a = 1/0
    except Exception as e:
        log_error(request,e)
        abort(500)

@app.errorhandler(500)
def internal_error(error):
    return make_response("Internal Server error. Unable to process request",500)