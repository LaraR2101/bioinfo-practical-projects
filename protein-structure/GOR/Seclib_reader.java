package GOR;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;

public class Seclib_reader {

public HashMap<String,ArrayList<String>> readFile(File file){

    HashMap<String, ArrayList<String>> mapData = new HashMap<>();
        String id = "";
        String temp_as = "";
        String temp_ss = "";

        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));

            //reader = new BufferedReader(new FileReader(file));
            String line;
            while((line = reader.readLine()) != null){
                if(line.startsWith(">")){
                    id = line.replace(">","").trim();
                }
                if(line.length() < 17){
                    continue;
                }
                if (line.startsWith("AS ")){
                    temp_as = line.substring(3).trim();
                }
                if(line.startsWith("SS ")){
                    temp_ss = line.substring(3).trim();
                }

                if(!id.isEmpty() && !temp_as.isEmpty() && !temp_ss.isEmpty()) {
                    ArrayList<String> as_ss = new ArrayList<>();
                    as_ss.add(temp_as);
                    as_ss.add(temp_ss);
                    mapData.put(id, as_ss);

                    id = "";
                    temp_as = "";
                    temp_ss = "";
                }
            }
        } catch (IOException e){
            e.printStackTrace();

        }
        return mapData;

    }
}
