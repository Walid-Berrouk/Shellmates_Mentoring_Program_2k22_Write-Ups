# javaF

## Description

> Help!! I was ransomwared by some java freak! I found some weird .class files, can you recover my favourite image ?

## Write-Up

At first, we get a `chall.zip` file, let's unzip it and see its content :

```
└─$ unzip chall.zip
Archive:  chall.zip
  inflating: AesCrypt.class
  inflating: flag.enc
  inflating: Main.class
```

From there, we get two `java` compiled classes, so let's try to decompile them using [javadecompliers](http://www.javadecompilers.com/) online tool :

```java
class Main {
    public static void main(final String[] array) {
        System.out.println("Pay the ransom dude");
        try {
            new AesCrypt("pUr3Ev!l").encrypt("flag.png", "flag.enc");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
```

```java
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
```

As we can see here, the `flag.enc` file was encrypted using a `AES` encryption code. Fortunatlly for us, the `AesCrypt.java` class has also the decrypt method. So all we have to do is use it to decrypt the flag (From the description and the code, the result must have `.png` extension). Here is the new code of the `Main.java` class :

```java
class Main {
    public static void main(final String[] array) {
        System.out.println("Pay the ransom dude");
        try {
            new AesCrypt("pUr3Ev!l").decrypt("flag.enc", "flag.png");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
```

After compiling it and executing it, we get our flag image : 


<img src="./flag.png"
     alt="Markdown Monster icon"
     style="
     width: 30%;
     diplay: box;"
/>


## Flag

shellmates{1M_JusT_a_jav4_FR34K}

## More Information

 - Java Decomplier : http://www.javadecompilers.com/
