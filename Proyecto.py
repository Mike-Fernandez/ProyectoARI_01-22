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
    a = json.loads(json1)    
    token = jwt.encode(payload=a, key=clave)
    return token

#    try:
#        f = open("output.json")
#        pl = json.load(f)
#        print("/////////////////PAYLOAD/////////////////")
#        print(pl)
#        token = jwt.encode(payload=pl, key=clave)
#        with open("jwt.txt", 'w') as w:
#            w.write(token)
#    except:
#        errorMessage("Error while fetching json object")
#    finally:
#        f.close()
#    

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
    cols = ["documento", "primer-nombre", "apellido", "credit-card", "tipo", "telefono"]
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

welcome = Label(root, text="Ingrese la clave a usar en el cifrado o descifrado").pack()
welcome2 = Label(root, text="CLAVE DEBE DE SER NUMÉRICA").pack()
claveVig = Entry(root)
claveVig.pack()

labelDelim = Label(root, text="Seleccione el delimitador del archivo a procesar \n Si se produce algun error verifique que el delimitador sea el correcto").pack()
drop = OptionMenu(root, clicked,*delimitadores)
drop.pack()

label1 = Label(root, text="Seleccione el archivo para convertirlo a XML").pack()
toXMLbutton = Button(root, text="Convertir a XML", command=lambda: toXML(claveVig.get()))
toXMLbutton.pack()

label2 = Label(root, text="Decodifique JWT a JSON").pack()
toXMLbutton = Button(root, text="Decodifique JWT", command=lambda: JWTtoJSON(claveVig.get()))
toXMLbutton.pack()

label3 = Label(root, text="Seleccione el archivo para convertirlo a JSON").pack()
toJSONbutton = Button(root, text="Convertir a JSON", command=lambda: toJSON(claveVig.get()))
toJSONbutton.pack()

labelreverseXML = Label(root, text="Seleccione el documento XML para convertirlo a csv").pack()
XMLtoCSVbutton = Button(root, text="Convertir XML a CSV", command=lambda: XMLtoCSV(claveVig.get())).pack()

labelreverseJSON = Label(root, text="Seleccione el documento JSON para convertirlo a csv").pack()
XMLtoCSVbutton = Button(root, text="Convertir JSON a CSV", command=lambda: JSONtoCSV()).pack()


label4=Label(root, text="Archivo fuente de los datos a procesar").pack()


scrollInStringvar = StringVar()
scrollInStringvar.set("Aqui se mostrará el documento origen")
scrollIn= Label(root, textvariable=scrollInStringvar, wraplength=1000).pack(pady=10,padx=10)

label5=Label(root, text="Archivo fuente de los datos a procesados").pack()

scrollOutStringvar = StringVar()
scrollOutStringvar.set("Aqui se mostrará el documento generado")
#globalScroll = Scrollbar(root)
#globalScroll.pack(side=RIGHT, fill='y')
scrollOut= Entry(root, textvariable=scrollOutStringvar, state='readonly').pack(pady=10,padx=10)
outScroll= Scrollbar(root, orient='vertical', command=scrollOut.yview)
outScroll.pack(side=RIGHT)
scrollOut.config(yscrollcommand=outScroll.set)

#globalScroll.config(command = scrollOut.yview)

buttonQuit = Button(root, text="Exit", command=root.quit)
buttonQuit.pack()

root.mainloop()