'''
Proyecto II de Intro
José Antonio y Luis Rodriguez
Inicio de sesión o Menú principal
'''
import tkinter as tk
from tkinter import StringVar, messagebox, filedialog, ttk
import json
import os


class Jugador:   #representa a cualquier jugador que ingrese al juego
    def __init__(self, nombre, contraseña, victorias_atacante=0, victorias_defensor=0):
        self.nombre=nombre
        self.contraseña=contraseña
        self.victorias_atacante=victorias_atacante  #por si no tienen victorias en ambos casos, pone el valor como 0
        self.victorias_defensor=victorias_defensor
    
    def suma_victoria(self,rol):
        if rol=="atacante":
            self.victorias_atacante+=1
        elif rol=="defensor":
            self.victorias_defensor+=1
    
    def total_victorias(self):
        return self.victorias_atacante + self.victorias_defensor
    
    def a_diccio(self):
        return {"contraseña": self.contraseña, "rol": "jugador", "victorias_atacante": self.victorias_atacante, "victorias_defensor": self.victorias_defensor}
    
    @staticmethod
    def del_diccio(nombre, datos):
        #Crea un jugador desde un diccionario
        return Jugador(nombre, datos["contraseña"], datos.get("victorias_atacante", 0), datos.get("victorias_defensor", 0))


#Clase para el manejo de archivos
class Gestor_archivos:
    def __init__(self, ruta_archivo="jugadores.json"):
        self.ruta_archivo = ruta_archivo
    
    def cargar_jugadores(self):
        #Carga todos los jugadores del archivo .json
        if os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, 'r') as file:
                datos = json.load(file)
                # Convierte diccionarios a objetos Jugador
                return {nombre: Jugador.del_diccio(nombre, info) 
                        for nombre, info in datos.items()}
        return {}
    
    def guardar_jugadores(self, jugadores_dict):
        #Guarda todos los jugadores en archivo .json
        datos_json = {nombre: jugador.a_diccio() for nombre, jugador in jugadores_dict.items()}
        with open(self.ruta_archivo, 'w') as file:
            json.dump(datos_json, file, indent=4)
    
    def guardar_jugador_individual(self, jugador, nombre_archivo=None):
        #guarda un jugador por archivo
        if not nombre_archivo:
            nombre_archivo = f"{jugador.nombre}_backup.json"
        with open(nombre_archivo, 'w') as f:
            json.dump({jugador.nombre: jugador.a_diccio()}, f, indent=4)
    
    def cargar_jugador_individual(self, nombre_archivo):
        #Carga el jugador de x archivo
        with open(nombre_archivo, 'r') as f:
            datos = json.load(f)
            for nombre, info in datos.items():
                return Jugador.del_diccio(nombre, info)
        return None
    

#Clase para la sesión actual del juego, como para definir atacante/defensor y las facciones de cada uno
class Sesion:
    def __init__(self):    #En principio, todavía no se definen roles ni facciones para los jugadores
        self.jugador_atacante = None
        self.jugador_defensor = None
        self.faccion_atacante = None
        self.faccion_defensor = None
    
    #Este método convierte al jugador en atacante
    def establecer_atacante(self, jugador, faccion):
        self.jugador_atacante=jugador
        self.faccion_atacante=faccion
    
    #Este método convierte al jugador en defensor
    def establecer_defensor(self, jugador, faccion):
        self.jugador_defensor=jugador
        self.faccion_defensor=faccion
    
    #Este método verifica que ambos jugadores están listos: como verificar facciones diferentes o que existan ambos jugadores
    def validar_sesion(self):
        if not self.jugador_atacante or not self.jugador_defensor:
            return False, "Ambos jugadores deben iniciar sesión"
        if self.faccion_atacante == self.faccion_defensor:
            return False, "Deben elegir facciones diferentes"
        return True, "Sesión válida"
    
    #Reinicia la sesión
    def reset(self):
        self.jugador_atacante = None
        self.jugador_defensor = None
        self.faccion_atacante = None
        self.faccion_defensor = None


#Variables globales del programa

# Ruta del archivo de jugadores
gestor = Gestor_archivos("jugadores.json")

# Base de datos de jugadores
jugadores_db = gestor.cargar_jugadores()

sesion_actual = Sesion()

# Facciones disponibles
FACCIONES_DISPONIBLES = ["Medieval", "Futurista", "Naturaleza", "Oscura", "Robótica"]



'''
funciones globales, empleando las herramientas de las clases
'''

#Registra un jugador nuevo
def registrar_jugador_menu(nombre, contraseña, rol):
    global jugadores_db
    if not (nombre and contraseña):
        messagebox.showerror("ERROR", "Por favor complete todos los campos")
        return False
    if nombre in jugadores_db:
        messagebox.showerror("ERROR", f"El jugador '{nombre}' ya existe")
        return False
    # Crea el jugador usando la clase
    nuevo_jugador = Jugador(nombre, contraseña)
    jugadores_db[nombre] = nuevo_jugador
    gestor.guardar_jugadores(jugadores_db)
    messagebox.showinfo("ÉXITO", f"Jugador '{nombre}' registrado correctamente")
    mostrar_rankings()
    return True

#Permite iniciar la sesión de un jugador
def iniciar_sesion_menu(nombre, contraseña, rol):
    if not (nombre and contraseña):
        messagebox.showerror("ERROR", "Por favor complete todos los campos")
        return False
    if nombre not in jugadores_db:
        messagebox.showerror("ERROR", f"El jugador '{nombre}' no existe")
        return False
    jugador = jugadores_db[nombre]
    if jugador.contraseña != contraseña:
        messagebox.showerror("ERROR", "Contraseña incorrecta")
        return False
    messagebox.showinfo("ÉXITO", f"¡Bienvenido {nombre}!")
    # Establece en la sesión actual
    if rol == "atacante":
        sesion_actual.establecer_atacante(jugador, facción_atacante.get())
        sesion_atacante_activa.set(nombre)
    elif rol == "defensor":
        sesion_actual.establecer_defensor(jugador, facción_defensor.get())
        sesion_defensor_activa.set(nombre)
    return True

#Permite guardar a un jugador en un archivo .json
def guardar_jugador_archivo(jugador, rol):
    filepath = filedialog.asksaveasfilename(
        title=f"Guardar {rol.capitalize()}",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )
    if filepath:
        gestor.guardar_jugador_individual(jugador, filepath)
        messagebox.showinfo("GUARDADO", f"{rol.capitalize()} guardado correctamente")

#Permite cargar a un jugador desde su arhivo .json correspondiente
def cargar_jugador_archivo(rol):
    filepath = filedialog.askopenfilename(
        title=f"Seleccionar {rol.capitalize()}",
        filetypes=[("JSON files", "*.json")]
    )
    if filepath:
        try:
            jugador = gestor.cargar_jugador_individual(filepath)
            if rol == "atacante":
                nombre_atacante.set(jugador.nombre)
            else:
                nombre_defensor.set(jugador.nombre)
            messagebox.showinfo("CARGADO", f"{rol.capitalize()} cargado correctamente")
        except Exception as e:
            messagebox.showerror("ERROR", f"No se pudo cargar: {e}")


#Actualiza las victorias en el archivo general de los jugadores
def actualizar_victorias(nombre, rol):
    global jugadores_db
    jugadores_db = gestor.cargar_jugadores()
    if nombre in jugadores_db:
        jugador = jugadores_db[nombre]
        jugador.suma_victoria(rol) 
        gestor.guardar_jugadores(jugadores_db)


#Abre el mapa de Crear_mapa_BCS desde el menú
def Abrir_mapa_desde_menu():
    valida, mensaje = sesion_actual.validar_sesion()
    if not valida:
        messagebox.showerror("ERROR DE SESIÓN", mensaje)
        return
    import Crear_mapa_BCS
    Crear_mapa_BCS.Abrir_mapa(Menu,
                              sesion_actual.jugador_defensor.nombre,
                              sesion_actual.jugador_atacante.nombre,
                              sesion_actual.faccion_defensor,
                              sesion_actual.faccion_atacante)

#Muestra ambos rankings en la ventana
def mostrar_rankings():
    global jugadores_db
    jugadores_db = gestor.cargar_jugadores()
    info_text_atacante.delete("1.0", tk.END)
    info_text_defensor.delete("1.0", tk.END)
    # Ordena usando el método total_victorias de la clase
    atacantes_ordenados = sorted(jugadores_db.items(), key=lambda x: x[1].victorias_atacante, reverse=True)
    defensores_ordenados = sorted(jugadores_db.items(), key=lambda x: x[1].victorias_defensor, reverse=True)
    info_text_atacante.insert(tk.END, "POSICIÓN | JUGADOR | VICTORIAS\n" + "-"*40 + "\n")
    for pos, (nombre, jugador) in enumerate(atacantes_ordenados, 1):
        info_text_atacante.insert(tk.END, f"#{pos:2d}      | {nombre:15s} | {jugador.victorias_atacante:3d}\n")
    info_text_defensor.insert(tk.END, "POSICIÓN | JUGADOR | VICTORIAS\n" + "-"*40 + "\n")
    for pos, (nombre, jugador) in enumerate(defensores_ordenados, 1):
        info_text_defensor.insert(tk.END, f"#{pos:2d}      | {nombre:15s} | {jugador.victorias_defensor:3d}\n")



if __name__ == "__main__":
    Menu = tk.Tk()
    Menu.title("Menú Batalla Campal Sin-igual")
    Menu.geometry("1000x600")

    tk.Label(Menu, text="Batalla Campal Sin-igual >:D", font=("Times New Roman", 24, "bold"), bg="#DBD225").pack(pady=10, fill=tk.X)

    # Frame principal para distribuir atacante y defensor lado a lado
    frame_jugadores = tk.Frame(Menu, bg="white")
    frame_jugadores.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

    ''' Atacante '''
    frame_atacante = tk.Frame(frame_jugadores, bg="#CE1F1F", relief=tk.RAISED, bd=2, width=450)
    frame_atacante.pack(side=tk.LEFT, padx=5, pady=5, expand=False)

    tk.Label(frame_atacante, text="ATACANTE", font=("Times New Roman", 14, "bold"), bg="#CE1F1F").pack(pady=5)

    nombre_atacante = StringVar(value="")
    contraseña_a = StringVar(value="")
    facción_atacante = StringVar()
    sesion_atacante_activa = StringVar(value="")

    frame_faccion_a = tk.Frame(frame_atacante, bg="#EA2121")
    frame_faccion_a.pack(padx=5, pady=5)
    tk.Label(frame_faccion_a, text="Facción:", font=("Times New Roman", 11, "bold"), bg="#EA2121", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
    combo_faccion_a = ttk.Combobox(frame_faccion_a, textvariable=facción_atacante, values=FACCIONES_DISPONIBLES, state="readonly", width=23, font=("Times New Roman", 11))
    combo_faccion_a.pack(side=tk.LEFT, padx=5)
    combo_faccion_a.current(0)

    frame_nombre_a = tk.Frame(frame_atacante, bg="#EA2121")
    frame_nombre_a.pack(padx=5, pady=5)
    tk.Label(frame_nombre_a, text="Nombre:", font=("Times New Roman", 11, "bold"), bg="#EA2121", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
    entry_n_a = tk.Entry(frame_nombre_a, textvariable=nombre_atacante, font=("Times New Roman", 11, "bold"), width=25)
    entry_n_a.pack(side=tk.LEFT, padx=5)

    frame_contra_a = tk.Frame(frame_atacante, bg="#EA2121")
    frame_contra_a.pack(padx=5, pady=5)
    tk.Label(frame_contra_a, text="Contraseña:", font=("Times New Roman", 11, "bold"), bg="#EA2121", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
    entry_c_a = tk.Entry(frame_contra_a, textvariable=contraseña_a, font=("Times New Roman", 11), width=25, show="*")
    entry_c_a.pack(side=tk.LEFT, padx=5)

    ''' Defensor '''
    frame_defensor = tk.Frame(frame_jugadores, bg="#0b852b", relief=tk.RAISED, bd=2)
    frame_defensor.pack(side=tk.RIGHT, padx=5, pady=5, expand=False)

    tk.Label(frame_defensor, text="DEFENSOR", font=("Times New Roman", 14, "bold"), bg="#0b852b").pack(pady=5)

    nombre_defensor = StringVar(value="")
    contraseña_d = StringVar(value="")
    facción_defensor = StringVar()
    sesion_defensor_activa = StringVar(value="")

    frame_faccion_d = tk.Frame(frame_defensor, bg="#1cbd46")
    frame_faccion_d.pack(padx=5, pady=5)
    tk.Label(frame_faccion_d, text="Facción:", font=("Times New Roman", 11, "bold"), bg="#1cbd46", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
    combo_faccion_d = ttk.Combobox(frame_faccion_d, textvariable=facción_defensor, values=FACCIONES_DISPONIBLES, state="readonly", width=23, font=("Times New Roman", 11))
    combo_faccion_d.pack(side=tk.LEFT, padx=5)
    combo_faccion_d.current(1)

    frame_nombre_d = tk.Frame(frame_defensor, bg="#1cbd46")
    frame_nombre_d.pack(padx=5, pady=5)
    tk.Label(frame_nombre_d, text="Nombre:", font=("Times New Roman", 11, "bold"), bg="#1cbd46", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
    entry_n_d = tk.Entry(frame_nombre_d, textvariable=nombre_defensor, font=("Times New Roman", 11, "bold"), width=25)
    entry_n_d.pack(side=tk.LEFT, padx=5)

    frame_contra_d = tk.Frame(frame_defensor, bg="#1cbd46")
    frame_contra_d.pack(padx=5, pady=5)
    tk.Label(frame_contra_d, text="Contraseña:", font=("Times New Roman", 11, "bold"), bg="#1cbd46", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
    entry_c_d = tk.Entry(frame_contra_d, textvariable=contraseña_d, font=("Times New Roman", 11), width=25, show="*")
    entry_c_d.pack(side=tk.LEFT, padx=5)

    # Asignación de botones de acción

    # Botones atacante
    tk.Button(frame_botones_a := tk.Frame(frame_atacante, bg="#CE2222"), text="Registrarse", command=lambda: registrar_jugador_menu(nombre_atacante.get(), contraseña_a.get(), "atacante"), font=("Times New Roman", 10, "bold"), bg="#90EE90", width=12).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_botones_a, text="Inicio de Sesión", command=lambda: iniciar_sesion_menu(nombre_atacante.get(), contraseña_a.get(), "atacante"), font=("Times New Roman", 10, "bold"), bg="#87CEEB", width=12).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_botones_a, text="Guardar", command=lambda: guardar_jugador_archivo(jugadores_db.get(nombre_atacante.get()), "atacante"), font=("Times New Roman", 10, "bold"), bg="#FFD700", width=10).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_botones_a, text="Cargar", command=lambda: cargar_jugador_archivo("atacante"), font=("Times New Roman", 10, "bold"), bg="#FFA500", width=10).pack(side=tk.LEFT, padx=2)
    frame_botones_a.pack(pady=10)

    # Botones defensor
    tk.Button(frame_botones_d := tk.Frame(frame_defensor, bg="#075E0B"), text="Registrarse", command=lambda: registrar_jugador_menu(nombre_defensor.get(), contraseña_d.get(), "defensor"), font=("Times New Roman", 10, "bold"), bg="#90EE90", width=12).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_botones_d, text="Inicio de Sesión", command=lambda: iniciar_sesion_menu(nombre_defensor.get(), contraseña_d.get(), "defensor"), font=("Times New Roman", 10, "bold"), bg="#87CEEB", width=12).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_botones_d, text="Guardar", command=lambda: guardar_jugador_archivo(jugadores_db.get(nombre_defensor.get()), "defensor"), font=("Times New Roman", 10, "bold"), bg="#FFD700", width=10).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_botones_d, text="Cargar", command=lambda: cargar_jugador_archivo("defensor"), font=("Times New Roman", 10, "bold"), bg="#FFA500", width=10).pack(side=tk.LEFT, padx=2)
    frame_botones_d.pack(pady=10)

    # Rankings
    frame_rankings = tk.Frame(Menu, bg="#217AC2", relief=tk.SUNKEN, bd=2)
    frame_rankings.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    frame_ranking_atacante = tk.Frame(frame_rankings, bg="#EA2121", relief=tk.RAISED, bd=2)
    frame_ranking_atacante.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
    tk.Label(frame_ranking_atacante, text="RANKING ATACANTES", font=("Times New Roman", 12, "bold"), bg="#CE1F1F").pack(pady=5)
    info_text_atacante = tk.Text(frame_ranking_atacante, height=8, width=40, font=("Times New Roman", 9), bg="white")
    info_text_atacante.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    frame_ranking_defensor = tk.Frame(frame_rankings, bg="#1cbd46", relief=tk.RAISED, bd=2)
    frame_ranking_defensor.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)
    tk.Label(frame_ranking_defensor, text="RANKING DEFENSORES", font=("Times New Roman", 12, "bold"), bg="#0b852b").pack(pady=5)
    info_text_defensor = tk.Text(frame_ranking_defensor, height=8, width=40, font=("Times New Roman", 9), bg="white")
    info_text_defensor.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # Botones principales
    tk.Button(Menu, text="Actualizar Rankings", command=mostrar_rankings, font=("Times New Roman", 11, "bold"), bg="#C22BC2", width=30).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(Menu, text="Empezar el juego", command=Abrir_mapa_desde_menu, font=("Times New Roman", 11, "bold"), bg="#11DB9B", width=30).pack(side=tk.RIGHT, padx=10, pady=10)
    tk.Button(Menu, text="Salir", command=Menu.destroy, font=("Times New Roman", 12, "bold"), bg="#ce0a1a", width=15).pack(side=tk.BOTTOM, pady=10)
    
    mostrar_rankings()
    Menu.mainloop()
