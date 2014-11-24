def cors(allow, *args):
    'return flask-response with CORS enabled for allow'
    if len(args) == 1:
        if type(args[0]) == str:
            r = make_response(args[0])
        else:
            r = args[0]
    else:
        r = make_response(*args)
    r.headers['Access-Control-Allow-Origin'] = allow
    return r
