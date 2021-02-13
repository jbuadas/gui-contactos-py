from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import NO
import sqlite3
import os

class Contactos:    
    def __init__(self,root):
        self.root = root
        self.crear_interfaz()
        ttk.style = ttk.Style()
        ttk.style.configure('Treeview', font=('helvetica 10'))
        ttk.style.configure('Treeview.Heading', font=('helvetica', 12, 'bold'))

   
   #----------Metodos de la interfaz--------------------- 

    def crear_interfaz(self):
        self.crear_panel_logo()
        self.crear_panel_entradas()
        self.crear_area_mensaje()
        self.crear_vista_arbol()
        self.crear_barra_desplazamiento()
        self.crear_botones_abajo()
        self.ver_contactos()
        #self.mostrar_splash_screen()
        self.mostrar_ventana_emergente()

    def crear_panel_logo(self):
        photo = PhotoImage(file='icons/logo.gif')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

    def crear_panel_entradas(self):
        labelframe = LabelFrame(self.root, text='Crear Nuevo Contacto', bg='sky blue', font='helvetica 10')
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        Label(labelframe, text='Nombre:', bg='green', fg='white').grid(row=1, column=1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5, pady=2)
        Label(labelframe, text='Correo:', bg='brown', fg='white').grid(row=2, column=1, sticky=W, pady=2, padx=15)
        self.emailfield = Entry(labelframe)
        self.emailfield.grid(row=2, column=2, sticky=W, padx=5, pady=2)
        Label(labelframe, text='Número:', bg='black', fg='white').grid(row=3, column=1, sticky=W, pady=2, padx=15)
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=3, column=2, sticky=W, padx=5, pady=2)
        Button(labelframe, text='Agregar Contacto', command=self.onclick_boton_agregar_contacto,bg='blue', fg='white').grid(row=4, column=2, sticky=E, padx=5, pady=5)

    def crear_area_mensaje(self):
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=1, sticky=W)
    
    def crear_vista_arbol(self):
        self.tree = ttk.Treeview(height=10, columns=('id_contacto','nombre', 'email', 'number'), show='headings') 
        self.tree.grid(row=6, column=0, columnspan=4)
        self.tree.heading('id_contacto', text='Id', anchor=W) 
        self.tree.column("id_contacto",minwidth=0, width=60, stretch=NO)       
        self.tree.heading('nombre', text='Nombre', anchor=W)        
        self.tree.heading('email', text='Correo Electronico', anchor=W)
        self.tree.heading('number', text='Nro del Contacto', anchor=W)

    def crear_barra_desplazamiento(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=1, column=3, rowspan=10, sticky='sn')

    def crear_botones_abajo(self):
        Button(text='Borrar Seleccionado', command=self.onclick_boton_borrar_seleccionado, bg='red', fg='white').grid(row=8, column=0, sticky=W, pady=10, padx=20)
        Button(text='Modificar Seleccionado', command=self.onclick_boton_modificar_seleccionado, bg='purple', fg='white').grid(row=8, column=1, sticky=W, padx=15)
        #Agregar acá un if para que lo muestre si no existe el archivo DDBB
        if not (os.path.exists('principal.db')):            
            Button(text='Crear Base de Datos', command=self.onclick_boton_crear_base_de_datos, bg='black', fg='white').grid(row=8, column=2, sticky=W)

    def abrir_ventana_modificacion(self):
        id = str(self.tree.item(self.tree.selection())['values'][0])
        nombre = self.tree.item(self.tree.selection())['values'][1]
        email_viejo = self.tree.item(self.tree.selection())['values'][2]
        numero_viejo = self.tree.item(self.tree.selection())['values'][3]
        
        self.emergente = Toplevel()
        self.emergente.title('Actualizar Contacto')
        self.emergente.configure(bg="sky blue")
        Label(self.emergente, text='Nombre:', bg='green', fg='white').grid(row=0, column=1, pady=2, padx=15)
        Entry(self.emergente, textvariable=StringVar(self.emergente, value=nombre), state='readonly').grid(row=0, column=2, padx=5, pady=2)
                
        Label(self.emergente, text='Email Anterior:', bg='brown', fg='white').grid(row=1, column= 1, pady=2, padx=15)
        Entry(self.emergente, textvariable=StringVar(self.emergente, value=email_viejo), state='readonly').grid(row=1, column=2, padx=5, pady=2)
        Label(self.emergente, text='Nuevo Email:', bg='saddle brown', fg='white').grid(row=2, column=1, pady=2, padx=15)
        entNuevoMail = Entry(self.emergente)
        entNuevoMail.grid(row=2, column=2, padx=5, pady=2)       
        
        Label(self.emergente, text='Numero Anterior:', bg='black', fg='white').grid(row=3, column= 1, pady=2, padx=15)
        Entry(self.emergente, textvariable=StringVar(self.emergente, value=numero_viejo), state='readonly').grid(row=3, column=2, padx=5, pady=2)
        Label(self.emergente, text='Nuevo Numero:', bg='dim grey', fg='white').grid(row=4, column=1, pady=2, padx=15)
        entNuevoNumero = Entry(self.emergente)
        entNuevoNumero.grid(row=4, column=2)
        
        Button(self.emergente, text='Actualizar', command=lambda:self.modificar_contacto(id, entNuevoMail.get(), entNuevoNumero.get(), nombre)).grid(row=5, column=2, padx=5, pady=2, sticky=E)
        self.emergente.geometry('280x160')        
        self.emergente.mainloop()

    def mostrar_splash_screen(self):
        self.emergente = Toplevel()
        self.emergente.configure(bg="sky blue")
        Label(self.emergente, text='Splash Screen!', bg='black', fg='white').pack
        self.emergente.mainloop()

    def mostrar_ventana_emergente(self):
        messagebox.showinfo("Pantalla de Login", "Despues voy a poner una pantalla de logueo acá")
    
    #----------Metodos de eventos click de botones--------------------- 
    
    def onclick_boton_crear_base_de_datos(self):
        self.crear_base()
    
    def onclick_boton_agregar_contacto(self):
        self.agregar_contacto()
    
    def onclick_boton_borrar_seleccionado(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Debe seleccionar un contacto para borrar'
            return
        self.borrar_contacto()
    
    def onclick_boton_modificar_seleccionado(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Debe seleccionar un contacto para modificar'
            return
        self.abrir_ventana_modificacion()

    
    #----------Metodos de Manejo de Base de Datos--------------------- 
    
    def crear_base(self):
        conn=sqlite3.connect('principal.db')
        cursor=conn.cursor()
        try:
            cursor.execute('CREATE TABLE lista_contactos (id_contacto INTEGER PRIMARY KEY AUTOINCREMENT, nombre VARCHAR(50), email VARCHAR(20), numero VARCHAR(16))')      
            conn.commit()
            messagebox.showinfo("Creacion de Base", "Se ha creado la Base de Datos") 
        except:
            messagebox.showinfo("Creacion de Base", "La Base de Datos ya existe")           
        conn.close()

    def ejecutar_consulta(self, consulta, parametros=()):
        with sqlite3.connect('principal.db') as conn:
            print(conn)
            print(' Conectaste exitosamente con la Base de Datos')
            cursor = conn.cursor()
            resultado_consulta = cursor.execute(consulta, parametros)
            conn.commit()
        return resultado_consulta

    def agregar_contacto(self):
        if self.validar_insercion():
            consulta = 'INSERT INTO lista_contactos VALUES(NULL,?,?,?)'
            parametros = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            self.ejecutar_consulta(consulta, parametros)
            self.message['text'] = 'Contacto Nuevo {} agregado'.format(self.namefield.get())
            self.namefield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
            self.ver_contactos()
        else:
            self.message['text'] = 'No puede dejar campos en blanco'
            self.ver_contactos()
    
    def validar_insercion(self):
        return len(self.namefield.get()) !=0 and len(self.emailfield.get()) !=0 and len(self.numfield.get()) !=0

    def ver_contactos(self):
        if (os.path.exists('principal.db')):
            items = self.tree.get_children()
            for item in items:
                self.tree.delete(item)
            consulta = 'SELECT * FROM lista_contactos ORDER BY nombre DESC'
            registros = self.ejecutar_consulta(consulta)
            for row in registros:
                #self.tree.insert('', 0, text = row[1], values = (row[2], row[3]))
                self.tree.insert("", END, values=row)

    def borrar_contacto(self):
        self.message['text'] = ''
        id_contacto = str(self.tree.item(self.tree.selection())['values'][0])
        consulta = 'DELETE FROM lista_contactos WHERE id_contacto = ?'
        self.ejecutar_consulta(consulta, id_contacto)
        self.message['text'] = 'Contacto borrado'
        self.ver_contactos()

    def modificar_contacto(self, id, emailNuevo, telefonoNuevo, nombre):
        consulta   = 'UPDATE lista_contactos SET email=?, numero=? WHERE id_contacto=?' 
        parametros = (emailNuevo, telefonoNuevo, id)
        self.ejecutar_consulta(consulta, parametros)
        self.emergente.destroy()
        self.message['text'] = 'Los datos de {} han sido actualizados'.format(nombre)
        self.ver_contactos()


#----------PRINCIPAL--------------------- 

if __name__ == '__main__':
    root = Tk()      
    root.geometry('650x450')
    root.resizable(width=False, height=False)
    root.title('Mi Lista de Contactos')
    root.iconbitmap('icons/icon.ico')    
    application = Contactos(root)
    root.mainloop()
