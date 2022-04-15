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
  with open('temps3file', 'wb') as f:
    s3.download_fileobj(s3bucket, s3key, f)
    line = f.read(10)
    print ("Read Line: %s" % (line))
    result = line.encode("utf-8")
    return result


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=PORT)
