package GOR;

import Alignment.CmdParser;
import GOR.Predict.predict;
import GOR.Training.train;
import org.apache.commons.cli.*;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

public class trainRunner {

    public static void main(String[] args) throws ParseException {
        CommandLineParser parser = new DefaultParser();
        Options options = new Options();
        options.addOption(null, "db", true, "inputpath");
        options.addOption(null, "model", true, "outputpath");
        options.addOption(null, "method", true, "inputpath");
        CommandLine cmd = parser.parse(options, args);

        String inputPath = cmd.getOptionValue("db");
        String gorMethod = cmd.getOptionValue("method");
        String modelPath = cmd.getOptionValue("model");

        Seclib_reader reader = new Seclib_reader();
        File file = new File(inputPath);

        HashMap<String, ArrayList<String>> SecLibFile = reader.readFile(file); //Strin is pdb id, ArrayList<String> is aa and ss seq
        methodOption(gorMethod, SecLibFile, modelPath);
    }
    public static void methodOption(String gorMethod, HashMap<String, ArrayList<String>> SecLibFile, String modelPath) {
        if (gorMethod.equals("gor1")) {
            GOR.Gor1.train.entryFromRunner(SecLibFile, modelPath);
        } else if (gorMethod.equals("gor3")) {
            //GOR.Gor3.train.entryFromRunner(SecLibFile, modelPath);
        } else if (gorMethod.equals("gor4")) {
            //GOR.Gor4.train.entryFromRunner(SecLibFile, modelPath);
        }
    }
}




