from bottle import route, run, static_file

@route('/sivut/<filepath>')
def server_static(filepath):
    f = static_file(filepath, root='/home/varpushaukka/proj/pistedatatallennin/src/sivut')
    return f

run(host='0.0.0.0', port=8088, debug=True)
