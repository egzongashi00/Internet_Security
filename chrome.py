from tkinter import *
import re


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


print(check("e"))  # ka vetem me pak se 8 karaktere
print(check("eeeeeeee"))  # ka me shume se 8 karaktere
print(check("1eeeeeee"))  # ka me shume se 8 karaktere + ka numer
print(check("1#eeeeee"))  # ka me shume se 8 karaktere + ka numer + ka special karakter
print(check("12#Leeee"))  # ka me shume se 8 karaktere + ka numer + ka karakter special + ka uppercase shkronje


class Table:

    def __init__(self, root):

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='black',
                               font=('Arial', 14, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])


lst = [("ID", 'username', 'password', 'strength of password'),
       (1, 'egzon', '123', str(check('123'))),
       (2, 'smith', 'Book123#', str(check('Book123#'))),
       (3, 'george', 'george1', str(check('georgee1'))),
       (4, 'barack', 'football', str(check('football')))]

total_rows = len(lst)
total_columns = len(lst[0])


root = Tk()
t = Table(root)
root.mainloop()
