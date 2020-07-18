## importing requests library to send http requests
import requests
class Login:
	## constructor initialized with the URl, login_data and headers
	def __init__(self, url, login_data, headers):
		self.url = 	url
		self.login_data = login_data
		self.headers = headers



	## loginuser sends http GET requests to the login page and then sends a http POST request with the login cedentials
	def loginUser(self):
		with requests.Session() as s:
			response = s.get(self.url, headers = self.headers)
			response = s.post(self.url, data=self.login_data, headers = self.headers)
			print(response.status_code)
			if response.status_code == 200:
				print "Successfull Login"
			else:
				print "Unsuccessfull Login"

if __name__ == "__main__":
	## target url
	url = "https://www.codecademy.com/login?redirect=%2F"
	## headers
	headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
	## form data used
	login_data = {
		'authenticity_token' : 'v4m8cO9uO+BnAJw+yn5TURjoS0/e3LFhBJCUDPLQZ3uppiQCzhsqMEbegE/52kF90Wy+BTSttmppgXfbIAAERw==',
		'redirect' : '/',
		'user[login]' : 'debjit16.dc@gmail.com',
		'user[password]' : 'debjit#31'
	}


	t = Login(url, login_data, headers)


	t.loginUser()
