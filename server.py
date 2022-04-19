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
def bizbaz():
  logging.info("Got request for path /bizbaz, doing nothing and returning simple message")
  return "bizbaz!"

@app.route("/whoami")
def whoami():
  logging.info("Get request for path /whoami, doing sts test call")
  sts = boto3.client('sts')
  identity = sts.get_caller_identity()
  logging.info(f"My account is {identity['Account']} and my user ARN is {identity['User']}"
  # Note for extra security let's not risk returning the info to the site itself, we'll check our logs later
  return "Go check logs".encode("utf-8")

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
