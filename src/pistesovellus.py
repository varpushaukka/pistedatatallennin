from bottle import route, run

@route('/sivut/<filepath:path>')
def server_static(filepath):
    f = static_file(filepath, root='/home/varpushaukka/proj/pistedatatallennin/src/sivut')
    print f.status
    return f

run(host='0.0.0.0', port=8088, debug=True)
