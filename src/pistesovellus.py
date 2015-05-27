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
   return cur.fetchall()

def users():  #viikon 3 esimerkkifunktio
   return [id for (id,) in sql("select id from kayttaja;")]

# return [tup[0] for tup in sql...]
print users()

run(host='0.0.0.0', port=8088, debug=True)

   
