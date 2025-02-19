#!/usr/bin/python3

# 645397 dunkel
# ada3cc hell
# add print for errors (if user provides too muhc inout "option x will be used as default")
import cgi
import cgitb
import os.path
import subprocess
import jinja2
import requests

cgitb.enable()
print("Content-type:text/html\n\n")

HTML_START = """
<html>
  <head>
    <title>GOR Train and Predict</title>
        <meta charset="UTF-8">

     <style>
            /* Global styles */
            body {
                font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            }             
            p { 
                font-size: 16px; 
                /* Ensure paragraphs use the same font family */
            }
    </style>

  </head>
  <body>
    <div id="head" style="background-color:#7968ac; text-align: center;">
        <h1 style="margin-bottom: 0; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">GOR Training and Prediction</h1> 
    </div>
    
    <div id="container" style="display: flex; justify-content: center;">

        <div id="menu" style="background-color: #ada3cc; text-align: center; padding: 10px;">
            <h4 style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;"><b>Menu</b></h4><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/index.html" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Home</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/acsearch_with_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">AC-Search</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/genome2aa_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Genome2aa</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/genome_length_CGI.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Genome-Length</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/psscan_CGI.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Psscan</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/spkeyword_with_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Spkeyword</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/cgi_homstrad.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Homstrad</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/cgi_alignment.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Alignment</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/plots.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Plots for Alignment</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/vr_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">What is this?</a><br><br>   
            <a href="http://bioclient1.bio.ifi.lmu.de/~kaciran/Website/cgi_scripts/GOR_validation_values.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">GOR Validation</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~rolf/GOR_train_predict.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">GOR Train & Predict</a><br><br>
            <a href="http://bioclient1.bio.ifi.lmu.de/~rolf/GOR_plots.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">GOR Plots</a><br><br>

        </div>
        <div id="content" style="text-align: center; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; margin: 0 auto;">
       
    
    """

HTML_FORM = """
	  <script>
 function toggleFields(option) {
    if (option === "predict") {
        // Hide unnecessary fields and info text
        document.getElementById("training_field").style.display = "none";
        document.getElementById("predict_model").style.display = "block";
        document.getElementById("aa_seq").style.display = "block";
        document.getElementById("submit").style.display = "block";
    } 
    else if (option === "train_and_predict") {
        // Hide unnecessary fields and info text
        document.getElementById("training_field").style.display = "block";
        document.getElementById("predict_model").style.display = "none";
        document.getElementById("aa_seq").style.display = "block";
        document.getElementById("submit").style.display = "block";
    } 
}

document.addEventListener('DOMContentLoaded', function() {
   toggleFields('predict');
}, false);

</script>

<form name="input" action="GOR_train_predict.py" method="post" enctype="multipart/form-data">
    
<div align="left">
    <fieldset>
        <div>
            <input type="radio" name="gor_option" value="predict" id="predict" checked onclick="toggleFields('predict')">
            <label for="predict">I just want to predict</label>
        </div>
        <div>
            <input type="radio" name="gor_option" value="train_and_predict" id="train_and_predict" onclick="toggleFields('train_and_predict')">
            <label for="train_and_predict">I want to train and predict</label>
        </div>
    </fieldset>
</div>

 <br>        
<hr>

<div id="training_field" align="left">  
    <p>Upload your Training File and choose a GOR version:</p>
    <label for="trainingFile">Training File:</label>
    <input type="file" name="trainingFile">
    
   <label for="gorVersion">Choose a GOR version:</label>
   <select name="gorVersionTrain" id="gorVersionID">
      <option value="gor1">GOR 1</option>
      <option value="gor3">GOR 3</option>
      <option value="gor4">GOR 4</option>
   </select>
   
    <br>
</div>

  

<div id="predict_model" align="left">
   <p> Please provide a Model File for the prediction or choose a GOR version for a default model file: </p>
   <label for="modelFile">Model File:</label>
   <input type="file" name="modelFile" />
  
   <label for="gorVersion">Choose a GOR version:</label>
   <select name="gorVersionPredict" id="gorVersionID">
      <option value="gor1">GOR 1</option>
      <option value="gor3">GOR 3</option>
      <option value="gor4">GOR 4</option>
   </select>
</div>

<br>
<hr>

<div id="aa_seq" align="left">
   <p> Please provide an amino acid sequence in the form of: Fasta File, PDB ID or provide the sequence directly: </p>
   
   <label for="FastaFile">Fasta File:</label>
   <input type="file" id="FastaFile" name="fastaFile" />
   
   <label for="pdbId">PDB ID:</label>
   <input type="text" id="pdbId" name="pdbId" />
   
   <label for="seq"> Amino Acid Sequence:</label>
   <input type="text" id="seq" name="sequence" />
   
   <br>
   <p style="font-size: 14;">Please note: if more than one sequence option is provided only the leftmost option will be predicted.</p>
</div>

<br>
<hr>

<div id="submit" align="left">
   <p>Click to create secondary structure prediction:</p>
   <input type="submit" name="submit"/>
</div>

<br>

</form>

</div>
</div>

<div style="overflow-x: auto; max-width: 100%;">
      <br>
      <br>
      {% if text %}
    <blockquote>
        {{text}} <br>
    </blockquote>
    {% endif %}
</div>

"""
HTML_END = "\t</div>\n</body>\n</html>"


def fbuffer(f, chunk_size=10000):
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        yield chunk


form = cgi.FieldStorage()
out = ""
java_output = None  # set inside if bodies
training_path = None
fasta_path = None
model_path = None

def getFasta(id):
    data_fasta = requests.get("https://www.rcsb.org/fasta/entry/" + id + "/download")
    #fasta_output = ("/home/r/rolf/public_html/" + id + ".fasta")
    fasta_output = os.path.join("/tmp/", id + ".fasta")
    with open(fasta_output, "w") as output:
        output.write(data_fasta.text)
    return fasta_output


# create "Fasta file" from input sequence string
def createFasta(seq):
    header = ">your provided sequence:\n"  # choose a better header line
    fasta_filename = os.path.join("/tmp/", "input_sequence.fasta")
    with open(fasta_filename, 'w') as file:
        file.write(header)
        file.write(seq)
    return fasta_filename


if form:
    gor_option = form.getvalue('gor_option')

    if gor_option == "train_and_predict":
        #print("if gor_option == train_and_predict entered")
        trainingFile = form.getvalue("trainingFile")
        gorVersion = form.getvalue("gorVersionTrain")

        # training file (does gorVersion is not None work correctly?)
        if 'trainingFile' in form and hasattr(form['trainingFile'], 'filename') and gorVersion is not None:
            #print("if 'trainingFile' in form entered")
            training_file = form['trainingFile']
            training_path = os.path.join("/tmp/", training_file.filename)
            with open(training_path, 'wb') as f: #error: Is a directory: '/home/r/rolf/public_html/tmp/'
                while True:
                    chunk = training_file.file.read(10000)
                    if not chunk:
                        break
                    f.write(chunk)

            #  model file (model_path) from training file:
            model_path = "/home/r/rolf/public_html/tmp/trainedModel.txt"
            #db: input path, model: output path, method: gor1/gor3/gor4
            java_command = ['java', '-jar', 'train.jar',
                            '--db', training_path, '--model', model_path, '--method', gorVersion]
            #run_train_jar = subprocess.run(java_command, capture_output=True, text=True) #capture to debug
            run_train_jar = subprocess.run(java_command)  # capture to debug

        # sequences
        fastaFile = form.getvalue("fastaFile")
        pdbID = form.getvalue("pdbId")  # mutliple with .split() ?
        sequence = form.getvalue("sequence")
        # check which sequence format provided:
        # if fastaFile is not None:
        if 'fastaFile' in form and hasattr(form['fastaFile'], 'filename') and form['fastaFile'].filename:
            #print("if 'fastaFile' in form entered")
            # print("if fastaFile entered")
            fasta_file = form['fastaFile']
            fasta_path = os.path.join("/tmp/", fasta_file.filename)
            with open(fasta_path, 'wb') as f:
                while True:
                    chunk = fasta_file.file.read(10000)
                    if not chunk:
                        break
                    f.write(chunk)
        elif 'pdbId' in form and form.getvalue('pdbId'):
            #print("elif pdbID entered")
            fasta_path = getFasta(pdbID)
            # print("getFasta(pdbID) called")
        elif 'sequence' in form and form.getvalue('sequence'):
            # elif sequence is not None:
            fasta_path = createFasta(sequence)

        if training_path is not None and fasta_path is not None:
            try:
                java_command = ['java', '-jar', 'predict.jar', '--model', model_path, '--format', 'html', '--seq',
                                fasta_path]
                java_process = subprocess.run(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                              check=True)
                java_output = java_process.stdout.decode('utf-8', 'ignore')
            except subprocess.CalledProcessError as e:
                print("Not a valid file format")

            """
            java_command = ['java', '-jar', 'predict.jar',
                            '--model', model_path, '--format', 'html', '--seq', fasta_path]
            java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')
            
            """

    elif gor_option == "predict":
        # sequences
        fastaFile = form.getvalue("fastaFile")
        pdbID = form.getvalue("pdbId")  # mutliple with .split() ?
        sequence = form.getvalue("sequence")

        # model
        modelFile = form.getvalue("modelFile")
        gorVersion = form.getvalue("gorVersionPredict")

        # check which model format provided:
        # if modelFile is not None:
        if 'modelFile' in form and hasattr(form['modelFile'], 'filename') and form['modelFile'].filename:
            model_file = form['modelFile']
            model_path = os.path.join("/home/r/rolf/public_html/tmp/", model_file.filename)
            with open(model_path, 'wb') as f:
                while True:
                    chunk = model_file.file.read(10000)
                    if not chunk:
                        break
                    f.write(chunk)
        elif gorVersion is not None: #careful! short path /tmp/ doesnt work
            #print("elif gorVersion is not None: entered")
            if gorVersion == "gor1":
                model_path = os.path.join("/home/r/rolf/public_html/tmp/", "gor1_cb513_model.txt")
                #model_path = os.path.join("/tmp/", "gor1_cb513_model.txt")
            if gorVersion == "gor3":
                model_path = os.path.join("/home/r/rolf/public_html/tmp/", "gor3_cb513_model.txt")
                #model_path = os.path.join("/tmp/", "gor3_cb513_model.txt")
            if gorVersion == "gor4":
                model_path = os.path.join("/home/r/rolf/public_html/tmp/", "gor4_cb513_model.txt")
                #model_path = os.path.join("/tmp/", "gor4_cb513_model.txt")

        # check which sequence format provided:
        # if fastaFile is not None:
        if 'fastaFile' in form and hasattr(form['fastaFile'], 'filename') and form['fastaFile'].filename:
            #print("if fastaFile entered")
            fasta_file = form['fastaFile']
            fasta_path = os.path.join("/tmp/", fasta_file.filename)
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
            # elif sequence is not None:
            fasta_path = createFasta(sequence)

        if model_path is not None and fasta_path is not None:
            try:
                java_command = ['java', '-jar', 'predict.jar', '--model', model_path, '--format', 'html', '--seq',
                                fasta_path]
                java_process = subprocess.run(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                java_output = java_process.stdout.decode('utf-8', 'ignore')
            except subprocess.CalledProcessError as e:
                print("Not a valid file format")

            """
            java_command = ['java', '-jar', 'predict.jar',
                            '--model', model_path, '--format', 'html', '--seq', fasta_path]
            java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')
            """


#print(HTML_START)
print(jinja2.Environment().from_string(HTML_START+HTML_FORM+HTML_END).render(text=java_output))
#print(HTML_END)
