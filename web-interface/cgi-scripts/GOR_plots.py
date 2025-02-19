#!/usr/bin/python3

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
    <title>GOR PLots</title>
        <meta charset="UTF-8">      
            <style>
    /* Global styles */
    body {
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }
    h2 {
        font-size: 18px;
        margin: 0.5em 0; /* Reduce space above and below */
    }
    h3 {
        font-size: 16px;
        margin: 0.5em 0; /* Reduce space above and below */
    }
    p {
        font-size: 14px;
    }
    #menu a {
        display: block; /* Make links block to control width */
        margin: 5px 0; /* Add some space between links */
    }
    /* Style modifications for toggle options */
    fieldset {
        padding: 10px;
        margin: 10px 0;
        width: auto; /* Adjust this value as needed to ensure enough space */
        border: 1px solid #ccc; /* Optional, just for visual enhancement */
    }
    .toggle-option {
        margin-bottom: 5px; /* Space between toggle options */
    }
    .toggle-option input[type="radio"] {
        margin-right: 5px; /* Space between radio button and label */
    }
    .toggle-option label {
        display: inline-block;
        min-width: 150px; /* Adjust this value to ensure labels do not wrap */
    }
    
    .fixed-toggle {
        position: fixed; /* Make the element fixed relative to the viewport */
        top: 20px; /* Distance from the top of the viewport */
        right: 20px; /* Distance from the right of the viewport */
        background-color: white; /* Optional: background color to make it stand out */
        padding: 10px;
        border: 1px solid #ccc; /* Optional: border to distinguish it */
        z-index: 1000; /* Ensure it sits above other content */
    }
    
</style>

  </head>
  <body>
    <div id="head" style="background-color:#7968ac; text-align: center;">
        <h1 style="margin-bottom: 0; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">GOR Plots</h1> 
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
    if (option === "SOV") {
        document.getElementById("div_sov").style.display = "block";
        document.getElementById("div_q3").style.display = "none";
    } else if (option === "Q3") {
        document.getElementById("div_sov").style.display = "none";
        document.getElementById("div_q3").style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', function() {
   toggleFields(document.querySelector('input[name="metric_option"]:checked').value);
}, false);
</script>


<form name="input" action="GOR_plots.py" method="post" enctype="multipart/form-data">

<div class="fixed-toggle" align="left">
    <fieldset>
        <div class="toggle-option">
            <input type="radio" name="metric_option" value="sov" id="sov_option" checked onclick="toggleFields('SOV')">
            <label for="sov_option">Evaluation metric: SOV</label>
        </div>
        <div class="toggle-option">
            <input type="radio" name="metric_option" value="q3" id="q3_option" onclick="toggleFields('Q3')">
            <label for="q3_option">Evaluation metric: Q3</label>
        </div>
    </fieldset>
</div>

 <br>        
<hr>

<div id="div_sov" align="left"> 
    <h2>Five-fold cross validaton:</h2>
    <img src="plots/SOV_crossVal.png" alt="SOV Cross validation plot">

    <br>

    <h2>Parameter Tuning:</h2>
    <p>SOV scores evaluated from the mean across all folds of a 5-fold cross validation.</p>

    <br>

    <h3>Window Size:</h3>
    <img src="plots/SOV_windowSize.png" alt="SOV Window Size Plot">

    <br>

    <h3>Pseudocounts:</h3>
    <img src="plots/SOV_pseudocounts.png" alt="SOV Pseudocount Plot">

    <br>
    
    <h2>Postprocessing: Removing biologically impossible predictions</h2>
    <p>It requires a minimum of 4 consecutive amino acids to form a helix and a minimum of 3 consecutive amino acids to form a sheet </p>
    <p>Singular and double occurences of H and E as well as triple occurences of H were removed and replaced with C.</p>
    <p>Example: CHC would be replaced with CCC.</p>
    <img src="plots/PostprocessingH.png" alt="Postprocessing SOV H">
    <img src="plots/PostprocessingE.png" alt="Postprocessing SOV E">
    <img src="plots/PostprocessingC.png" alt="Postprocessing SOV C">
    
</div>



<div id="div_q3" align="left" style="display:none;">

    <h2>Five-fold cross validaton:</h2>
    <img src="plots/Q3_crossVal.png" alt="Q3 Cross validation plot">

    <br>

    <h2>Parameter Tuning:</h2>
    <p>Q3 scores evaluated from the mean across all folds of a 5-fold cross validation.<p>

    <br>

    <h3>Window Size:</h3>
    <img src="plots/Q3_windowSize.png" alt="Q3 Window Size Plot">

    <br>

    <h3>Pseudocounts:</h3>
    <img src="plots/Q3_pseudocounts.png" alt="Q3 Pseudocount Plot">

    <br>

</div>

"""
HTML_END = "\t</div>\n</body>\n</html>"

form = cgi.FieldStorage()

metric_option = form.getvalue('metric_option')

print(HTML_START)
print(HTML_FORM)
print(HTML_END)