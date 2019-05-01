/*
Changed code original created by filippiazikou

Found at: https://github.com/filippiazikou/Tweetopolitics/blob/master/ElectionsServer/src/stagger/AnalyzeText.java

*/
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import se.su.ling.stagger.FormatException;
import se.su.ling.stagger.TagNameException;

/**
 *
 * @author filippia
 */
public class AnalyzeText {

    Communication c;
    TagFile taggedInput;

    public AnalyzeText(Communication c, TagFile taggedInput) {
        this.taggedInput = taggedInput;
        this.c = c;
        try {
            ExchangeMassages();
        } catch (IOException | ClassNotFoundException | FormatException | TagNameException ex) {
            Logger.getLogger(AnalyzeText.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    private void ExchangeMassages() throws IOException, ClassNotFoundException, FormatException, TagNameException {
        String taggedSentense, received_text, cleaned_received_text;
        while (true) {
            received_text = c.ReceiveMessage();

            if (received_text.startsWith("EOF") || received_text.startsWith("ERROR")) {
                break;
            } else {
                cleaned_received_text = received_text.replaceAll("[^\\x00-\\x7F]", "");
                //If more than 50% of the text consists of invalid characters, then the whole text is considered invalid
                if (cleaned_received_text.length() < received_text.length()/2)
                    taggedSentense = "";
                else
                    taggedSentense = taggedInput.getTaggedText(received_text);
                //System.out.println("tagged: " + taggedSentense);
                c.SendMessage(taggedSentense + "\n");
            }
        }
    }
}


