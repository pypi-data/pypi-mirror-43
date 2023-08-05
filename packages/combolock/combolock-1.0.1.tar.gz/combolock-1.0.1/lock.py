import sys
import getpass

from Crypto.Cipher import AES

IV = 'g4vhFIR1KncRIyvO'.encode()

def __encrypt(plaintext, pw):
    suite = AES.new(pw, AES.MODE_CBC, IV)
    ciphertext = suite.encrypt(plaintext)
    return ciphertext

def __decrypt(ciphertext, pw):
    suite = AES.new(pw, AES.MODE_CBC, IV)
    plaintext = suite.decrypt(ciphertext)
    return plaintext

def __pad_nl(text):
    text_len = len(text)
    pad = '\n' * (16 -(text_len % 16))
    return text + pad

def __strip_nl(text):
    while text[-2] == '\n' and text[-1] == '\n':
        text = text[:-1]

    return text

def main():
    if len(sys.argv) != 3:
        print("Usage: python lock.py (-e|-d|--encrypt|--decrypt) <file>")
        return 1

    option = sys.argv[1]
    filename = sys.argv[2]
    pw = getpass.getpass()

    if len(pw) != 16:
        print('Password must be 16 characters!')
        return 1

    pw = pw.encode()

    if option == '-e' or option == '--encrypt':
        plaintext = None
        with open(filename, "r") as f:
            plaintext = f.read()
            f.close()

        plaintext = __pad_nl(plaintext)
        plaintext = plaintext.encode()
        ciphertext = __encrypt(plaintext, pw)

        with open(filename, "wb") as f:
            f.write(ciphertext)
            f.close()

    elif option == '-d' or option == '--decrypt':
        ciphertext = None
        with open(filename, "rb") as f:
            ciphertext = f.read()
            f.close()

        plaintext = __decrypt(ciphertext, pw)
        plaintext = plaintext.decode()
        plaintext = __strip_nl(plaintext)

        with open(filename, "w") as f:
            f.write(str(plaintext))
            f.close()

    else:
        print("Unrecognized option: {}".format(option))
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
