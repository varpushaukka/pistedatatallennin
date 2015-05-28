#coding: utf-8
from bottle import route, run, static_file, redirect
from os.path import realpath, dirname
from psycopg2 import connect

script_dir = dirname(realpath(__file__))

cur = connect("dbname=pistedata port=5433").cursor()

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

#esimerkkifunktio "all"
def valitsekaikki(taulu):
   kysely = "select * from " + taulu
   return sql(kysely)

#print valitsekaikki("paikka")

#esimerkkifunktio, joka hakee käyttäjätaulusta kaikki id:t ja palauttaa ne listana
def kayttajat():  
   return [id for (id,) in sql("select id from kayttaja;")]

#print kayttajat()

#esimerkkifunktio "find"
def etsi(tunnus, taulu):
   kysely = "select * from " + taulu + " where id =" + tunnus
   return sql(kysely)

#print etsi("1", "kayttaja")

#esimerkkifunktio "save" tagi-taululle HUOM ei toimi vielä, koska sql ottaa vain yhden argumentin TODO
def talletatagi(paikka, tagi):
   data = (paikka, tagi, )
   return sql("insert into tagi (tagi) values (%s,%s);", data)


run(host='0.0.0.0', port=8088, debug=True)

   
