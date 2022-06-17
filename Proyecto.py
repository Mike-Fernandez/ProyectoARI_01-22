from tkinter import *
from tkinter import filedialog


root = Tk()
root.title("Testing")
root.geometry("200x200")


#textBox = Entry(root)
#textBox.pack()

def toXML():
    root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI", title="Select a file", filetypes=(("csv files", "*.csv"),("all files", "*.*")))

    label2 = Label(root, text=root.filename).pack()

    # TODO: convertir csv to xml

label1 = Label(root, text="Seleccione el archivo para convertirlo a XML").pack()
toXMLbutton = Button(root, text="Convertir a XML", command=toXML)
toXMLbutton.pack()

buttonQuit = Button(root, text="Exit", command=root.quit)
buttonQuit.pack()

root.mainloop()