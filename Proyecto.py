from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import csv
import jwt
import json
import xml.etree.ElementTree as xet
import pandas as pd

root = Tk()
root.title("Proyecto ARI")
root.geometry("450x600")

delimitadores = [
    ',',
    ';',
]

clicked = StringVar()
clicked.set(delimitadores[1])

def cifVigenere(Mensaje, Clave):
    Abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" 
    Final = "" 
    I = 0  
    
    for x in Mensaje:
        if x == " ":
            Final += "*"
        else: 
            Mod_cl=I%len(Clave) 
            Asignada=Clave[Mod_cl] 
            Sumando=Abecedario.find(x)+Abecedario.find(Asignada) ##sumamos la letra del mensaje y la letra clave asignada a la misma
            Modulo=(Sumando%36) ##obtenido el resultado de la suma, lo modulamos con la longitud del abecedario utilizado
            Final=Final+Abecedario[Modulo] ##Sumamos la letra cifrada, al conjunto de respuesta
            I=I+1 ##aumentamos una posicion, para cifrar la siguiente letra del mensaje

    return Final

def desVigenere(Final, Clave):
    Abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cad=""
    I=0
    for x in Final:
        if x == " " or x=="*":
            cad+= " "
        else:        
            Mod_cl=I%len(Clave)
            Asignada=Clave[Mod_cl]
            mov=Abecedario.find(x)-Abecedario.find(Asignada)                    
            Modulo=(mov%36)            
            cad=cad+Abecedario[Modulo]
            I=I+1
    print(cad)
    return cad


def convertRowtoJSON(row, clave):
    objeto = """{
    \"documento\": \"%s\",
    \"primer-nombre\": \"%s\",
    \"apellido\": \"%s\",
    \"credit-card\": \"%s\",
    \"tipo\": \"%s\",
    \"telefono\": \"%s\"
    }""" %(row[0],row[1],row[2],row[3],row[4],row[5])
    return createJWT(objeto, clave)


def convertRowtoXML(row, clave):
    ccNumCifrado = cifVigenere(row[3], clave)
    return """\t<cliente>
    \t<documento>%s</documento>
    \t<primer-nombre>%s</primer-nombre>
    \t<apellido>%s</apellido>
    \t<credit-card>%s</credit-card>
    \t<tipo>%s</tipo>
    \t<telefono>%s</telefono>
\t</cliente>""" %(row[0],row[1],row[2],ccNumCifrado,row[4],row[5])


def createJWT(json1, clave):

    try:
        a = json.loads(json1)    
        token = jwt.encode(payload=a, key=clave)
        return token
    except:
        errorMessage("Error cifrando objeto JSON")

def showInputFile(filename):
    file = open(filename)
    scrollInStringvar.set(file.read())
    file.close()

def showOutputFile(filename):
    file = open(filename)
    scrollOutStringvar.set(file.read())
    file.close()

def decodeJWT(row, clave):
    token = row[0]
    return jwt.decode(token,clave,algorithms=['HS256',])

def messageBox(mensaje):
    messagebox.showinfo("Info", mensaje)

def errorMessage(mensaje):
    messagebox.showerror("ERROR", mensaje)

def XMLtoCSV(clave):
    rows = ""
    root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("XML files", "*.xml"),("all files", "*.*")))
    xmlParse = xet.parse(root.filename)
    xmlR = xmlParse.getroot()
    for i in xmlR:
        documento = i.find("documento").text
        primer_nombre = i.find("primer-nombre").text
        apellido = i.find("apellido").text
        credit_card = i.find("credit-card").text
        tipo = i.find("tipo").text
        telefono = i.find("telefono").text

        rows += """%s %s %s %s %s %s \n"""%(documento+clicked.get(), primer_nombre+clicked.get(),
                                           apellido + clicked.get(), desVigenere(credit_card,clave) + clicked.get(),
                                           tipo + clicked.get(), telefono)
            
    
    showInputFile(root.filename)
    messageBox("Seleccione donde quiere guardar el archivo resultado")
    outputfile = filedialog.asksaveasfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", defaultextension=".csv", title="Save As",
                                              filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    with open(outputfile, 'w') as w:
        w.write(rows)
    
    showOutputFile(outputfile)

def JSONtoCSV():
    root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("JSON files", "*.json"),("all files", "*.*")))
    pdObject = pd.read_json(root.filename, orient='values')
    csvData = pdObject.to_csv(index=False)
    showInputFile(root.filename)
    messageBox("Seleccione donde quiere guardar el archivo resultado")
    outputfile = filedialog.asksaveasfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", defaultextension=".csv", title="Save As",
                                              filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    with open(outputfile, 'w') as w:
        w.write(csvData)
    showOutputFile(outputfile)


def JWTtoJSON(clave):
    try:
        root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("text files", "*.txt"),("all files", "*.*")))
        delimitador = clicked.get()
        f = open(root.filename)
        csv_f = csv.reader(f, delimiter=delimitador)
        data = []

        for row in csv_f:
            data.append(row)
        f.close()

        showInputFile(root.filename)

        messageBox("Seleccione donde quiere guardar el archivo resultado")
        outputfile = filedialog.asksaveasfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", defaultextension=".json", title="Save As",
                                              filetypes=(("JSON files", "*.json"), ("All files", "*.*")))

        with open(outputfile, 'w') as w:
            w.write("[\n")
            w.write("\n".join([(str(decodeJWT(n, clave))+',') for n in data]))

        with open(outputfile, 'r') as r:
            fix = r.read()[:-1]
        fix2 = fix.replace("'", '"')
        print(fix2)
        with open(outputfile, 'w') as w:
            w.write(fix2)
            w.write("\n]")
        showOutputFile(outputfile)
    except:
        errorMessage("Error al decodificar JWT, verifique que el delimitador sea el correcto")

    print("it worked!")


def toXML(clave):
    boolean = clave.isnumeric()
    print("Clave" + clave)
    print("Boolean if clave" + str(boolean))
    if not boolean :
        errorMessage("La clave ingresada no es valida")
        root.quit()
    else :
        root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("csv files", "*.csv"),("all files", "*.*")))
        delimitador = clicked.get()
        f = open(root.filename)
        csv_f = csv.reader(f, delimiter=delimitador)
        data = []

        for row in csv_f:
            data.append(row)
            
        f.close()

        showInputFile(root.filename)
        messageBox("Seleccione donde quiere guardar el archivo resultado")
        outputfile = filedialog.asksaveasfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", defaultextension=".xml", title="Save As",
                                              filetypes=(("XML files", "*.xml"), ("All files", "*.*")))
        with open(outputfile, 'w') as w:
            w.write("<clientes>\n")
            w.write('\n'.join([convertRowtoXML(n,clave) for n in data]))
            w.write("\n</clientes>")

        showOutputFile(outputfile)
        print("it worked!")

def toJSON(clave):
    root.filename = filedialog.askopenfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", title="Select a file", filetypes=(("csv files", "*.csv"),("all files", "*.*")))
    delimitador = clicked.get()
    f = open(root.filename)
    csv_f = csv.reader(f, delimiter=delimitador)
    data = []

    for row in csv_f:
        data.append(row)
    f.close()

    print(data)

    showInputFile(root.filename)

    messageBox("Seleccione donde quiere guardar el archivo resultado")
    outputfile = filedialog.asksaveasfilename(initialdir="/Users/operator/Documents/ARI/Proyecto", defaultextension=".txt", title="Save As",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    with open(outputfile, 'w') as w:
#        w.write("[\n")
        w.write('\n'.join([(str(convertRowtoJSON(n, clave)) + ',') for n in data]))
    
#    with open('jwt.txt', 'r') as r:
#        fix = r.read()[:-1]
#    with open('jwt.txt', 'w') as w:
#        w.write(fix)
#        w.write("\n]")

    showOutputFile(outputfile)
    print("it worked!")

mainFrame=Frame(root)
mainFrame.pack(fill=BOTH, expand=1)

espacio = Canvas(mainFrame)
espacio.pack(side=LEFT,fill=BOTH,expand=1)

scrollGlobal = Scrollbar(mainFrame, orient=VERTICAL, command=espacio.yview)
scrollGlobal.pack(side=RIGHT,fill=Y)

espacio.configure(yscrollcommand=scrollGlobal.set)
espacio.bind('<Configure>', lambda e: espacio.configure(scrollregion=espacio.bbox("all")))

sFrame = Frame(espacio)

espacio.create_window((0,0),window=sFrame, anchor="nw")


welcome = Label(sFrame, text="Ingrese la clave a usar en el cifrado o descifrado").pack()
welcome2 = Label(sFrame, text="CLAVE DEBE DE SER NUMÉRICA").pack()
claveVig = Entry(sFrame)
claveVig.pack()

labelDelim = Label(sFrame, text="Seleccione el delimitador del archivo a procesar \n Si se produce algun error verifique que el delimitador sea el correcto").pack()
drop = OptionMenu(sFrame, clicked,*delimitadores)
drop.pack()

label1 = Label(sFrame, text="Seleccione el archivo para convertirlo a XML").pack()
toXMLbutton = Button(sFrame, text="Convertir a XML", command=lambda: toXML(claveVig.get()))
toXMLbutton.pack()

label2 = Label(sFrame, text="Decodifique JWT a JSON").pack()
toXMLbutton = Button(sFrame, text="Decodifique JWT", command=lambda: JWTtoJSON(claveVig.get()))
toXMLbutton.pack()

label3 = Label(sFrame, text="Seleccione el archivo para convertirlo a JSON").pack()
toJSONbutton = Button(sFrame, text="Convertir a JSON", command=lambda: toJSON(claveVig.get()))
toJSONbutton.pack()

labelreverseXML = Label(sFrame, text="Seleccione el documento XML para convertirlo a csv").pack()
XMLtoCSVbutton = Button(sFrame, text="Convertir XML a CSV", command=lambda: XMLtoCSV(claveVig.get())).pack()

labelreverseJSON = Label(sFrame, text="Seleccione el documento JSON para convertirlo a csv").pack()
XMLtoCSVbutton = Button(sFrame, text="Convertir JSON a CSV", command=lambda: JSONtoCSV()).pack()


label4=Label(sFrame, text="Archivo fuente de los datos a procesar").pack()


scrollInStringvar = StringVar()
scrollInStringvar.set("Aqui se mostrará el documento origen")
scrollIn= Label(sFrame, textvariable=scrollInStringvar, wraplength=1000).pack(pady=10,padx=10)

label5=Label(sFrame, text="Archivo fuente de los datos a procesados").pack()

scrollOutStringvar = StringVar()
scrollOutStringvar.set("Aqui se mostrará el documento generado")
#globalScroll = Scrollbar(sFrame)
#globalScroll.pack(side=RIGHT, fill='y')
#Entry(sFrame, textvariable=scrollOutStringvar, state='readonly')
scrollOut = Label(sFrame, textvariable=scrollOutStringvar, wraplength=1000)
scrollOut.pack(pady=10,padx=10)
#outScroll= Scrollbar(sFrame, orient='vertical', command=scrollOut.yview)
#scrollOut.config(yscrollcommand=outScroll.set)
#outScroll.pack(side=RIGHT)

#globalScroll.config(command = scrollOut.yview)

buttonQuit = Button(sFrame, text="Exit", command=sFrame.quit)
buttonQuit.pack()

root.mainloop()