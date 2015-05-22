from bottle import route, run

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/proj/pistedatatallennin/src/sivut')

run(host='0.0.0.0', port=8088, debug=True)
