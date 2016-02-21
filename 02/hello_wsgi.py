from cgi import parse_qs, escape  

def application(environ, start_response):
	d = parse_qs(environ['QUERY_STRING'])
	user = d.get('user', [''])[0]
	start_response('200 OK', [('Content-Type', 'text/html')])
	return '<h1>Hello %s!</h1>' % (user)