from flask import Flask
import os
import boto3
import logging
import time

logging.basicConfig(level==logging.INFO)

PORT = 8080
name = os.environ.get('NAME')
s3bucket = os.environ.get('BUCKET')
s3key = os.environment.get('KEY')

if name == None or len(name) == 0:
  name = "world"

if s3bucket == None or len(bucket) == 0:
  logging.error("BUCKET env var missing!")

if s3key == None or len(bucket) == 0:
  logging.error("KEY env var missing!")

MESSAGE = "Hello, " + name + "!"

app = Flask(__name__)

@app.route("/")
def root():
  logging.info(f"Got request for root path /. Returning message: {MESSAGE}")
  result = MESSAGE.encode("utf-8")
  return result

@app.route("/bizbaz")
  logging.info("Got request for path /bizbaz, doing nothing and returning simple message")
  return "bizbaz!"

@app.route("/foobar")
def foobar():
  logging.info(f"Got request for path /foobar. Downloading file {s3key} from S3 bucket {s3bucket} and Returning contents...")
  s3 = boto3.client('s3')
  content = ""
  with open('temps3file', 'a+b') as f:
    logging.info("Starting download...")
    s3.download_fileobj(s3bucket, s3key, f)
    logging.info("Download complete...")
    data = f.read()
    logging.info("Decoding into UTF-8...")
    content = data.decode('utf-8')
    
  logging.info(f"Content is: {content}")
  result = content.encode("utf-8")
  return result


if __name__ == "__main__":
  logging.info("starting up server...")
  app.run(debug=True, host="0.0.0.0", port=PORT)
