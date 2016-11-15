import java.io.*;
public class checkreadme {
    public static void main(String[] args) throws IOException {
	String[][] group = new String[4][3];
	BufferedReader r = new BufferedReader(new FileReader("README"));
	String s = r.readLine();
	String s2[];
	int i = 0;
	while(s != null && i < 4) {
		group[i] = s.split(", ");
		i++;
		s = r.readLine();
	}
    if (s != null && i >= 4) {
        System.out.println("group too large");
        return;
    }
    while (i < 4) {
        group[i] = null;
        i++;
    }
	System.out.println("Your group is");
	for (i = 0; i < 4; i++) {
		if (group[i] != null) {
            System.out.println("Name: " + group[i][0] + "\t" + "Email: " + group[i][1] + "\t" + "SID: " + group[i][2]);
		}
	}
	}
}