# Aufgabenstellungen:

## genome_length.py:
Schreiben Sie ein Programm, das den Genome Report für Bakterien von der NCBI Genomes
Webseite herunterlädt und dann für alle gegebenen regulären Ausdrücke nach vollständig
sequenzierten Genomen mit passendem Organismus-Namen sucht. Das Programm soll für
alle gefundenen Genome den vollständigen Organismus-Namen und die Genomlänge in Mb
ausgeben.

Hinweise:

• Der Genome Report befindet sich hier: ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_
REPORTS/prokaryotes.txt

• Die Genome können in beliebiger Reihenfolge ausgegeben werden.

genome_length.py --organism <regex1> ... <regexn>
<matched_name>\t<length>
<matched_name>\t<length>
...

Benutzen Sie CGI um das Skript direkt auf Ihrer Praktikumswebsite verfügbar zu machen.


## encode.py:
Schreiben Sie ein Programm, das die sog. Experiment-Liste des ENCODE Projekts (enco-
de.csv ) aus dem Datenverzeichnis lädt und einige Tabellen im tsv-Format ausgibt. Im Data
Ordner unter exampleOutput finden sich Beispiele, die genau vorgeben, wie die output Ta-
bellen formatiert werden müssen. Geben Sie die Antworten auf die unten angegebenen Fragen
in einer separaten Textdatei ab.

• Data Type bezeichnet verschiedene experimentelle Methoden, die bei ENCODE ver-
wendet wurden. Das Skript soll eine Tabelle zusammenstellen, in der zu jedem Da-
ta Type die Anzahl der Experimente diesen Typs steht. Was bedeutet ChIP-seq, was
RNA-seq? 

• Zähle die Anzahl verschiedener ChIP-seq Antikörper für jede Zelllinie (auch Zelllinien
ohne ChIP-seq Experimente) und gib eine entsprechende Tabelle aus. In welcher Zell-
linie wurden die meisten verschiedenen Antikörper verwendet? Wofür stehen NFKB,
Pol2 und H3K27me3? 

• Für welche Zelllinien gibt es sowohl ChIP-seq Experimente für H3K27me3 als auch
RNA-seq Experimente? Geben Sie eine Tabelle aus, die die Zelllinien mit den zugehörigen DCC Accession Nummern für beide Experimenttypen auflistet. Nicht vorhandene
DCC Nummern sollen nicht gelistet werden. Sortieren Sie die DCC Nummern aufstei-
gend. 

encode.py --input <path_to_file> --output <path_to_dir>

Creates files:
exptypes.tsv
antibodies.tsv
chip_rna_seq.tsv

## unique.py
Teilaufgabe a):
Schreiben Sie ein Python-Skript, das alle möglichen Folgen von k Basen aus den Gensequen-
zen eines Genoms (z.B. des E. coli Genoms, im Datenverzeichnis unter Data/Genomes/U00096.ffn)
extrahiert und die Anzahl von Genen bestimmt, die mindestens eine einzigartige Sequenz
von k Basen besitzen. Eine Basensequenz ist einzigartig, wenn sie in keinem anderen Gen
vorkommt. Ihr Programm soll mehrere Werte für k als Eingabe akzeptieren. Geben Sie ei-
ne Tabelle (tab-separiert, eine Zeile für pro Wert für k) aus, die jedem k die Anzahl der
eindeutig identifizierbaren Gene zuordnet.

unique.py --fasta <file> --k <k1> ... <kn>

<k>\t<#unique>

Erweiterung: Plotten Sie die Zahl k auf der x-Achse gegen den Prozentsatz der eindeutig
identifizierbaren Gene auf der y-Achse.

Teilaufgabe b): Erweitern Sie Ihr Skript derart, dass nun pro Sequenz in der fasta Datei
nicht mehr alle beliebigen Folgen der Länge k betrachtet werden, sondern nur die eine Sub-
sequenz, die an einer gegebenen Position im Gen beginnt. Erzeugen Sie eine Tabelle analog
zu a).

Erweiterung: Plotten Sie die Anzahl der Basen die vom Anfang eines E. coli Gens
sequenziert werden müssen, um es eindeutig zu identifizieren, auf der x-Achse gegen den
Prozentsatz der eindeutig identifizierbaren Gene auf der y-Achse.
