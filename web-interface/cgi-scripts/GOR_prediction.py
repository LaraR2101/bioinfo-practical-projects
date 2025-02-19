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
    <title>GOR Prediction</title>
  </head>

  <body>
  <h1>GOR Prediction</h1>
  <h2>Find a predicted secondary structure for an amino acid sequence</h2>
  <form action="./GOR_prediction.py" method="post" enctype="multipart/form-data"> 

  <p> Please provide an amino acid sequence in the form of: Fasta File, PDB ID or provide the sequence directly: </p>
   
   <label for="FastaFile">Fasta File:</label>
   <input type="file" id="FastaFile" name="fastaFile" />
   
   <label for="pdbId">PDB ID:</label>
   <input type="text" id="pdbId" name="pdbId" />
   
   <label for="seq"> Amino Acid Sequence:</label>
   <input type="text" id="seq" name="sequence" />
   <br> <br>
   
   <p> Please provide a Model File for the prediction or choose a GOR version for a default model file: </p>
   <input type="file" name="modelFile" />
  
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

"""

cgitb.enable()

# Setup Jinja2 template environment
template_loader = jinja2.FileSystemLoader(searchpath="/path/to/your/templates")
template_env = jinja2.Environment(loader=template_loader)

# Process form data
form = cgi.FieldStorage()

UPLOAD_DIR = 'tmp'
java_output = None  # set inside if bodies
model_path = None
fasta_path = None


# model_path = os.path.join("/home/r/rolf/public_html/", "gor1_cb513_model.txt")  # set default paths
# fasta_path = "/home/r/rolf/public_html/shortFasta.fasta"  # set default paths


# get Fasta file from pdb id
def getFasta(id):
    data_fasta = requests.get("https://www.rcsb.org/fasta/entry/" + id + "/download")
    #fasta_output = ("/home/r/rolf/public_html/" + id + ".fasta")
    fasta_output = os.path.join("/home/r/rolf/public_html", id + ".fasta")
    with open(fasta_output, "w") as output:
        output.write(data_fasta.text)
    return fasta_output


# create "Fasta file" from input sequence string
def createFasta(seq):
    header = ">your provided sequence:\n"  # choose a better header line
    fasta_filename = os.path.join("/home/r/rolf/public_html/", "input_sequence.fasta")
    with open(fasta_filename, 'w') as file:
        file.write(header)
        file.write(seq)
    return fasta_filename


# sequences
fastaFile = form.getvalue("fastaFile")
pdbID = form.getvalue("pdbId") #mutliple with .split() ?
sequence = form.getvalue("sequence")

# model
modelFile = form.getvalue("modelFile")
gorVersion = form.getvalue("gorVersion")

# check which model format provided:
#if modelFile is not None:
if 'modelFile' in form and hasattr(form['modelFile'], 'filename') and form['modelFile'].filename:
    model_file = form['modelFile']
    model_path = os.path.join("/home/r/rolf/public_html/tmp/", model_file.filename)
    with open(model_path, 'wb') as f:
        while True:
            chunk = model_file.file.read(10000)
            if not chunk:
                break
            f.write(chunk)
elif gorVersion is not None:
    if gorVersion == "gor1":
        model_path = os.path.join("/home/r/rolf/public_html/", "gor1_cb513_model.txt")
    if gorVersion == "gor3":
        model_path = os.path.join("/home/r/rolf/public_html/", "gor3_cb513_model.txt")
    if gorVersion == "gor4":
        model_path = os.path.join("/home/r/rolf/public_html/", "gor4_cb513_model.txt")


# check which sequence format provided:
#if fastaFile is not None:
if 'fastaFile' in form and hasattr(form['fastaFile'], 'filename') and form['fastaFile'].filename:
    #print("if fastaFile entered")
    fasta_file = form['fastaFile']
    fasta_path = os.path.join("/home/r/rolf/public_html/tmp/", fasta_file.filename)
    with open(fasta_path, 'wb') as f:
        while True:
            chunk = fasta_file.file.read(10000)
            if not chunk:
                break
            f.write(chunk)
elif 'pdbId' in form and form.getvalue('pdbId'):
    #print("elif pdbID entered")
    fasta_path = getFasta(pdbID)
    #print("getFasta(pdbID) called")
elif 'sequence' in form and form.getvalue('sequence'):
#elif sequence is not None:
    fasta_path = createFasta(sequence)



if model_path is not None and fasta_path is not None:
    java_command = ['java', '-jar', 'predict.jar',
                    '--model', model_path, '--format', 'html', '--seq', fasta_path]
    java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')


print(jinja2.Environment().from_string(html).render(text=java_output))



"""

fastaFile = form.getvalue("fastaFile")
#model
modelFile = form.getvalue("modelFile")


#if 'fastaFile' in form and 'modelFile' in form:
if fastaFile is not None or modelFile is not None:
    # Get uploaded files
    fasta_file = form['fastaFile']
    model_file = form['modelFile']
    if fasta_file.filename and model_file.filename:
        # Define paths for uploaded files
        fasta_path_file = os.path.join("/home/r/rolf/public_html/", fasta_file.filename)
        model_path = os.path.join("/home/r/rolf/public_html/", model_file.filename)

        # Save uploaded files
        with open(fasta_path_file, 'wb') as f:
                while True:
                    chunk = fasta_file.file.read(10000)
                    if not chunk:
                        break
                    f.write(chunk)
            #f.write(fasta_file.file.read())
        with open(model_path, 'wb') as f:
                while True:
                    chunk = model_file.file.read(10000)
                    if not chunk:
                        break
                    f.write(chunk)
            #f.write(model_file.file.read())

        # Call java program with uploaded files as arguments
        java_command = ['java', '-jar', 'predict.jar',
                        '--model', model_path, '--format', 'html', '--seq', fasta_path_file]
        java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')

# print("Content-type:text/html\n\n")
print(jinja2.Environment().from_string(html).render(text=java_output))
"""


"""
#get Fasta file from pdb ID
def getFasta(id):
    data_fasta = requests.get("https://www.rcsb.org/fasta/entry/" + id + "/download")
    #fasta_output = ("/home/r/rolf/public_html/" + id + ".fasta")
    fasta_output = os.path.join("/home/r/rolf/public_html", id + ".fasta")
    with open(fasta_output, "w") as output:
        output.write(data_fasta.text)
    return fasta_output
    #pass

#if 'pdbID' in form and 'modelFile' in form:
elif pdbID is not None or modelFile is not None:
    model_file = form['modelFile']
    # Get the PDB IDs from the text input
    pdb_ids = form.getvalue('pdbId') #.split() ?
    fasta_path_ID = getFasta(pdb_ids)  #get path to saved fasta file
    model_path = os.path.join("/home/r/rolf/public_html/", model_file.filename)

    # f.write(fasta_file.file.read())
    with open(model_path, 'wb') as f:
        while True:
            chunk = model_file.file.read(10000)
            if not chunk:
                break
            f.write(chunk)
    # f.write(model_file.file.read())

    # Call java program with uploaded files as arguments
    java_command = ['java', '-jar', 'predict.jar',
                    '--model', model_path, '--format', 'html', '--seq', fasta_path_ID]
    java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')




#create "Fasta file" from input sequence string
def createFasta(seq):
    header = ">your provided sequence:\n"  # choose a better header line
    fasta_filename = os.path.join("/home/r/rolf/public_html/", "input_sequence.fasta")
    #fasta_filename = "input_sequence.fasta"
    with open(fasta_filename, 'w') as file:
        file.write(header)
        file.write(seq)
    return fasta_filename


#if 'sequence' in form and 'modelFile' in form:  #create "fake" fasta file with input sequence and random? header
elif sequence is not None and modelFile is not None:
    model_file = form['modelFile']
    model_path = os.path.join("/home/r/rolf/public_html/", model_file.filename)
    # Get the PDB IDs from the text input
    seq = form.getvalue('sequence')
    fasta_path_Seq = createFasta(seq)  # Get path to saved FASTA file


    # f.write(fasta_file.file.read())
    with open(model_path, 'wb') as f:
        while True:
            chunk = model_file.file.read(10000)
            if not chunk:
                break
            f.write(chunk)
    # f.write(model_file.file.read())

    # Call java program with uploaded files as arguments
    java_command = ['java', '-jar', 'predict.jar',
                    '--model', model_path, '--format', 'html', '--seq', fasta_path_Seq]
    java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')



# print("Content-type:text/html\n\n")
print(jinja2.Environment().from_string(html).render(text=java_output))

"""


