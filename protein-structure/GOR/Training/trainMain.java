package GOR.Training;

import org.apache.commons.cli.*;
import GOR.Seclib_reader;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

public class trainMain {
    public static void main(String[] args) throws ParseException {
        CommandLineParser parser = new DefaultParser();
        Options options = new Options();
        options.addOption(null,"db", true, "inputpath");
        options.addOption(null,"model", true, "outputpath");
        options.addOption(null,"method", true, "inputpath");
        CommandLine cmd = parser.parse(options,args);

        String inputPath = cmd.getOptionValue("db");
        String gorMethod = cmd.getOptionValue("method");
        String modelPath = cmd.getOptionValue("model");


        Seclib_reader reader = new Seclib_reader();
        File file = new File(inputPath);

        HashMap<String, ArrayList<String>> map = reader.readFile(file);

        train trainingdata = new train();
        trainingdata.train();

        for (ArrayList<String> list : map.values()) {
            trainingdata.countOccurences(list.get(0), list.get(1));

            HashMap<String, HashMap<Character, int[]>> ssMatrices = trainingdata.getSsMatrices();
            trainingdata.printMatrixToTxt(ssMatrices, modelPath);

        }
    }
}
