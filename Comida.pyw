from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

import sqlite3

def conect():
    miconect = sqlite3.connect("Pedido.db")
    pedido = miconect.cursor()
    
    try:
        pedido.execute('''
            CREATE TABLE Categoria(
                Id_Categ INTEGER PRIMARY KEY AUTOINCREMENT,
                Tipo VARCHAR(6)
            )
        ''')
        
        pedido.execute('''
            INSERT INTO Categoria (Id_Categ, Tipo) VALUES (1, "Comida"), (2, "Bebida")
        ''')
        
        pedido.execute('''
            CREATE TABLE Comida(
                Categoria INTEGER,
                Id_Comida INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre VARCHAR(20),
                Precio INTEGER,
                FOREIGN KEY(Categoria) REFERENCES Categoria(Id_Categ)
            )
        ''')
        
        pedido.execute('''
            INSERT INTO Comida (Categoria, Id_Comida, Nombre, Precio) VALUES 
            (1, 1, "Hamburguesa", 15), 
            (1, 2, "Salchipapas", 12), 
            (1, 3, "Ensalada", 18), 
            (1, 4, "Pizza", 9)
        ''')
        
        pedido.execute('''
            CREATE TABLE Bebida(
                Categoria INTEGER,
                Id_Bebida INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre VARCHAR(20),
                Precio INTEGER,
                FOREIGN KEY(Categoria) REFERENCES Categoria(Id_Categ)
            )
        ''')
        
        pedido.execute('''
            INSERT INTO Bebida (Categoria, Id_Bebida, Nombre, Precio) VALUES 
            (2, 1, "Limonada", 4), 
            (2, 2, "Gaseosa", 3), 
            (2, 3, "Agua", 2)
            ''')
        
        pedido.execute('''
            CREATE TABLE Orden(
                Nro_Orden INTEGER PRIMARY KEY AUTOINCREMENT,
                Comida INTEGER,
                CantCom INTEGER,
                Bebida INTEGER,
                CantBeb INTEGER,
                comentario VARCHAR(150),
                FOREIGN KEY(Comida) REFERENCES Comida(Id_Comida),
                FOREIGN KEY(Bebida) REFERENCES Bebida(Id_Bebida)
                )
            ''')

        pedido.execute('''
            CREATE TABLE Factura(
                Nro_Orden INTEGER,
                Valor_Total INTERGER,
                FOREIGN KEY(Nro_Orden) REFERENCES Orden(Nro_Orden)
                )              
        ''')
        
        miconect.commit()
        messagebox.showinfo("BBDD", "Base de datos creada")
        
    except sqlite3.Error as e:
        messagebox.showwarning("Atención", "La base de datos ya existe")

def salir():
    valor = messagebox.askquestion("Salir", "¿Desea salir de la aplicación?")
    if valor == "yes":
        raiz.destroy()

def limpCamp():
    Comida_combobox.get("")
    CantCom_entry.get("")
    Bebida_combobox.get("")
    CantBeb_entry.get("")
    tcoment_text.delete('1.0', 'end')

def Crear():
    try:
        micin = sqlite3.connect("Pedido.db")
        cur = micin.cursor()

        Comida = Comida_combobox.get()
        CantCom = CantCom_entry.get()
        Bebida = Bebida_combobox.get()
        CantBeb = CantBeb_entry.get()
        Comentario = tcoment_text.get('1.0', 'end')

        datos = (Comida, CantCom, Bebida, CantBeb, Comentario)

        cur.execute("INSERT INTO Orden (Comida, CantCom, Bebida, CantBeb, Comentario) VALUES (?,?,?,?,?)", datos)

        micin.commit()
        messagebox.showinfo("BBDD", "Pedido Creado")

    except sqlite3.Error as error:
        messagebox.showerror("Error", f"No se pudo crear el pedido: {error}")

def leer():
    micin=sqlite3.connect("Pedido.db")
    cur=micin.cursor()
    cur.execute("SELECT * FROM Orden WHERE Nro_Orden="+ Nro_Orden.get())
    USERe=cur.fetchall()
    for Orden in USERe:
        Nro_Orden.set(Orden[0])
        Comida_combobox.set(Orden[1])
        CantCom_entry.set(Orden[2])
        Bebida_combobox.set(Orden[3])
        CantBeb_entry.set(Orden[4])
        tcoment_text.set(1.0,Orden[5])
    micin.commit()

def actualizar():
    micin=sqlite3.connect("Pedido.db")
    cur=micin.cursor()
    cur.execute("UPDATE Orden SET Comida='"+Comida_combobox.get()+"', Cant Comida='"+CantCom_entry.get()+"', Bebida='"+Bebida_combobox.get()+"', Cant Bebida='"+CantBeb_entry.get()+"Comentario='"+tcoment_text.get("1.0".END)+"' WERE Id="+Nro_Orden())

def eliminar():
    micin=sqlite3.connect("Pedido,db")
    cur=micin.cursor()
    cur.execute("DELETE FROM Orden WHERE Id=", Nro_Orden.get())
    micin.commit()
    messagebox.showinfo("Pedido","Eliminado")

raiz=Tk()
raiz.config(bg="peach puff")
raiz.geometry("400x430")
raiz.resizable(False,False)
raiz.iconbitmap("./img/Hamb.ico")
raiz.title("Comidas Rapidas")
#Barra
barraMenu=Menu(raiz)
raiz.config(menu=barraMenu,width=300,height=300)
bbddM=Menu(barraMenu,tearoff=0)
bbddM.add_command(label="Conectar",command=conect)
bbddM.add_command(label="Salir",command=salir)

BorrarM=Menu(barraMenu,tearoff=0)
BorrarM.add_command(label="Borrar",command=limpCamp)

barraMenu.add_cascade(label="BBDD",menu=bbddM)
barraMenu.add_cascade(label="borrar",menu=BorrarM)

#Campos

Mf=Frame(raiz)
texto=Label(Mf,text="Pedido")
Mf.pack()
texto.pack()
texto.config(bg="peach puff")
texto.config(fg="black")
texto.config(font=("Comic Sans MS",20))
texto.grid( padx = 50, pady = 30)
Mf.config(bg="peach puff")

imagen_Hamb =Image.open("./img/Hamb.png")
imagen_Hamb=imagen_Hamb.resize((50, 50))
imagen_Hamb = ImageTk.PhotoImage(imagen_Hamb)
imagen_Comida = ttk.Label(Mf, image=imagen_Hamb)
imagen_Comida.grid(row=0, column=1)

Comida_combobox = ttk.Combobox(Mf, values=["Hamburguesa", "Salchipapas", "Ensalada de Frutas", "Pizza"])
Comida_combobox.grid(row=2, column=0, padx=3, pady=3)

CantCom_entry = Entry(Mf)
CantCom_entry.grid(row=2, column=1, padx=3, pady=3)

Bebida_combobox = ttk.Combobox(Mf, values=["Limonada", "Gaseosa", "Agua"])
Bebida_combobox.grid(row=4, column=0, padx=10, pady=10)

CantBeb_entry = Entry(Mf)
CantBeb_entry.grid(row=4, column=1, padx=3, pady=3)

tcoment_text = Text(Mf, width=16, height=5)
tcoment_text.grid(row=5, column=1, padx=10, pady=10)
sv = Scrollbar(Mf, command=tcoment_text.yview)


#Label

ComidasLabel=Label(Mf,text="Comidas: ")
ComidasLabel.grid(row=1,column=0,sticky="e",padx=10,pady=10)

CantComLabel=Label(Mf,text="Cant: ")
CantComLabel.grid(row=1,column=1,sticky="e",padx=10,pady=10)

BebidasLabel=Label(Mf,text="Bebidas: ")
BebidasLabel.grid(row=3,column=0,sticky="e",padx=10,pady=10)

CantBebLabel=Label(Mf,text="Cant: ")
CantBebLabel.grid(row=3,column=1,sticky="e",padx=10,pady=10)

Comentl=Label(Mf,text="Comentario: ")
Comentl.grid(row=5,column=0,sticky="e",padx=10,pady=10)

#Botones

MF2=Frame(raiz)
MF2.pack()
MF2.config(bg="peach puff")

BC=Button(MF2,text="Crear",command= Crear)
BC.grid(row=1,column=0,sticky="e",padx=10,pady=10)

BA=Button(MF2,text="Actualizar",command=actualizar)
BA.grid(row=1,column=2,sticky="e",padx=10,pady=10)

BB=Button(MF2,text="Borrar",command=eliminar)
BB.grid(row=1,column=3,sticky="e",padx=10,pady=10)

raiz.mainloop()