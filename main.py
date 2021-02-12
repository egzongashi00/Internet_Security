import tkinter
import os

OPTIONS = [
"Chrome",
"Mozilla",
"Internet Explorer"
]

window = tkinter.Tk()
window.geometry('500x300')

window.title('Web browser password retriver')

def get():
    if variable.get() == 'Chrome':
        os.system('python chrome.py')


variable = tkinter.StringVar(window)
variable.set(OPTIONS[0])
text = tkinter.Label(window, text = "Zgjedhni njerin nga browseret").place(relx=0.5, rely=0.2,anchor='center')
select = tkinter.OptionMenu(window, variable, *OPTIONS).place(relx=0.4, rely=0.4,anchor='center')
kerkoButton = tkinter.Button(window, text="Kerko", command = get).place(relx=0.6, rely=0.4,anchor='center')


window.mainloop()