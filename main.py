import os

import webapp2
import jinja2

from lesson2.cipher import Lesson2Rot13
from lesson2.signup import Lesson2Signup, Lesson2SignupThanks

template_dir = os.path.join(os.path.dirname(__file__), 'lesson2\\templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)

class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)

app = webapp2.WSGIApplication([('/', MainPage),
							   ('/lesson2/rot13', Lesson2Rot13),
							   ('/lesson2/signup', Lesson2Signup),
							   ('/lesson2/signup/thanks', Lesson2SignupThanks),
							   ('/lesson2/templates/fizzbuzz', FizzBuzzHandler)], debug=True)