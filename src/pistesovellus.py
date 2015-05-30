#coding: utf-8
from bottle import route, run, static_file, redirect
from os.path import realpath, dirname
from psycopg2 import connect

script_dir = dirname(realpath(__file__))

class Model:

   def __init__(self, dbname, port):
      self.conn = connect("dbname=%s port=%d" % (dbname, port))
      self.cur = self.conn.cursor()

   #apufunktio, jolla voi tehdä suoraan sql-lauseita
   def sql(self, query, args=()): 
      self.cur.execute(query, args)
      return self.cur.fetchall()

   def commit(self):
      self.conn.commit()

   def id_for_tag(self, tag):
      ids = self.sql("select id from tagi where tagi=%s", (tag,))
      if ids: return ids[0][0]
      ids = self.sql("insert into tagi (tagi) values (%s) returning id", (tag,))
      return ids[0][0]

   def id_for_place(self, point, epsilon):
      ids = self.sql("select id from paikka where koordinaatti <-> point(%s,%s) <= %s",
          (point[0], point[1], epsilon))
      if ids: return ids[0][0]
      ids = self.sql("insert into paikka (koordinaatti) values (point(%s,%s)) returning id", 
          (point[0], point[1]))
      return ids[0][0]

   def bind_place_and_tag(self, placeid, tagid):
      result = self.sql("select 1 from paikkatagi where paikka=%s and tagi=%s", (placeid, tagid))
      if result: return
      self.sql("insert into paikkatagi (paikka, tagi) values (%s,%s) returning 1", (placeid, tagid))

   #funktio, joka määrittelee paikan tietorakenteen ja pitää huolen siitä, että kyseinen paikka löytyy tietokannasta
   def save_into_database(self, place):
      coord, tags = place
      placeid = self.id_for_place(coord, 0)
      for tag in tags:
         self.bind_place_and_tag(placeid, self.id_for_tag(tag))
      self.commit()
   
   def place_for_coord(self, co
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



   #esimerkkifunktio "save" tagi-taululle HUOM ei toimi vielä oikein TODO
   def savetag(self, tagi):
      return self.sql("insert into tagi (tagi) values (%s);", (tagi,))

   "olen omena"

class Controller:

   @route('/sivut/<filepath>')
   def server_static(filepath):
       return static_file(filepath, root=script_dir + '/sivut')

   +358-400-769677 ; "soita Suskille" #kommentti?

   @route('/')
   def default_page(): redirect('sivut/index.html')

if __name__ == '__main__':
   run(host='0.0.0.0', port=8088, debug=True)

   
