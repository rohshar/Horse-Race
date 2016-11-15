import java.io.*;
import java.lang.Integer;
public class validateinput {
	public static void main(String[] args) {
        String dir = "";
        if (args.length != 0) {
            dir = args[0];
        }
		int[] arr = {1,2,3};
        boolean valid = true;
		for(int i = 0; i < arr.length; i++) {
            checkInput(dir + arr[i] + ".in");
        }
	}
    public static boolean checkInput(String file) {
        //read file
        try{
        BufferedReader r = new BufferedReader(new FileReader(file));
        String s = r.readLine();
        int V = Integer.parseInt(s);
        int adj[][] = new int[V][V];
        for(int j = 0; j < V; j++) {
            s = r.readLine();
            String[] s2 = s.split(" ");
            for(int k = 0; k < V; k++){
                adj[j][k] = Integer.parseInt(s2[k]);
            }
        }
        //check that input is valid
        for(int j = 0; j < V; j++){
            for(int k = 0; k < V; k++) {
                if (j != k && adj[j][k] != 0 && adj[j][k] != 1) {
                    //check that edges are 0 or 1
                    System.out.println(file + " was invalid. incorrect values for edges");
                    return false;
                }
                if (j == k && (adj[j][k] > 99 || adj[j][k] < 0)) {
                    //check that performance rating is <= 99 and >= 0
                    System.out.println(file + " was invalid. incorrect values for performance ratings");
                    return false;
                }
            }
        }
        return true;
        }
        catch (IOException e) {
            //error reading file
            System.out.println(file + " could not be read");
            return false;
        }
    }
        
}