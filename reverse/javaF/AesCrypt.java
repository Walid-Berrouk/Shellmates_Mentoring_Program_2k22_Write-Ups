
import javax.crypto.spec.IvParameterSpec;
import java.io.OutputStream;
import javax.crypto.CipherOutputStream;
import java.io.InputStream;
import javax.crypto.CipherInputStream;
import java.security.Key;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.security.MessageDigest;
import java.security.spec.AlgorithmParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.Cipher;

// 
// Decompiled by Procyon v0.5.36
// 

public class AesCrypt {
    private final Cipher cipher;
    private final SecretKeySpec key;
    private AlgorithmParameterSpec spec;

    public AesCrypt(final String s) throws Exception {
        final MessageDigest instance = MessageDigest.getInstance("SHA-256");
        instance.update(s.getBytes("UTF-8"));
        final byte[] key = new byte[32];
        System.arraycopy(instance.digest(), 0, key, 0, key.length);
        this.cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        this.key = new SecretKeySpec(key, "AES");
        this.spec = this.getIV();
    }

    public void decrypt(final String name, final String name2) throws Exception {
        final FileInputStream is = new FileInputStream(name);
        final FileOutputStream fileOutputStream = new FileOutputStream(name2);
        this.cipher.init(2, this.key, this.spec);
        final CipherInputStream cipherInputStream = new CipherInputStream(is, this.cipher);
        final byte[] array = new byte[8];
        while (true) {
            final int read = cipherInputStream.read(array);
            if (read == -1) {
                break;
            }
            fileOutputStream.write(array, 0, read);
        }
        fileOutputStream.flush();
        fileOutputStream.close();
        cipherInputStream.close();
    }

    public void encrypt(final String name, final String name2) throws Exception {
        final FileInputStream fileInputStream = new FileInputStream(name);
        final FileOutputStream os = new FileOutputStream(name2);
        this.cipher.init(1, this.key, this.spec);
        final CipherOutputStream cipherOutputStream = new CipherOutputStream(os, this.cipher);
        final byte[] array = new byte[8];
        while (true) {
            final int read = fileInputStream.read(array);
            if (read == -1) {
                break;
            }
            cipherOutputStream.write(array, 0, read);
        }
        cipherOutputStream.flush();
        cipherOutputStream.close();
        fileInputStream.close();
    }

    public AlgorithmParameterSpec getIV() {
        return new IvParameterSpec(new byte[16]);
    }
}
