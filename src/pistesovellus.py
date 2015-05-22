from bottle import route, run, static_file
from os.path import realpath, dirname

script_dir = dirname(realpath(__file__))

@route('/sivut/<filepath>')
def server_static(filepath):
    return static_file(filepath, root=script_dir + '/sivut')

run(host='0.0.0.0', port=8088, debug=True)
