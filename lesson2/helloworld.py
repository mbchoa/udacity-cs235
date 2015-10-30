import webapp2
import cgi

form="""
<!DOCTYPE html>
<html>
	<head>
		<title>Udacity CS253 - Lesson 2: Forms and Input</title>
	</head>
	<body>
		<form method="post">
			What is your birthday?
			<br>
			
			<div>
				<label>
					Month
					<br><input type="text" name="month" value="%(month)s">
				</label>
			</div>
			
			<div>
				<label>
					Day
					<br><input type="text" name="day" value="%(day)s">
				</label>
			</div>
			
			<div>
				<label>
					Year
					<br><input type="text" name="year" value="%(year)s">
				</label>
			</div>
			<div style="color: red">%(error)s</div>
			
			<br>
			<br>
			<input type="submit">
		</form>
	</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
	months = ['January',
			  'February',
			  'March',
			  'April',
			  'May',
			  'June',
			  'July',
			  'August',
			  'September',
			  'October',
			  'November',
			  'December']

	month_abbvs = dict((m[:3].lower(), m) for m in months)
	
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error": error, 
										"month": self.escape_html(month), 
										"day": self.escape_html(day), 
										"year": self.escape_html(year)})
	def escape_html(self, input):
		return cgi.escape(input, quote=True)
		
	def get(self):
		self.write_form()
		
	def post(self):
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')
		
		month = self.valid_month(user_month);
		day = self.valid_day(user_day);
		year = self.valid_year(user_year);
		
		if not (month and day and year):
			self.write_form("That doesn't look valid to me, friend.",
							user_month, user_day, user_year)
		else:
			self.redirect("/thanks")
			
	def valid_month(self, month):
		if month:
			abv_month = month[:3].lower()
			return self.month_abbvs.get(abv_month)
			
	def valid_day(self, day):
		if day and day.isdigit():
			int_day = int(day)
			if int_day >= 1 and int_day <= 31:
				return int_day
				
	def valid_year(self, year):
		if year and year.isdigit():
			int_year = int(year)
			if int_year >= 1900 and int_year <= 2020:
				return int_year

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid day!")
	
class InspectHandler(webapp2.RequestHandler):	
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(self.request)
		
app = webapp2.WSGIApplication([('/', MainPage),
							   ('/thanks', ThanksHandler),
							   ('/inspect', InspectHandler)], 
							   debug=True)