import tkinter as tk
parent = tk.Tk()
parent.geometry("400x250")
email = tk.Label(parent, text = "Username").place(x = 90, y = 90)
password =  tk.Label(parent, text = "Password").place(x = 90, y = 130)
sbmitbtn = tk.Button(parent, text = "Log In", activebackground = "green", activeforeground = "blue").place(x = 190, y = 170)
entry1 = tk.Entry(parent).place(x = 160, y = 90)
entry2 = tk.Entry(parent, show="*").place(x = 160, y = 130)
parent.mainloop()