import webapp2
import re
import cgi

form="""
<!DOCTYPE html>
<html>
	<header>
		<title>Lesson 2 User Signup</title>
		<style>
			form  { display: table;      }
			p     { display: table-row;  }
			label { display: table-cell; text-align: right}
			input { display: table-cell; }
			span { display: table-cell; }
		</style>
	</header>
	<body>
		<h1>Signup</h1>
		<form method="post">
			<p>
				<label>Username</label>
				<input name="username" value="%(username_value)s">
				<span style="color: red">%(username_error)s</span>
			</p>
			<p>
				<label>Password</label>
				<input type="password" name="password">
				<span style="color: red">%(password_error)s</span>
			</p>
			<p>
				<label>Verify Password</label>
				<input type="password" name="verify">
				<span style="color: red">%(verify_error)s</span>
			</p>
			<p>
				<label>Email (optional)</label>
				<input name="email" value="%(email_value)s">
				<span style="color: red">%(email_error)s</span>
			</p>
			<input type="submit">
		</form>
	</body>
</html>
"""

welcome_message="""
<h1>Welcome, %(username)s!</h1>
"""

class Lesson2SignupThanks(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write(welcome_message % {"username": username })
			
class Lesson2Signup(webapp2.RequestHandler):
	def write_form(self, username_value="", email_value="", username_error="", password_error="", verify_error="", email_error=""):
		self.response.out.write(form % {"username_value": username_value,
										"email_value": email_value,
										"username_error": username_error,
										"password_error": password_error,
										"verify_error": verify_error,
										"email_error": email_error})
										
	def get(self):
		self.write_form()
	
	def post(self):
		username = escape_html(self.request.get('username'))
		password = escape_html(self.request.get('password'))
		verify = escape_html(self.request.get('verify'))
		email = escape_html(self.request.get('email'))
			
		isUsernameValid = valid_username(username)
		isPasswordValid = valid_password(password)
		passwordsMatch = password == verify
		isEmailValid = valid_email(email)
		
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
			
def escape_html(input):
	return cgi.escape(input, quote=True)
		
def valid_username(username):
    return re.compile(r"^[a-zA-Z0-9_-]{3,20}$").match(username)
	
def valid_password(password):
    return re.compile(r"^.{3,20}$").match(password)
	
def valid_email(email):
    return re.compile(r"^[\S]+@[\S]+\.[\S]+$").match(email)