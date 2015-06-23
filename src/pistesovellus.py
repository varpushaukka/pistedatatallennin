#coding: utf-8
from bottle import route, run, static_file, redirect, template, view, post, request, app as webapp
from os.path import realpath, dirname
import psycopg2
from pisteconfig import port
from beaker.middleware import SessionMiddleware

script_dir = dirname(realpath(__file__))

class Model:

	def __init__(self, dbname, port):
		self.conn = psycopg2.connect("dbname=%s port=%d" % (dbname, port))
		self.cur = self.conn.cursor()
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, self.cur)

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
		print "insert into tagi (tagi) values(" + tag + ") returning id"
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

	#tarkistaa löytyykö kyseinen tunnus-salasana-yhdistelmä tietokannasta
	def check_login(self, username, password):
		usrnames = self.sql("""select tunnus from kayttaja;""")
		if (username,) in usrnames: 
			pw = self.sql("""select salasana from kayttaja 
			where kayttaja.tunnus=%s""", (username,))
		else: return False
		if (password,) in pw: return True
		return False

#Controller

def require_auth(handler):
	def new_handler(*args):
		s = request.environ.get('beaker.session')
		if 'loggedin' in s:
			return handler(*args)
		else:
			redirect('/pages/kirjaudu.html')
	return new_handler

@route('/pages/<filepath>')
def server_static(filepath):
	return static_file(filepath, root=script_dir + '/sivut')

@route('/')
@view('templates/index_template')
def default_page():
	s = request.environ.get('beaker.session')
	return {'session':s}

app = SessionMiddleware(webapp(), {
	'session.type': 'file',
	'session.cookie_expires': 300,
	'session.data_dir': './data',
	'session.auto': True
})

@route('/test')
def test():
	s = request.environ.get('beaker.session')
	if 'loggedin' in s:
		return 'kirjautuneena: %s' % s['loggedin']
	else: return 'ei sisäänkirjautunutta'

@route('/login', method='POST')
def do_login():
	s = request.environ.get('beaker.session')
	username = request.forms.username
	password = request.forms.password
	if m.check_login(username, password):
		s['loggedin'] = username
		s.save()
		redirect('/')
	else:
		if 'loggedin' in s: del s['loggedin']
		return "<p>Kirjautuminen epäonnistui.</p>"

@route('/logout')
def logout():
	s = request.environ.get('beaker.session')
	del s['loggedin']	
	redirect('/')

@route('/list')
def list_all_coordinates():
	return '<br>'.join(str(c) for c in m.list_coordinates((9043,9438)))

@route('/search', method='POST')
def list_coords():
	haku = request.forms.haku
	print haku, type(haku)
	return '<br>'.join(str(c) for c in m.list_coordinates((9043,9438)))

@route('/place')
@require_auth
def placething():
	return static_file('paikka.html', root=script_dir + '/sivut')


@route('/addplace', method='POST')
def addplace():
	pieces = request.forms.piste.split(",")
	point = tuple(float(n) for n in pieces)
	tag = request.forms.tagi
	place = (point, [tag])
	m.save_into_database(place)
	return '<br>' + str(m.place_for_coord(point))

@route('/list/<tag>')
@view('templates/list_template')
def search_by_tag(tag):
	return {'tag':tag, 'm':m}

if __name__ == '__main__':
	m = Model("pistedata", port)
	run(host='0.0.0.0', port=8088, debug=True, app=app)

