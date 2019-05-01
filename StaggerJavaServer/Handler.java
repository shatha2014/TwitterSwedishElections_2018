/*
Changed code original created by filippiazikou

Found at: https://github.com/filippiazikou/Tweetopolitics/blob/master/ElectionsServer/src/listener/Handler.java

*/


/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.net.Socket;

/**
 *
 * @author filippia
 */
public class Handler extends Thread {

    private Socket clientSocket;
    private TagFile taggedInput;

    public Handler(Socket clientSocket, TagFile taggedInput) {
        System.out.println("Connection Received");
        this.clientSocket = clientSocket;
        this.taggedInput = taggedInput;
    }


    public void run() {
        BufferedInputStream in;
        BufferedOutputStream out;

        try {
            in = new BufferedInputStream(clientSocket.getInputStream());
            out = new BufferedOutputStream(clientSocket.getOutputStream());
        } catch (IOException e) {
            System.out.println(e.toString());
            return;
        }

        Communication c = new Communication(in, out);
        while (true) {
            String received_text = c.ReceiveMessage();
            if (received_text.startsWith("1")) {
                c.SendMessage("ready\n");
                new AnalyzeText(c, taggedInput);
                System.out.println("Done");
                //c.SendMessage("done\n");
            }
            else
                break;
        }

        try {
            out.close();
            in.close();
            clientSocket.close();
            System.out.println ("One connection closed");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}