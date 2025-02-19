#!/usr/bin/python3

import cgi
import cgitb
import os
import subprocess
import jinja2
import requests

cgitb.enable()

print("Content-type:text/html\n\n")

html = """
<html>
  <head>
    <title>GOR Training</title>
  </head>

  <body>
  <h1>GOR Training</h1>
  <h2>Create a GOR model file from a training dataset</h2>
  <form action="./GOR_training.py" method="post" enctype="multipart/form-data"> 

  <p> Please provide a training dataset otherwise a default dataset will be used: </p>

   <label for="TrainingFile">Training File:</label>
   <input type="file" id="TrainingFile" name="trainingFile" />

   <br> <br>

   <label for="gorVersion">Choose a GOR version:</label>
   <select name="gorVersion" id="gorVersionID">
      <option value="gor1">GOR 1</option>
      <option value="gor3">GOR 3</option>
      <option value="gor4">GOR 4</option>
   </select>

   <br> <br>
    <p>Click to submit your input:</p>
   <input type="submit" name="submit"/>


  </form>
  <br> <hr> <br>

  {% if text %}
  <blockquote>
        {{text}} <br>
  </blockquote>
  {% endif %}
  </body>
  </html>

  
  </body>
  </html>

"""


cgitb.enable()

"""
{% if text %}
  <blockquote>
        {{text}} <br>
  </blockquote>
  {% endif %}

  {% if model_output_path %}
  <a href="{{ model_output_path }}" download="trained_Model.txt">
    <button>Download Model</button>
  </a>
  {% endif %}
"""

# Setup Jinja2 template environment
template_loader = jinja2.FileSystemLoader(searchpath="/path/to/your/templates")
template_env = jinja2.Environment(loader=template_loader)

# Process form data
form = cgi.FieldStorage()

UPLOAD_DIR = 'tmp'
java_output = None  # set inside if bodies
training_path = None


trainingFile = form.getvalue("trainingFile")
gorVersion = form.getvalue("gorVersion")

model_output_path = "/home/r/rolf/public_html/trained_Model.txt"

# check which model format provided:
if trainingFile is not None:
    training_file = form['trainingFile']
    training_path = os.path.join("/home/r/rolf/public_html/", training_file.filename)
    with open(training_path, 'wb') as f:
        while True:
            chunk = training_file.file.read(10000)
            if not chunk:
                break
            f.write(chunk)

if gorVersion is not None:
    if gorVersion == "gor1":
        gorX = "gor1"
    if gorVersion == "gor3":
        gorX = "gor3"
    if gorVersion == "gor4":
        gorX = "gor4"

if training_path is not None and gorVersion is not None:
    java_command = ['java', '-jar', 'train.jar',
                    '--db', training_path, '--model', model_output_path, '--method', gorX]
    java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')

print(jinja2.Environment().from_string(html).render(text=java_output))
#print(jinja2.Environment().from_string(html).render(text=java_output, model_output_path=model_output_path))

