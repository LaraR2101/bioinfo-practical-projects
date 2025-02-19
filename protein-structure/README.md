# Instructions:

## visualize_all.py
Schreiben Sie ein Programm unter Verwendung der vorherigen Programme, welches fur ei
ne Liste von PDBs Darstellungen aller Proteine als Bilder in ein Ziel-Verzeichnis speichert
 (sofern dies angegeben ist). Laden Sie (mindestens) die Strukturen 1MBN, 1BAF, 1TIM und
 256b.
Erweitern Sie Ihr Skript um die Moglichkeit, den Abstand zwischen den einzelnen C-Atomen
 (C C)derersten und der letzten Aminosaure zu bestimmen. Berechnen Sie auch die Gro e
 der kleinsten achsenparallelen Box, in die das Protein passen wurde. Wie hoch ist der Anteil
 von Aminosauren, die zu Sekundarstrukturen gehoren in Bezug auf die Aminosauren, fur die
 die raumlichen Koordinaten bekannt sind?(13P)
 Klassi zieren Sie die Strukturen (visuell anhand der Bilder) nach ihrem Sekundarstrukturge
halt. Bestimmen Sie den Fold der Proteine gema der SCOP (http://scop.berkeley.edu/)
 und CATH (http://www.cathdb.info/) Klassi kationen und vergleichen Sie die Ergebnis
se. 
 visualize_all.py--id <p1> ... <pn> [--output <picture_output_dir>]

## makesscc.py
 Schreiben Sie ein Programm, dass eine sogenannte Contact Number Datei (*.sscc) fur eine
 gegebene PDB ID erzeugt. Zwei Atome sind in Kontakt, falls ihr Abstand kleiner als eine
 vorgegebene Kontaktdistanz ist. Die Contact Number Datei enthalt eine Tabelle mit einer
 Zeile fur jede Aminosaure des Proteins. Die Spalten enthalten die Kette (chain), Position
 (pos), Atom-ID (serial), Typ der Aminosaure (aa) und Sekundarstruktur (ss) sowie die An
zahl der globalen (global) und lokalen (local) Kontakte. Als lokal wird ein Kontakt gezahlt,
 falls die beiden Aminosauren weniger als l Positionen in der Aminosauresequenz voneinander
 entfernt sind. Kontakte zwischen allen anderen Paaren werden als global bezeichnet. Die Di
stanzen zwischen den Aminosauren werden auf Basis einer bestimmten Atom-Art berechnet
 (CA, CB, etc.). Sollte eine Aminosaure kein Atom des gewunscheten Typs beinhalten, wird
 sie in der Tabelle nicht eingetragen. Sollte die gegebene PDB-Datei mehrere Modelle fur ein
 Protein enthalten, so berechen Sie nur Kontakte fur das erste Modell.
 Erzeugen Sie zusatzlich eine Kontaktmatrix C, so dass c(i j) = 1 genau dann, wenn die
 Aminosauren i und j Kontakt haben gema der De nition und den Parametern. Speichern
 Sie die Matrix als Datei. Erzeugen Sie eine zweidimensionale Abbildung, die die Abstande
 im Protein durch Farben visualisiert. Speichern Sie die Abbildung als Datei. Erzeugen Sie
 abschlie end die sscc-Dateien fur die Proteine in der vorhergehenden Aufgabe.
 Hierbei ist die d die Kontaktdistanz, t die Atomart, die fur die Berechnung der Distanzen
 verwendet wird und l die Sequenzdistanz fur lokale Kontakte.
 
makesscc.py--id <p1>--distance <d>--type <a>--length <l> 

 [--contactmatrix <o>]
 Std-out:<sscc table>

 ## GOR

Your task is now to implement a simple secondary structure
predictor based on the GOR method and later (task 3) to validate the system using quality
measurements for secondary structure prediction.
Detailed Task Description
You can find a dataset of 513 proteins (the CB513) set in Data/GOR/CB513DSSP.db.
Additionally, you can find a zip archive containing multiple alignments for all of those proteins
(GOR/CB513MultipleAlignments.zip). The secondary structure assignment for the proteins
in the CB513 set have already been annotated to the proteins.

### Seclib-Reader for DSSP and PDB files

The first step in secondary structure prediction is to acquire secondary structures from
different sources. The local data directories provide both <pdb> and <dssp> files of the
Protein Data Bank (pdb). Search and read the respective format specification and implement
a tool to extract the secondary structure either from pdb files directly, or by calling the dssp
tool and reading the output. A list of ids must be converted into a <seclib-file>. Most
proteins consist of multiple chains. Extract the structure of each chain separately (resulting
in one sequence per chain) in such cases. If an id does not exist locally, consider downloading
it from the web and preprocess it via the create-seclib command line tool automatically.
The create-seclib tool should complement your pipeline by creating training sets. Keep it
simple - it may not be necessary to adapt all special cases. Focus on the creation of a
sensible test and training sets. You can use Python for this task.

### GOR I-V

Implement the GOR secondary structure prediction method as discussed in the papers/slides
on the homepage. Start with GOR I and advance to GOR III& IV, finally implement GOR
V. The secondary structure elements must be predicted in three states: H=Helix, E=Sheet
and C=Coil. For every sequence position, you should also print out the probability for the
position to be Helix, Sheet, and Coil. The GOR algorithm splits into two parts: training
and prediction. Thus implement two binaries, one for each task (see specifications).


### Bonus: Postprocessing

Certain secondary structures do not make sense (e.g., CCCHCCC). You may want to imple-
ment a postprocessing to remove such occurences from your predictions. It may be interesting
to evaluate GOR with postprocessing against GOR without postprocessing.

## Validation GOR

Evaluate your secondary structure prediction methods by repeated cross-validation (5-
fold, 5-CV) on the CB513 data set using the Q3 and SOV score. Also evaluate the results
separately for the three possible secondary structure assignments.
Retrain your prediction methods on the complete CB513 dataset.

Define a new test set. Be careful to exclude from training proteins with high sequence
similarity to your test-set. Evaluate your method on your own training/test-set. What are
the differences in performance estimates between the cross-validation and the new test set?
In the Data directory, you can find secondary structure predictions for all proteins in the

CB513 by PSIPRED (GOR/CB513.psipred), an off-the-shelves secondary structure predic-
tion. Calculate both Q3 and SOV score for these predictions and compare them to your own
results. What are the differences between the different GOR versions? Are they statistically
significant? Visualize your results.

