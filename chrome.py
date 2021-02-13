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
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
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


if __name__ == '__main__':
    try:
        with open('decrypted_password.csv', mode='w', newline='') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index", "url", "username", "password"])
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(CHROME_PATH) if
                       re.search("^Profile*|^Default$", element) != None]
            for folder in folders:
                chrome_path_login_db = r"%s\%s\Login Data" % (CHROME_PATH, folder)
                conn = get_db_connection(chrome_path_login_db)
                if (secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    strengthOfPassword = []
                    decryptedPassword = []
                    urlOfSite = []
                    usernameInThatSite = []
                    for index, login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if (url != "" and username != "" and ciphertext != ""):
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            strengthOfPassword.insert(0,check(decrypted_password))
                            decryptedPassword.insert(0,decrypted_password)
                            urlOfSite.insert(0,url)
                            usernameInThatSite.insert(0,username)
                            print("Sequence: %d" % (index))
                            print("URL: %s\nUser Name: %s\nPassword: %s\nHow much strong? %s\n" % (url, username, decrypted_password, check(decrypted_password)))
                            print("*" * 50)
                            csv_writer.writerow([index, url, username, decrypted_password])
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] " % str(e))

plt.plot(decryptedPassword, strengthOfPassword)

plt.xlabel('Passwords')

plt.ylabel('Strength')

plt.title('Graph based on the strength of passwords')

plt.show()


class Table:

    def __init__(self, root):

        for i in range(total_columns):
            for j in range(total_rows):
                self.e = Entry(root, width=20, fg='black',
                               font=('Arial', 14, 'bold'))

                self.e.grid(row=j, column=i)
                self.e.insert(END, lst[i][j])

urlOfSite.insert(0, "URL")
usernameInThatSite.insert(0, "Username")
decryptedPassword.insert(0, "Password")
strengthOfPassword.insert(0, "Strength of the password")

lst = [(urlOfSite),(usernameInThatSite),(decryptedPassword),(strengthOfPassword)]

total_rows = len(lst[0])
total_columns = len(lst)

root = Tk()
root.title('Chrome password retriver')
t = Table(root)
root.mainloop()
