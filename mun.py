from bottle import route, run

@route('/hello')
def hello():
   return "Hello World"

#run(host='0.0.0.0', port=8088, debug=True)
