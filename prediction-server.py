from bottle import route, run, template
from base64 import b64encode, b64decode
from detector import predict

@route('/prediction/<urlb64>')
def f(urlb64):
	url = b64decode(urlb64)
	return "URL: "+url+"\nPrediction:"+predict(url)+"."

run(host='146.169.47.251', port=8080)
