from app import app
import unittest
import random

class FlaskTest(unittest.TestCase):

	# IMPORTANT all test methods must start with test_

	# test if flask app loads
	def test_Index(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type = 'html/text')
		self.assertEqual(response.status_code, 200)



	# test if login page loads
	def test_login_page_loads(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type = 'html/text')
		self.assertTrue(b'Login' in response.data)



	# test that login is required to acsess homepage and aboutpage
	def test_that_login_is_required(self):
		tester = app.test_client(self)
		response = tester.get('/about', content_type = 'html/text', follow_redirects=True)
		self.assertIn(b'You need to login to access',response.data)
		response = tester.get('/', content_type = 'html/text', follow_redirects=True)
		self.assertIn(b'You need to login to access',response.data)


	# test if login is required to logout
	def test_that_login_is_required_to_logout(self):
		tester = app.test_client(self)
		response = tester.get('/logout', content_type = 'html/text', follow_redirects=True)
		self.assertIn(b'You need to login to access',response.data)


	# test if login behaves correctly given correct credentials
	def test_correct_login_with_correct_data(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username='admin', password='admin'), follow_redirects=True)
		self.assertIn(b'You where just logged in', response.data)



	# test if login behaves correctly given wrong credentials
	def test_correct_login_with_wrong_data(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username='wrong', password='wrong'), follow_redirects=True)
		self.assertIn(b'invalid username or password', response.data)



	# test if registration behaves correctly with duplicate username
	def test_registration_with_duplicate_username(self):
		tester = app.test_client(self)
		response = tester.post('/register', data = dict(username='admin', password='something'), follow_redirects=True)
		self.assertIn(b'That username is already taken', response.data)

	# test if registration behaves correctly with unique username
	def test_registration_with_unique_username(self):
		tester = app.test_client(self)
		username = random_string(10)
		response = tester.post('/register', data = dict(username=username, password='fromATest'), follow_redirects=True)
		self.assertIn(b'Registration succeeded', response.data)


	# test if logout works when logged in 
	def test_logout_behaves_when_logged_in(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username='admin', password='admin'), follow_redirects=True)
		response = tester.get('/logout',content_type = 'html/text',follow_redirects=True)
		self.assertIn(b'You are now logged out', response.data)


	# test that logout redirects when not logged in
	def test_logout_behaves_when_logged_out(self):
		tester = app.test_client(self)
		response = tester.get('/logout',content_type = 'html/text',follow_redirects=True)
		self.assertIn(b'You need to login to access', response.data)

	# test that the post shows on the main page
	def test_post_shows_up(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username='admin', password='admin'), follow_redirects=True)
		self.assertIn(b'i am good', response.data)


# Help method
def random_string(length):
		alpha = 'abcdefghijklmnopqrstuwxuz'
		string=""
		for i in range(0,length):
			string+=random.choice(alpha)
		return string


# Run test
if __name__ == '__main__':
	unittest.main()