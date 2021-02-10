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
