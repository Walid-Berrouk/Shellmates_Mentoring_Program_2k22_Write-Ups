class Main {
    public static void main(final String[] array) {
        System.out.println("Pay the ransom dude");
        try {
            // new AesCrypt("pUr3Ev!l").encrypt("flag.png", "flag.enc");
            new AesCrypt("pUr3Ev!l").decrypt("flag.enc", "flag.png");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}