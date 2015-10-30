import webapp2

from lesson2.cipher import Lesson2Rot13
from lesson2.signup import Lesson2Signup
from lesson2.signup import Lesson2SignupThanks

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.redirect('/lesson2/signup')
		
app = webapp2.WSGIApplication([('/', MainPage),
							   ('/lesson2/rot13', Lesson2Rot13),
							   ('/lesson2/signup', Lesson2Signup),
							   ('/lesson2/signup/thanks', Lesson2SignupThanks)], debug=True)