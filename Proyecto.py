from tkinter import *
from tkinter import filedialog
import csv


root = Tk()
root.title("Testing")
root.geometry("200x200")


def convertRowtoJSON(row):
    return """\t{
        \t\"documento\" : \"%s\",
        \t\"primer-nombre\" : \"%s\",
        \t\"apellido\" : \"%s\",
        \t\"credit-card\" : \"%s\",
        \t\"tipo\" : \"%s\",
        \t\"telefono\" : \"%s\"
\t}""" %(row[0],row[1],row[2],row[3],row[4],row[5])


def convertRowtoXML(row):
    return """\t<cliente>
    \t<documento>%s</documento>
    \t<primer-nombre>%s</primer-nombre>
    \t<apellido>%s</apellido>
    \t<credit-card>%s</credit-card>
    \t<tipo>%s</tipo>
    \t<telefono>%s</telefono>
\t</cliente>""" %(row[0],row[1],row[2],row[3],row[4],row[5])

def toXML():
    root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("csv files", "*.csv"),("all files", "*.*")))
    
    f = open(root.filename)
    csv_f = csv.reader(f, delimiter=';')
    data = []

    for row in csv_f:
        data.append(row)
    f.close()

    print(data)

    with open('output.xml', 'w') as w:
        w.write("<clientes>\n")
        w.write('\n'.join([convertRowtoXML(n) for n in data]))
        w.write("\n</clientes>")

    print("it worked!")

def toJSON():
    root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("csv files", "*.csv"),("all files", "*.*")))
    
    f = open(root.filename)
    csv_f = csv.reader(f, delimiter=';')
    data = []

    for row in csv_f:
        data.append(row)
    f.close()

    print(data)

    with open('output.json', 'w') as w:
        w.write("[\n")
        w.write('\n'.join([(convertRowtoJSON(n) + ',') for n in data]))
    
    with open('output.json', 'r') as r:
        fix = r.read()[:-1]
    with open('output.json', 'w') as w:
        w.write(fix)
        w.write("\n]")

    print("it worked!")


label1 = Label(root, text="Seleccione el archivo para convertirlo a XML").pack()
toXMLbutton = Button(root, text="Convertir a XML", command=toXML)
toXMLbutton.pack()

label2 = Label(root, text="Seleccione el archivo para convertirlo a JSON").pack()
toJSONbutton = Button(root, text="Convertir a JSON", command=toJSON)
toJSONbutton.pack()

buttonQuit = Button(root, text="Exit", command=root.quit)
buttonQuit.pack()

root.mainloop()