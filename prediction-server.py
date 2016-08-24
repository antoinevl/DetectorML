from bottle import route, run, template, request
from base64 import b64encode, b64decode
from detector import predict

@route('/prediction')
def f():
	url = request.query.url
	return "URL: "+url+"<br>Prediction:"+predict(url)+"."

run(host='146.169.47.251', port=8080)
