package GOR;

import GOR.Predict.predict;
import org.apache.commons.cli.*;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;

public class predictRunner {

    public static void main(String[] args) throws ParseException, IOException {
        CommandLineParser parser = new DefaultParser();
        Options options = new Options();
        options.addOption(null, "model", true, "inputpath");
        options.addOption(null, "format", false, "outputpath");
        options.addOption(null, "seq", true, "inputpath");
        options.addOption(null, "maf", false, "inputpath");
        CommandLine cmd = parser.parse(options, args);

        String filePathModel = cmd.getOptionValue("model");
        String filePathFasta = cmd.getOptionValue("seq");
        String format = cmd.getOptionValue("format");

        methodOption(filePathFasta, filePathModel, format);

    }

    public static String readModelFile(String filePathModel) throws IOException {
        String GorName = null;
        try (BufferedReader br = new BufferedReader(new FileReader(filePathModel))) {
            String line;
            while ((line = br.readLine()) != null) { // Loop through each not empty line in the file
                if (line.startsWith("//")) {
                    GorName = line.trim();
                    break;
                }
            }
        }
        return GorName;
    }

    public static void methodOption(String filePathFasta, String filePathModel, String format) throws IOException {
        if (readModelFile(filePathModel).equals("// Matrix3D")) {
            GOR.Gor1.predict.entryFromRunner(filePathFasta, filePathModel, format);
        } else if (readModelFile(filePathModel).equals("// Matrix4D")) {
            //GOR.Gor3.predict.entryFromRunner(filePathFasta, filePathModel, format);
        } else if (readModelFile(filePathModel).equals("// Matrix6D")) {
           // GOR.Gor4.predict.entryFromRunner(filePathFasta, filePathModel, format);
        }
    }

}
