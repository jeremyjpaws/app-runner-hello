from flask import Flask
import os
import boto3
import logging
import time
import request
import requests

logging.basicConfig(level=logging.INFO)

PORT = 8080
name = os.environ.get('NAME')
s3bucket = os.environ.get('BUCKET')
s3key = os.environ.get('KEY')
target1 = os.environ.get('TARGET1')

if name == None or len(name) == 0:
  name = "world"

if s3bucket == None or len(s3bucket) == 0:
  logging.error("BUCKET env var missing!")

if s3key == None or len(s3key) == 0:
  logging.error("KEY env var missing!")

if target1 == None or len(target1) == 0:
  logging.error("TARGET1 env var missing!")

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

@app.route("/sts")
@app.route("/whoami")
def whoami():
  logging.info("Get request for path /whoami, doing sts test call")
  sts = boto3.client('sts')
  identity = sts.get_caller_identity()
  logging.info(f"My account is {identity['Account']} and my user ARN is {identity['Arn']} and I am {identity['UserId']}.")
  # Note for extra security let's not risk returning the info to the site itself, we'll check our logs later
  return "Go check logs"

@app.route("/foobar")     
@app.route("/s3")
def s3download():
  logging.info(f"Got request for path /foobar. Downloading file {s3key} from S3 bucket {s3bucket} and Returning contents...")
  s3 = boto3.client('s3')
  content = ""
  with open('download.txt', 'a+b') as f:
    logging.info("Starting download...")
    s3.download_fileobj(s3bucket, s3key, f)
    logging.info("Download complete...")
    f.seek(0)
    data = f.read()
    logging.info("Decoding into UTF-8...")
    content = data.decode('utf-8')
    
  logging.info(f"Content is: {content}")
  result = content.encode("utf-8")
  return result

"""
Ping target 1, for example you could set target1 to be an EC2 instance in the same VPC
Uses TARGET1 env var which should be like an IP address or URL to hit
"""
@app.route("/target1")
def pingTarget():
  logging.info(f"About to ping target which is {target1}...")
  r =requests.get(target1)
  logging.info(f"Got response from target, status code: {r.status}")
  return f"Pinged target, got response {r.status}"
    


if __name__ == "__main__":
  logging.info("starting up server...")
  app.run(debug=True, host="0.0.0.0", port=PORT)
