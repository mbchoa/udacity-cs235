import webapp2
import cgi

import rot13

lesson2_rot13_form="""
<!DOCTYPE html>
<html>
	<header>
		<title>Lesson 2 Rot13</title>
	</header>
	<body>
		<h1>Enter some text to ROT13:</h1>
		<form method="post">
		<textarea rows="8" cols="75" name="text")>%(feedback)s</textarea>
		<br>
		<input type="submit">
		</form>
	</body>
</html>
"""

class Lesson2Rot13(webapp2.RequestHandler):
	def write_form(self, feedback=""):
		self.response.out.write(lesson2_rot13_form % {"feedback" : self.escape_html(feedback)})
		
	def get(self):
		self.write_form()
		
	def post(self):
		inputtext = self.request.get('text')
		ciphtertext = rot13.rot13(inputtext)
		self.write_form(ciphtertext)
		pass
		
	def escape_html(self, input):
		return cgi.escape(input, quote=True)