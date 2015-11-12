import os
import re
import webapp2
import jinja2

from lesson2.cipher import Lesson2Rot13
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

class Lesson2Signup(Handler):
	def write_form(self, username_value="", email_value="", username_error="", password_error="", verify_error="", email_error=""):
		self.render("signup.html", username_value=username_value,
									email_value=email_value,
									username_error=username_error,
									password_error=password_error,
									verify_error=verify_error,
									email_error=email_error)
										
	def get(self):
		self.write_form()
	
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
			
		isUsernameValid = self.valid_username(username)
		isPasswordValid = self.valid_password(password)
		passwordsMatch = password == verify
		isEmailValid = self.valid_email(email)
		
		username_error_message = ""
		password_error_message = ""
		verify_error_message = ""
		email_error_message = ""
		
		if not isUsernameValid:
			username_error_message = "That's not a valid username."
		if not isPasswordValid:
			password_error_message = "That wasn't a valid password."
		if not passwordsMatch:
			verify_error_message = "Your passwords didn't match."
		if len(email) > 0 and not isEmailValid:
			email_error_message = "That's not a valid email."
		
		if isUsernameValid and isPasswordValid and passwordsMatch and (len(email) == 0 or isEmailValid):
			self.redirect('/lesson2/signup/thanks?username=' + username)
		else:
			self.write_form(username, 
							email,
							username_error_message, 
							password_error_message, 
							verify_error_message, 
							email_error_message)

	def valid_username(self, username):
   		return re.compile(r"^[a-zA-Z0-9_-]{3,20}$").match(username)
	
	def valid_password(self, password):
	    return re.compile(r"^.{3,20}$").match(password)
	
	def valid_email(self, email):
	    return re.compile(r"^[\S]+@[\S]+\.[\S]+$").match(email)

class Lesson2SignupThanks(Handler):
	def get(self):
		username = self.request.get('username')
		self.render("signup_thanks.html", username=username)

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
			post_id = str(p.key().id())
			self.redirect("/lesson3/blog/%s" % post_id)
		else:
			error = "we need both a subject and content!"
			self.render("newpost.html", error=error)

class BlogPermalinkHandler(Handler):
	def get(self, post_id):
		if post_id and int(post_id):
			p = Post.get_by_id(int(post_id))
			if p:
				self.render("permalink.html", post = p)

app = webapp2.WSGIApplication([('/', MainPage),
							   ('/lesson2/rot13', Lesson2Rot13),
							   ('/lesson2/signup', Lesson2Signup),
							   ('/lesson2/signup/thanks', Lesson2SignupThanks),
							   ('/lesson2/fizzbuzz', FizzBuzzHandler),
							   ('/lesson2/shopping_list', ShoppingListHandler),
							   ('/lesson3/blog', BlogHandler),
							   ('/lesson3/blog/newpost', BlogPostHandler),
							   ('/lesson3/blog/([0-9]+)', BlogPermalinkHandler)], debug=True)