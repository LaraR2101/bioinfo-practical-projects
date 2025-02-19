#!/usr/bin/python3

import cgi
import cgitb
import subprocess
import jinja2


cgitb.enable()

print("Content-type:text/html\n\n")

html = """
<html>
  <head>
    <title>genome length</title>
  </head>
  
  <body>
  <h1>Find the genome length of selected bacteria from 'NCBI Genomes'</h1>
  <form action="./genome_length_CGI.py" method="post" enctype="multipart/form-data"> 

  <p> Please enter at least one regular expression to find in the organism names: </p>
  <p> Multiple regular expression should be separated by a space. </p>
  <input type="text" name="regEx" multiple />
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

form = cgi.FieldStorage()
regEx_values = form.getvalue("regEx")  # Retrieve value for regEx as one string

out = ""
if regEx_values:
    for regEx in regEx_values.split(): #split string into list of strings based on space for multiple args
        if regEx:  # Check if regEx is not empty
            out += subprocess.check_output(["python3", "genome_length.py", "--organism", regEx]).decode("utf-8", "ignore")
            out = out.replace("\n", "<br>")

print(jinja2.Environment().from_string(html).render(text=out))


