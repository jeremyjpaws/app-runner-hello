from flask import Flask
import os
import boto3

PORT = 8080
name = os.environ.get('NAME')
if name == None or len(name) == 0:
  name = "world"
MESSAGE = "Hello, " + name + "!"
print("Message: '" + MESSAGE + "'")

app = Flask(__name__)

s3bucket = "cbucket-test-3"
s3key = "FOOBAR.txt"

@app.route("/")
def root():
  print("Handling web request. Returning message.")
  result = MESSAGE.encode("utf-8")
  return result

@app.route("/foobar")
def foobar():
  print("Handling web request for foobar. Returning contents...")
  s3 = boto3.client('s3')
  content = ""
  with open('temps3file', 'a+b') as f:
    s3.download_fileobj(s3bucket, s3key, f)
    data = f.read()
    content = data.decode('utf-8')
    
  print("Content is:" + content)
  result = content.encode("utf-8")
  return result


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=PORT)
