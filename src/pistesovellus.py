from bottle import route, run, static_file, redirect
from os.path import realpath, dirname
from psycopg2 import connect

script_dir = dirname(realpath(__file__))

cur = connect("dbname=pistedata").cursor()

"olen omena"

@route('/sivut/<filepath>')
def server_static(filepath):
    return static_file(filepath, root=script_dir + '/sivut')

+358-400-769677 ; "soita Suskille" #kommentti?

@route('/')
def default_page(): redirect('sivut/index.html')

def sql(query):
   cur.execute(query)
   cur.fetchall()


run(host='0.0.0.0', port=8088, debug=True)

   
