package GOR.Predict;

import javax.imageio.metadata.IIOMetadataNode;
import java.io.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Scanner;

//edge cases unbekannte aa als C
//zu kurze sequenzen (kleiner als window) ss als --- ausgeben

public class predict {

//gets passed a model text file  (from training.jar) to convert to Hashmap with count Matrices
// and a Fasta File with aa sequence

    //private HashMap<String, HashMap<Character, int[]>> ssMatrices;

    public HashMap<String, HashMap<Character, int[]>> readModelFile(String filePath) {
        HashMap<String, HashMap<Character, int[]>> modelFileMatrices = new HashMap<>(); // declare HashMap to store matrices

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) { // Loop through each not empty line in the file
                String GorName;
                if (line.startsWith("//")) {
                    GorName = line.trim();
                }

                String MatrixName = null;
                if (line.startsWith("=")) {
                    MatrixName = line.trim();
                }

                HashMap<Character, int []> aaRows = new HashMap<>(); /// Inner hashmap to store amino acid rows of each matrix
                String[] AaColumns = line.trim().split(" "); //split aa rows into cols based on whitespace
                Character aminoAcid = AaColumns[0].charAt(0); // Extract the amino acid character
                int[] values = new int[AaColumns.length - 1]; // Initialize array to store the values in each row (-1 bc first column is aa)
                // Loop through rows starting from index 1 to extract values
                for (int i = 1; i < AaColumns.length; i++) {
                    // Parse each value as an integer and store it in the array
                    values[i - 1] = Integer.parseInt(AaColumns[i]);
                }
                // Put the amino acid and its corresponding values into the inner map
                aaRows.put(aminoAcid, values);

                modelFileMatrices.put(MatrixName, aaRows);
            }
            return modelFileMatrices;
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e); //print "please provide a valid file path"
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    public HashMap<String, String> readFastaFile(String filePathFasta) { //store header and seq in hashmap
        HashMap<String, String> FastaFile = new HashMap<>();
        StringBuilder sequence = new StringBuilder();
        String header = null;
        try (Scanner scanner = new Scanner(new File(filePathFasta))) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                if (line.startsWith(">")) {
                    header = line;
                } else {
                    sequence.append(line.trim()); //append all other lines (not empty or >) to sequence
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        FastaFile.put("Header", header);
        FastaFile.put("AaSeq", sequence.toString());
        return FastaFile;
    }


    //instead of always counting whole matrix, always count first column:
    public HashMap<String, Double> stateFrequenciesInfoDif(HashMap<String, HashMap<Character, int[]>> countMatrices) {
        HashMap<String, Double> stateFrequencies = new HashMap<>();
        double totalH = 0;
        double totalS = 0;
        double totalC = 0;

        for (String secStruc : countMatrices.keySet()) { // Loop over each count matrix (H, S, C)
            HashMap<Character, int[]> countMatrix = countMatrices.get(secStruc); //get matrix

            // Sum up counts for the current sec structure
            for (char aminoAcid : countMatrix.keySet()) {
                int[] counts = countMatrix.get(aminoAcid);
                //only use first column for counting:
                if (secStruc == "=H=") {
                    totalH += counts[0]; // is 0 or 1 first column in matrix?
                } else if (secStruc == "=S=") {
                    totalS += counts[0];
                } else if (secStruc == "=C=") {
                    totalC += counts[0];
                }
            }
        }
        double freqH = totalH / (totalH + totalS + totalC);
        double freqS = totalS / (totalH + totalS + totalC);
        double freqC = totalC / (totalH + totalS + totalC);
        double infoDifH = Math.log((freqS + freqC) / freqH); //need to avoid division by 0 and log(0) ??
        double infoDifS = Math.log((freqH + freqC) / freqS);
        double infoDifC = Math.log((freqS + freqH) / freqC);
        // Store infodif (=info content?) in the hashmap
        stateFrequencies.put("=H=", infoDifH);
        stateFrequencies.put("=S=", infoDifS);
        stateFrequencies.put("=C=", infoDifC);

        return stateFrequencies;
    }

    // formula for information difference (gets called for each window and each sec structure)
    private double calculateInfoDiff(int[] counts, String State, HashMap<String, HashMap<Character, int[]>> CountMatrices) { //parameter: array with counts for each position in window
        double sum = 0.0;
        for (int count : counts) {
            sum += Math.log(count + 1); // + 1 to avoid log(0) ?
            sum += stateFrequenciesInfoDif(CountMatrices).get(State);
        }
        return sum;
    }


    //edge case: unbekannte aa als C predicten:
    char[] AAs = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'};
    public String predictSecondaryStructure(String sequence, HashMap<String, HashMap<Character, int[]>> CountMatrices) { //gets aa sequence and returns predicted ss sequence
        int windowSize = 17;
        StringBuilder predictedSsSeq = new StringBuilder();
        if (sequence.length() < windowSize) { //if sequence is shorter than window
            for (int i = 0; i < windowSize; i++) {
                predictedSsSeq.append('-');
            }
        } else { //if sequence is longer than window
            for (int cur_pos = 8; cur_pos <= sequence.length() - 9; cur_pos++) { //loop over seq
                if (!Arrays.asList(AAs).contains(sequence.charAt(cur_pos)) ) { //if amino acid is not part of 20 aa
                    predictedSsSeq.append("C"); //default predict C
                }

                //add later: If central aa/cur_pos is ambiguous then default should be ss = C
                String window = sequence.substring(cur_pos - 8, cur_pos + 9); //+9 bc last element not included
                String predictedStructure = predictStructurePos(window, CountMatrices); //predicted H/E/C at central pos. of window
                predictedSsSeq.append(predictedStructure);
            }
        }
        return predictedSsSeq.toString();
    }

    //predict ss of central aa of a window:
    private String predictStructurePos(String window, HashMap<String, HashMap<Character, int[]>> CountMatrices) { //gets passed windows of seq from predictSecondaryStructure
        //arrays to store counts of each corresponding (aa and position) countMatrix field for the window:
        int[] windowHelixCounts = new int[window.length()];
        int[] windowSheetCounts = new int[window.length()];
        int[] windowCoilCounts = new int[window.length()];

        for (int i = 0; i < window.length(); i++) { // Loop through positions in the window
            char cur_aa = window.charAt(i); //get aa at that position
            int[] helixMatrix = CountMatrices.get("=H=").get(cur_aa); //get aa row in corresponding count matrix
            int[] sheetMatrix = CountMatrices.get("=S=").get(cur_aa);
            int[] coilMatrix = CountMatrices.get("=C=").get(cur_aa);

            // add counts from matrix to array to store
            windowHelixCounts[i] = helixMatrix[i]; // matrix column = position in the window
            windowHelixCounts[i] = sheetMatrix[i];
            windowCoilCounts[i] = coilMatrix[i];
        }

        double InfDifHelixWindow = calculateInfoDiff(windowHelixCounts, "=H=", CountMatrices);
        double InfDifSheetWindow = calculateInfoDiff(windowSheetCounts, "=S=", CountMatrices);
        double InfDifCoilWindow = calculateInfoDiff(windowCoilCounts, "=C=", CountMatrices);


        // decide predicted structure based on max InfDif value:
        String predictedStructure = "C"; // default is coil (do we need this for edge cases?)
        if (InfDifHelixWindow > InfDifSheetWindow && InfDifHelixWindow > InfDifCoilWindow) {
            predictedStructure = "H";
        } else if (InfDifSheetWindow > InfDifHelixWindow && InfDifSheetWindow > InfDifCoilWindow) {
            predictedStructure = "S";
        } else {
            predictedStructure = "C";
        }

        return predictedStructure;
    }

    //print out results in seclib format (> header, AS , SS ):
    public void printPredictionAsSeclib(String filePathFasta, String filePathModel) {
        System.out.println(readFastaFile(filePathFasta).get("Header"));
        System.out.println(readFastaFile(filePathFasta).get("AaSeq"));
        HashMap<String, HashMap<Character, int[]>> CountMatrices = new HashMap<>();
        CountMatrices = readModelFile(filePathModel);
        System.out.println(predictSecondaryStructure(readFastaFile(filePathFasta).get("AaSeq"), CountMatrices));
    }

    // Bonus: For every sequence position, you should also print out a score/-probability for each conformation

    // New method to handle the format option
    public void FormatOption2(String format) {

    }
    /*
    public void FormatOption(String filePathFasta, String filePathModel) {
        HashMap<String, HashMap<Character, int[]>> CountMatrices = new HashMap<>();
        CountMatrices = readModelFile(filePathModel);
        if (format.equals("txt")) {
            printPredictionAsSeclib(filePathFasta, filePathModel);
        } else if (format.equals("html")) {
            StringBuilder htmlOutput = new StringBuilder();
            htmlOutput.append("<html>");
            htmlOutput.append("<head><title>Prediction Results</title></head>");
            htmlOutput.append("<body>");
            htmlOutput.append("<h1>Prediction Results</h1>");
            htmlOutput.append("<h2>Fasta Header:</h2>");
            htmlOutput.append("<p>").append(readFastaFile(filePathFasta).get("Header")).append("</p>");
            htmlOutput.append("<h2>Amino Acid Sequence:</h2>");
            htmlOutput.append("<p>").append(readFastaFile(filePathFasta).get("AaSeq")).append("</p>");
            htmlOutput.append("<h2>Secondary Structure Prediction:</h2>");
            htmlOutput.append("<p>").append(predictSecondaryStructure(readFastaFile(filePathFasta).get("AaSeq"), CountMatrices)).append("</p>");
            htmlOutput.append("</body>");
            htmlOutput.append("</html>");


        }
    }

//f formel auf gesamte matrix anwenden und dann aufsummieren (vorsicht Nenner nicht null ist)

//input für f formeln window aber nur amino säure an central position relevant als argument)
//wieder mit hashmap, keys amino säuren und counts
//return max(H,C,E)

//predicting:
//Calculate 3 probabilities (P) for each residue to be H/E/C (predict state with max. P.)
//calculate P for each residue:
//move window over sequence, for each central res in window sum up whole matrix
// sum of calucated (log(f...) formula for each position (?)
// f not frequency but acutal count
//f(S)
//f(!S)
//f(S,a) (sum up the window sequence for each position were looking at, for each window)
//f(!S,a) (sum up the window sequence from the other two matrices)
*/
}