#!/usr/bin/python3

import cgi
import cgitb
import subprocess
import jinja2


cgitb.enable()

print("Content-type:text/html\n\n")

HTML_START = """
<html>
  <head>
    <title>Genome Length</title>
        <meta charset="UTF-8">

  </head>
  <body>
    <div id="head" style="background-color:#7968ac; text-align: center;">
        <h1 style="margin-bottom: 0; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Genome Length</h1> 
    </div>
<div id="container" style="display: flex; justify-content: center;">
        <div id="menu" style="background-color: #ada3cc; text-align: center; padding: 10px;">
            <h4 style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;"><b>Menu</b></h4><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/index.html" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Home</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/acsearch_with_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">AC-Search</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/genome2aa_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Genome2aa</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/genome_length_CGI.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Genome-Length</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/psscan_CGI.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Psscan</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/spkeyword_with_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Spkeyword</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/cgi_homstrad.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Homstrad</a><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/cgi_alignment.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Alignment</a><br>    
        </div>
    <div id="content" style="text-align: center; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; margin: 0 auto;">"""

HTML_FORM = """
<h4>Find the genome length of selected bacteria from NCBI Genomes.</h4>
<form action="./genome_length_CGI.py" method="post" enctype="multipart/form-data"> 
<table style="margin: 0 auto;">
<tr><td colspan="2">Please enter at least one regular expression to find in the organism names.</td></tr>
<tr><td colspan="2">Multiple regular expressions should be separated by a space.</td></tr>
<tr>
<td><input type="text" name="regEx" multiple size="80" style="margin: 0 auto; display: block;" /></td>
</tr>
<tr>
<td colspan="2" style="text-align: center;"><button type="submit">Submit</button></td>
</tr>
</table>
</form>
<br><br>

{% if text %}
<blockquote>
    {{text}} <br>
</blockquote>
{% endif %}
"""

HTML_END = """\t</div>\n</body>\n</html>"""

form = cgi.FieldStorage()
regEx_values = form.getvalue("regEx")  # Retrieve value for regEx as one string

out = ""
if regEx_values:
    for regEx in regEx_values.split(): #split string into list of strings based on space for multiple args
        if regEx:  # Check if regEx is not empty
            out += subprocess.check_output(["python3", "genome_length.py", "--organism", regEx]).decode("utf-8", "ignore")
            out = out.replace("\n", "<br>")

print(HTML_START)
print(jinja2.Environment().from_string(HTML_FORM).render(text=out))
print(HTML_END)


