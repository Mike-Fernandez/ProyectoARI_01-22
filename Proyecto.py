from email import message
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import csv


root = Tk()
root.title("Testing")

def cifVigenere(Mensaje, Clave):
    Abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" 
    #Mensaje = input("Ingresa el Mensaje a Cifrar:  ").upper() 
    #Clave = input("Ingresa la Clave:  ").upper()
    Final = "" 
    I = 0  
    
    for x in Mensaje:
        if x == " ":
            Final += "*"
        else: 
            Mod_cl=I%len(Clave) ##segun la letra en la que estemos, sabremos que letra de la clave se le fue asignada
            Asignada=Clave[Mod_cl] ##obtenemos la letra clave asignada
            Sumando=Abecedario.find(x)+Abecedario.find(Asignada) ##sumamos la letra del mensaje y la letra clave asignada a la misma
            Modulo=(Sumando%36) ##obtenido el resultado de la suma, lo modulamos con la longitud del abecedario utilizado
            Final=Final+Abecedario[Modulo] ##Sumamos la letra cifrada, al conjunto de respuesta
            I=I+1 ##aumentamos una posicion, para cifrar la siguiente letra del mensaje

    print (Final) ##revelamos el resultado final
    return Final

def desVigenere(Final, Clave):
#def desVigenere():
    #Final = input("Ingrese el mensaje a descrifrar:  ").upper()
    #Clave = input("Ingresa la Clave:  ").upper()
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
    return """\t{
        \t\"documento\" : \"%s\",
        \t\"primer-nombre\" : \"%s\",
        \t\"apellido\" : \"%s\",
        \t\"credit-card\" : \"%s\",
        \t\"tipo\" : \"%s\",
        \t\"telefono\" : \"%s\"
\t}""" %(row[0],row[1],row[2],row[3],row[4],row[5])


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


def errorMessage():
    messagebox.showerror("ERROR", "La clave ingresada no es valida")

def toXML(clave):
    boolean = clave.isnumeric()
    print("Clave" + clave)
    print("Boolean if clave" + str(boolean))
    if not boolean :
        errorMessage()
        root.quit()
    else :
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
            w.write('\n'.join([convertRowtoXML(n,clave) for n in data]))
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

welcome = Label(root, text="Ingrese la clave para cifrar el numero de tarjeta").pack()
welcome2 = Label(root, text="CLAVE DEBE DE SER NUMÉRICA").pack()
claveVig = Entry(root)
claveVig.pack()

label1 = Label(root, text="Seleccione el archivo para convertirlo a XML").pack()
toXMLbutton = Button(root, text="Convertir a XML", command=lambda: toXML(claveVig.get()))
toXMLbutton.pack()

label2 = Label(root, text="Seleccione el archivo para convertirlo a JSON").pack()
toJSONbutton = Button(root, text="Convertir a JSON", command=toJSON)
toJSONbutton.pack()

buttonQuit = Button(root, text="Exit", command=root.quit)
buttonQuit.pack()

root.mainloop()