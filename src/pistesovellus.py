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

#apufunktio, jolla voi tehdä suoraan sql-lauseita
def sql(query): 
   cur.execute(query)
   return cur.fetchall()

def valitsekaikki(taulu):
   return sql("select * from table (%s)", (taulu,))"

#viikon 3 esimerkkifunktio, joka hakee käyttäjätaulusta kaikki id:t ja palauttaa ne listana
def kayttajat():  
   return [id for (id,) in sql("select id from kayttaja;")]
   # return [tup[0] for tup in sql...]

print kayttajat()

#viikon 3 toinen esimerkkifunktio

run(host='0.0.0.0', port=8088, debug=True)

   
