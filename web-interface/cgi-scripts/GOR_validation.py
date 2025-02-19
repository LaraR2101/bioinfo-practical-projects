#!/usr/bin/python3

#copied from GOR_predict

# perform cross validation of GOR I – V on a user-defined dataset
# compare your own tool to state-of-the-art prediction tools, e.g. PSIPRED
# present alignment and secondary structure prediction benchmark results that feature these reference methods
# develop and describe an approach for test set creation (sequence similarity etc.)

import cgi
import cgitb
import os
import subprocess
import jinja2

cgitb.enable()

print("Content-type:text/html\n\n")

html = """
<html>
  <head>
    <title>GOR validation</title>
  </head>

  <body>
  <h1>GOR prediction</h1>
  <h2>Validation of the GOR secondary structure prediction</h2>
  <form action="./GOR_prediction.py" method="post" enctype="multipart/form-data"> 

  <p> Please provide a dataset for 5-fold Cross Validation: </p>
   <input type="file" name="crossValFile" />

  <button type="submit">Submit</button>
  </form>
  <br> <br>

  {% if text %}
  <blockquote>
        {{text}} <br>
  </blockquote>
  {% endif %}
  </body>
  </html>

"""
cgitb.enable()

# Setup Jinja2 template environment
template_loader = jinja2.FileSystemLoader(searchpath="/path/to/your/templates")
template_env = jinja2.Environment(loader=template_loader)

# Process form data
form = cgi.FieldStorage()

#UPLOAD_DIR = 'tmp'
java_output = None

if 'crossValFile' in form:
    # Get uploaded files
    crossVal_file = form['crossValFile']
    if crossVal_file.filename:
        crossVal_path = os.path.join("/home/r/rolf/public_html/", crossVal_file.filename)

        # Save uploaded files
        with open(crossVal_path, 'wb') as f:
            while True:
                chunk = crossVal_file.file.read(10000)
                if not chunk:
                    break
                f.write(chunk)

        # Call java program with uploaded files as arguments
        java_command = ['java', '-jar', 'crossVal.jar', '--dataset', crossVal_path]
        java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')

out = java_output

print(jinja2.Environment().from_string(html).render(text=out))