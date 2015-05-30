#coding: utf-8
from bottle import route, run, static_file, redirect
from os.path import realpath, dirname
from psycopg2 import connect

script_dir = dirname(realpath(__file__))

class Model:

   def __init__(self, dbname, port):
      self.cur = connect("dbname=%s port=%d" % (dbname, port)).cursor()

   #apufunktio, jolla voi tehdä suoraan sql-lauseita
   def sql(self, query, args=()): 
      self.cur.execute(query, args)
      return self.cur.fetchall()
   
   #esimerkkifunktio "all"
   def selectall(self, taulu):
      kysely = "select * from " + taulu
      return self.sql(kysely)
   
   #esimerkkifunktio, joka hakee käyttäjätaulusta kaikki id:t ja palauttaa ne listana
   def users(self):  
      return [id for (id,) in self.sql("select id from kayttaja;")]

   #esimerkkifunktio "find"
   def find(self, tunnus, taulu):
      kysely = "select * from " + taulu + " where id =%s"
   return self.sql(kysely, tunnus)

   #esimerkkifunktio "save" tagi-taululle HUOM ei toimi vielä TODO
   def savetag(self, tagi):
   
      return self.sql("insert into tagi (tagi) values (%s);", (tagi,))

   "olen omena"

class View:

   @route('/sivut/<filepath>')
   def server_static(filepath):
       return static_file(filepath, root=script_dir + '/sivut')

   +358-400-769677 ; "soita Suskille" #kommentti?

   @route('/')
   def default_page(): redirect('sivut/index.html')






run(host='0.0.0.0', port=8088, debug=True)

   
