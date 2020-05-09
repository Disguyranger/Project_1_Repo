from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title('Hahahheehdlfajhdsjjlfah')


# showinfo, showwarning, showerror, askquestion, askokcancel, askyesno

def popup():
    response = messagebox.showerror('Dis is poopup', 'You goofy!')
    Label(root, text = response).pack()
    if response == 1:
        Label(root, text = 'You bitch!').pack()
    else:
        Label(root, text = 'You nota bitch!').pack()
Button(root, text = 'Popup', command = popup()).pack()





root.mainloop()
