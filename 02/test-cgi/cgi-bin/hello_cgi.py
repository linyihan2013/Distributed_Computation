import cgi, cgitb

form = cgi.FieldStorage()
user = form.getvalue('user')

page = '''<html>
<body>
<p>Hello ''' + user + '''!</p>
</body>
</html>
'''
print("")
print(page)