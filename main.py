import os
import re
import webapp2
import jinja2
import hmac
import random
import string
import hashlib
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

	def set_secure_cookie(self, name, val):
		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

class Signup(Handler):
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
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.email = self.request.get('email')
			
		isUsernameValid = self.valid_username(self.username)
		isPasswordValid = self.valid_password(self.password)
		passwordsMatch = self.password == self.verify
		isEmailValid = self.valid_email(self.email)
		
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
		if len(self.email) > 0 and not isEmailValid:
			email_error_message = "That's not a valid email."
		
		if isUsernameValid and isPasswordValid and passwordsMatch and (len(self.email) == 0 or isEmailValid):
			self.done()
		else:
			self.write_form(self.username, self.email, username_error_message, password_error_message, verify_error_message, email_error_message)

	def done(self, *a, **kw):
		raise NotImplementedError
		
	def valid_username(self, username):
   		return re.compile(r"^[a-zA-Z0-9_-]{3,20}$").match(username)
	
	def valid_password(self, password):
	    return re.compile(r"^.{3,20}$").match(password)
	
	def valid_email(self, email):
	    return re.compile(r"^[\S]+@[\S]+\.[\S]+$").match(email)

class Unit2Signup(Signup):
	def done(self):
		self.redirect('/lesson2/signup/thanks?username=' + self.username)

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

secret = '@0Tt~[^[0ihubIXP\U9yQny0s4NB/nYG6GOm:Wf1)r(>/0g;d6Ru](&^'

def make_secure_val(val):
	return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == make_secure_val(val):
		return val

def make_salt(length = 5):
	return ''.join(random.choice(string.letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
	return db.Key.from_path('users', group)

class User(db.Model):
	name = db.StringProperty(required = True)
	pw_hash = db.StringProperty(required = True)
	email = db.StringProperty()

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid, parent = users_key())

	@classmethod
	def by_name(cls, name):
		return User.all().filter('name =', name).get()
	
	@classmethod
	def register(cls, name, pw, email = None):
		pw_hash = make_pw_hash(name, pw)
		return User(parent = users_key(),
					name = name,
					pw_hash = pw_hash,
					email = email)

class Register(Signup):
	def get(self):
		users = db.GqlQuery("SELECT * from User")
		self.render("signup.html", users = users)
		
	def done(self):
		#make sure user does not exist already
		u = User.by_name(self.username)
		if u:
			msg = 'Username already exists.'
			self.render('signup.html', username_error = msg)
		else:
			u = User.register(self.username, self.password, self.email)
			u.put()

			self.set_secure_cookie('user_id', str(u.key().id()))
			self.redirect('/lesson4/welcome')
			

class Lesson4Welcome(Handler):
	def get(self):
		if self.user:
			self.render('signup_thanks.html', username=self.user.name)
		else:
			self.redirect('/lesson4/signup')
			
class Login(Register):
	def write_form(self, username_value="", username_error="", password_error=""):
		self.render("login.html", username_value=username_value,
									username_error=username_error,
									password_error=password_error)

	def get(self):
		self.write_form()

	def post(self):
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.done()

	def done(self):
		u = User.by_name(self.username)
		if u:
			isValidPassword = valid_pw(self.username, self.password, u.pw_hash)
			if isValidPassword:
				self.set_secure_cookie('user_id', str(u.key().id()))
				self.redirect('/lesson4/welcome')
			else:
				self.write_form(self.username, "", "Incorrect password")
		else:
			self.write_form(self.username, "User does not exist")

class Logout(Handler):
	def get(self):
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % ('user_id', ''))
		self.redirect('/lesson4/signup')
		
app = webapp2.WSGIApplication([('/', MainPage),
							   ('/lesson2/rot13', Lesson2Rot13),
							   ('/lesson2/signup', Unit2Signup),
							   ('/lesson2/signup/thanks', Lesson2SignupThanks),
							   ('/lesson2/fizzbuzz', FizzBuzzHandler),
							   ('/lesson2/shopping_list', ShoppingListHandler),
							   ('/lesson3/blog', BlogHandler),
							   ('/lesson3/blog/newpost', BlogPostHandler),
							   ('/lesson3/blog/([0-9]+)', BlogPermalinkHandler),
							   ('/lesson4/signup', Register),
							   ('/lesson4/welcome', Lesson4Welcome),
							   ('/lesson4/login', Login),
							   ('/lesson4/logout', Logout)], debug=True)