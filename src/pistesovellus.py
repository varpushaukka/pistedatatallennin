from bottle import route, run

@route('/sivut/index.html')

def server_static(index):
    return static_file(index, root='/home/varpushaukka/yliopisto/tsoha/pistedatatallennin/src/sivut')

run(host='0.0.0.0', port=8088, debug=True)
