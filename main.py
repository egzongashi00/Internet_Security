import tkinter 

OPTIONS = [
"Chrome",
"Mozilla",
"Internet Explorer"
]

window = tkinter.Tk()
window.geometry('500x300')

variable = tkinter.StringVar(window)
variable.set(OPTIONS[0])
text = tkinter.Label(window, text = "Zgjedhni njerin nga browseret").place(relx=0.5, rely=0.2,anchor='center')
select = tkinter.OptionMenu(window, variable, *OPTIONS).place(relx=0.4, rely=0.4,anchor='center')
kerkoButton = tkinter.Button(window, text="Kerko").place(relx=0.6, rely=0.4,anchor='center')

def get():
    print ("value is:" + variable.get())


window.mainloop()