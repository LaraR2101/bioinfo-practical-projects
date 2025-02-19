package GOR;

import Alignment.CmdParser;
import GOR.Predict.predict;
import GOR.Training.train;


import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

public class Main {

    public static void main(String[] args) {

        CmdParser parser = new CmdParser("--db", "--method", "--model");
        String inputPath = parser.getValue("--db");
        String gorMathod = parser.getValue("--method");
        String outputPath = parser.getValue("--model");

        CmdParser parserPredict = new CmdParser("--model", "--format", "--seq", "--maf");
        String filePathFasta = parserPredict.getValue("--seq");
        String filePathModel = parserPredict.getValue("--model");



        Seclib_reader reader = new Seclib_reader();

        File file = new File("./GOR/CB513DSSP.db");
        //File file = new File(inputPath);

        HashMap<String, ArrayList<String>> map = reader.readFile(file);

        train trainingdata = new train();
        trainingdata.train();

        for (ArrayList<String> list : map.values()) {
            trainingdata.countOccurences(list.get(0), list.get(1));
        }
        /*
        HashMap<Character, HashMap<Character, int[]>> ssMatrices = trainingdata.getSsMatrices();

        trainingdata.printMatrixToTxt('H', ssMatrices);



         */

        predict prediction = new predict();
        prediction.printPredictionAsSeclib(filePathFasta, filePathModel);

    }
}



