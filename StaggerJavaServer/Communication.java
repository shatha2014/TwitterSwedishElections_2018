/*
Changed code original created by filippiazikou

Found at: https://github.com/filippiazikou/Tweetopolitics/blob/master/ElectionsServer/src/listener/Communication.java

*/

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;

/**
 *
 * @author filippia
 */
public class Communication {
    private BufferedInputStream in;
    private BufferedOutputStream out;

    public Communication(BufferedInputStream in, BufferedOutputStream out) {
        this.in = in;
        this.out = out;
    }

     public String SendMessage(String msg) {
        try {
            byte toClientMsg[] = msg.getBytes(StandardCharsets.UTF_8);
            out.write(toClientMsg, 0, toClientMsg.length);
            out.flush();
            return "SUCCESS";
        } catch (IOException ioException) {
            System.out.println("Unable to send message on server" + ioException.toString());
            return "ERROR";
        }
    }

    public String ReceiveMessage() {
        int msglen, n;

        try {
            byte[] fromClientMsg = new byte[5000];
            n = in.read(fromClientMsg, 0, 5000);
            //System.out.println("received: "+ new String(fromClientMsg));
            return (new String(fromClientMsg,StandardCharsets.UTF_8));
        } catch (IOException ioException) {
            System.out.println("Unable to receive message on server" + ioException.toString());
            return "ERROR";
        }
    }
}