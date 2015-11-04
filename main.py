import os

import webapp2
import jinja2

from lesson2.cipher import Lesson2Rot13
from lesson2.signup import Lesson2Signup, Lesson2SignupThanks
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
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
		self.render("front.html")
		
class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 5)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)

class ShoppingListHandler(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class BlogHandler(Handler):
	def get(self):
		posts = db.GqlQuery("SELECT * from Post ORDER by created DESC ")
		self.render("blog.html", posts = posts)

class BlogPostHandler(Handler):
	def get(self):
		
		self.render("newpost.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			p = Post(subject = subject, content = content)
			p.put()


			self.redirect("/lesson3/blog/")
		else:
			error = "we need both a subject and content!"
			self.render("newpost.html", error=error)

app = webapp2.WSGIApplication([('/', MainPage),
							   ('/lesson2/rot13', Lesson2Rot13),
							   ('/lesson2/signup', Lesson2Signup),
							   ('/lesson2/signup/thanks', Lesson2SignupThanks),
							   ('/lesson2/fizzbuzz', FizzBuzzHandler),
							   ('/lesson2/shopping_list', ShoppingListHandler),
							   ('/lesson3/blog', BlogHandler),
							   ('/lesson3/blog/newpost', BlogPostHandler)], debug=True)