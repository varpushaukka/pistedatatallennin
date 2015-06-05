#coding: utf-8
from bottle import route, run, static_file, redirect, template, view
from os.path import realpath, dirname
from psycopg2 import connect
from pisteconfig import port

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

	#seuraavissa funktioissa "pitää huolen" tarkoittaa sitä,
	# että funktio tarkistaa onko haluttu tieto olemassa ja jos ei, se inserttaa halutun tiedon

	#pitää huolen siitä, että parametrina annettu tagi löytyy tietokannasta, palauttaa id:n
	def id_for_tag(self, tag):
		ids = self.sql("select id from tagi where tagi=%s", (tag,))
		if ids: return ids[0][0]
		ids = self.sql("insert into tagi (tagi) values (%s) returning id", (tag,))
		return ids[0][0]

	#pitää huolen siitä, että parametrina annettu paikka löytyy tietokannasta, palauttaa id:n
	def id_for_place(self, point, epsilon):
		ids = self.sql("select id from paikka where koordinaatti <-> point(%s,%s) <= %s",
			 (point[0], point[1], epsilon))
		if ids: return ids[0][0]
		ids = self.sql("insert into paikka (koordinaatti) values (point(%s,%s)) returning id", 
			 (point[0], point[1]))
		return ids[0][0]

	#tarkistaa lötyykö paikka ja tagi paikkatagi-taulusta ja lisää ne, jos ei löydy
	def bind_place_and_tag(self, placeid, tagid):
		result = self.sql("select 1 from paikkatagi where paikka=%s and tagi=%s", (placeid, tagid))
		if result: return
		self.sql("insert into paikkatagi (paikka, tagi) values (%s,%s) returning 1", (placeid, tagid))

	#tallettaa paikan tietokantaan, jos sitä ei sieltä jo löydy
	def save_into_database(self, place):
		coord, tags = place
		placeid = self.id_for_place(coord, 0)
		for tag in tags:
			self.bind_place_and_tag(placeid, self.id_for_tag(tag))
		self.commit()
	
	#määrittelee paikan tietorakenteen
	def place_for_coord(self, coord):
		tags = self.sql("select tagi.tagi from paikka, tagi, paikkatagi where paikka.id=paikkatagi.paikka and tagi.id=paikkatagi.tagi and koordinaatti <-> point(%s,%s) = 0", (coord[0], coord[1]))
		return (coord, [tag for (tag,) in tags])

	#listaa koordinaatit ja filtteröi ne tagin perusteella
	def list_coordinates(self, startcoord, tag=None):
		if tag: return self.sql("""select koordinaatti[0], koordinaatti[1] 
			from paikka, paikkatagi, tagi
			where paikka.id=paikkatagi.paikka and tagi.id=paikkatagi.tagi and tagi.tagi=%s""", (tag,))
		else: return self.sql("select koordinaatti[0], koordinaatti[1] from paikka")

#Controller
@route('/pages/<filepath>')
def server_static(filepath):
	return static_file(filepath, root=script_dir + '/sivut')

@route('/')
def default_page(): redirect('/pages/index.html')

@route('/list')
def list_all_coordinates():
	return '<br>'.join(str(c) for c in m.list_coordinates((9043,9438)))

@route('/list/<tag>')
@view('list_template')
def search_by_tag(tag):
	return {'tag':tag, 'm':m}

if __name__ == '__main__':
	m = Model("pistedata", port)
	run(host='0.0.0.0', port=8088, debug=True)

