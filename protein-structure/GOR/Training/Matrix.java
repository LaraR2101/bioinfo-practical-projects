package GOR.Training;

import java.util.HashMap;

//Jesus: "Matrix klasse die in map gemacht werden kann"
public class Matrix {
    int[][] matrix = new int[20][17];
    char[] AAs = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'};
    int windowSize = 17;
    HashMap<Character, int[]> map;

    public Matrix(){
        for(int i = 0; i <20; i++){
            for(int j = 0; j < 17; j++){
                this.matrix[i][j] = 0;
            }
        }
    }

//    public String printMatrix(){
//
//    }
}
