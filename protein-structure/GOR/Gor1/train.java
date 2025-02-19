package GOR.Gor1;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
// coil als default for "rare" amino acids (skip in counting)

public class train {
    int windowSize = 17;
    int[][] matrix = new int[20][windowSize];

    static char[] AAs = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'};
    static char[] noAAs = {'B','J','O','U','X','Z'};

    public static void entryFromRunner( HashMap<String, ArrayList<String>> SecLibFile, String modelPath){
        for (ArrayList<String> list : SecLibFile.values()) {
            countOccurences(list.get(0), list.get(1));

            HashMap<String, HashMap<Character, int[]>> ssMatrices = getSsMatrices();
            printMatrixToTxt(ssMatrices, modelPath);

        }
        //printMatrixToTxt(HashMap<String, HashMap<Character, int[]> > maps, String outputpath)
        //printMatrix
    }


    static HashMap<Character, int[]> SheetAminoMatrix = new HashMap<Character, int[]>();
    static HashMap<Character, int[]> CoilAminoMatrix = new HashMap<Character, int[]>();
    static HashMap<Character, int[]> HelixAminoMatrix = new HashMap<Character, int[]>();

    static HashMap<String, HashMap<Character, int[]> > ssMatrices = new HashMap<>();



    public void train() { //initialize matrix
        for (char AA : AAs) { //for each aa/rows of matrix
            SheetAminoMatrix.put(AA, new int[windowSize]);
        }
        for (char AA : AAs) { //for each aa/rows of matrix
            CoilAminoMatrix.put(AA, new int[windowSize]);
        }
        for (char AA : AAs) { //for each aa/rows of matrix
            HelixAminoMatrix.put(AA, new int[windowSize]);
        }
    }


    public static void countOccurences(String Aminosequence, String SecStrucSequence) {
        for (int cur_pos = 8; cur_pos <= Aminosequence.length() - 9; cur_pos++) { // < oder <=
            String cur_sec_struc = SecStrucSequence.substring(cur_pos,cur_pos+1);
            CountWindowSS(cur_sec_struc, Aminosequence.substring(cur_pos-8,cur_pos+(8)+1));
        }
        ssMatrices.put("H", HelixAminoMatrix);
        ssMatrices.put("S", SheetAminoMatrix);
        ssMatrices.put("C", CoilAminoMatrix);
    }

    public static void CountWindowSS(String cur_ss, String window) {
        for (int i = 0; i < window.length(); i++) {
            char cur_AA = window.charAt(i);


            if (cur_ss.equals("E")) {
                if (!isNotAA(noAAs, cur_AA)) {
                    SheetAminoMatrix.get(cur_AA)[i]++;
                }
            }

            if (cur_ss.equals("C")) {
                if (!isNotAA(noAAs, cur_AA)) {
                    CoilAminoMatrix.get(cur_AA)[i]++;

                }
            }
            if (cur_ss.equals("H")) {
                if (!isNotAA(noAAs, cur_AA)) {
                    HelixAminoMatrix.get(cur_AA)[i]++;
                }
            }
        }

    }


    public static void printMatrix(Character c, HashMap<Character, int[]> AminoMatrix){
        System.out.println("="+c+"=");
        for (Character key : AminoMatrix.keySet()) {
            System.out.println();
            System.out.print(key + "\t");
            int[] values = AminoMatrix.get(key);
            for(int value : values){
                System.out.print(value + "\t");
            }
        }
    }

    public static void printMatrixToTxt(HashMap<String, HashMap<Character, int[]> > maps, String outputpath) {
        try {
            FileWriter myWriter = new FileWriter(outputpath);
            for (HashMap<Character, int[]> map : maps.values()) {
                for (Character key : map.keySet()) {
                    myWriter.write("\n");
                    myWriter.write(key + "\t");
                    int[] values = map.get(key);
                    for (int value : values) {
                        myWriter.write(value + "\t");
                    }
                }
                myWriter.write("\n");
            }
            myWriter.close();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }


    public static int getMatrixSum(HashMap<Character, int[]> AminoMatrix){
        int sum = 0;
        for(Character key : AminoMatrix.keySet()){
            int[] values = AminoMatrix.get(key);
            for(int value : values){
                sum += value;
            }
        }
        return sum;
    }

    public static boolean isNotAA(char[] noAA, char cur_base){
        for(char c : noAA){
            if (c == cur_base){
                return true;
            }
        }
        return false;
    }

    public static HashMap<String, HashMap<Character, int[]>> getSsMatrices() {
        return ssMatrices;
    }

//calculate frequencies from matrices:
    //frequency is the actual count not a probability

    //f(S) (not positon specific) (add up whole matrix but bc column sums are the same
    // so just use one column (but the same column from all 3 matrices!)
    //MatrixH[col(i)] / MatrixE[col(i)] + MatrixC[col(i)] + MatrixH[col(i)]

    //f(!S) (not positon sepcific)

    //für jede Matrix/Sec Structure:
    //für jede Position: eine Spalte aus den Matrizen loopen
    //loopen durch rows(amino acids):
    //f(S,a) (sum up the window sequence for each position were looking at, for each window)
    //

    //f(!S,a) (sum up the window sequence from the other two matrices)


    //intelllij professional

}