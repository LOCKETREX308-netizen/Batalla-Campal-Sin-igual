import tkinter as tk
from tkinter import messagebox
import math
from PIL import Image, ImageTk

# Variables globales de configuración básica
TAM = 30   # Tamaño en píxeles de las celdas 
jugador_actual = "defensor"  

# Declaramos el diccionario vacío globalmente
SPRITES = {}

# Variables de Control de Partida (Estructura de Rondas)
ronda_actual = 1
rondas_defensor = 0
rondas_atacante = 0
danio_realizado_ronda = 0  

# Matriz lógica base
matriz = [[0]*15 for _ in range(15)]
matriz[7][2] = 1  # Base Central fija inicial

usuario_defensor_actual = "Defensor"
usuario_atacante_actual = "Atacante"
faccion_defensor_actual = "Medieval"
faccion_atacante_actual = "Futurista"


class EstructuraDefensiva:
        def __init__(self, id_tipo, fila, col):
                self.id_tipo = id_tipo
                self.fila = fila
                self.col = col
                self.x = col * TAM + TAM // 2
                self.y = fila * TAM + TAM // 2
                
                if id_tipo == 1:
                        self.nombre = "Base Central"; self.hp = 1500; self.vida_max = 1500; self.ataque = 0; self.rango = 0; self.recompensa = 500
                elif id_tipo == 2:
                        self.nombre = "Muro"; self.hp = 400; self.vida_max = 400; self.ataque = 0; self.rango = 0; self.recompensa = 25
                elif id_tipo == 3:
                        self.nombre = "Torre Básica"; self.hp = 200; self.vida_max = 200; self.ataque = 4; self.rango = 100; self.recompensa = 50
                elif id_tipo == 4:
                        self.nombre = "Torre Pesada"; self.hp = 350; self.vida_max = 350; self.ataque = 12; self.rango = 140; self.recompensa = 125
                elif id_tipo == 5:
                        self.nombre = "Torre Mágica"; self.hp = 180; self.vida_max = 180; self.ataque = 7; self.rango = 120; self.recompensa = 90

class TropaAtacante:
        def __init__(self, id_tipo, fila, col):
                self.id_tipo = id_tipo
                self.x = col * TAM + TAM // 2
                self.y = fila * TAM + TAM // 2
                
                if id_tipo == 6:
                        self.nombre = "Soldado Rápido"; self.hp = 100; self.vida_max = 100; self.velocidad = 3; self.ataque = 8; self.rango = 20; self.recompensa = 35  
                elif id_tipo == 7:
                        self.nombre = "Tanque Pesado"; self.hp = 450; self.vida_max = 450; self.velocidad = 1; self.ataque = 25; self.rango = 40; self.recompensa = 100
                elif id_tipo == 8:
                        self.nombre = "Unidad Médica"; self.hp = 90; self.vida_max = 90; self.velocidad = 2; self.ataque = -15; self.rango = 60; self.recompensa = 55
                elif id_tipo == 9:
                        self.nombre = "Asaltante"; self.hp = 140; self.vida_max = 140; self.velocidad = 2; self.ataque = 15; self.rango = 25; self.recompensa = 75

def puede_modificar(fila, col, jugador):
        if fila < 0 or fila >= len(matriz) or col < 0 or col >= len(matriz[0]): return False
        valor = matriz[fila][col]
        if valor == 1: return False
        if valor == 0: return True
        if jugador.lower() == "defensor" and valor in [2, 3, 4, 5]: return True
        if jugador.lower() == "atacante" and valor in [6, 7, 8, 9]: return True
        return False

# Función auxiliar encargada de rellenar el diccionario una vez que Tkinter esté listo
def cargar_sprites():
        global SPRITES
        if SPRITES: return # Si ya se cargaron una vez, no lo hace de nuevo
        
        ruta_sprites= {"Medieval_1": "Diseños/Medieval/Base_Central_M.png",
                        "Medieval_2": "Diseños/Medieval/Muro_M.png",
                        "Medieval_3": "Diseños/Medieval/Torre_Basica_M.png",
                        "Medieval_4": "Diseños/Medieval/Torre_Fuerte_M.png",
                        "Medieval_5": "Diseños/Medieval/Torre_Magica_M.png",
                        "Medieval_6": "Diseños/Medieval/Soldado_Rapido_M.png",
                        "Medieval_7": "Diseños/Medieval/Tanque_Pesado_M.png",
                        "Medieval_8": "Diseños/Medieval/Unidad_Medica_M.png",
                        "Medieval_9": "Diseños/Medieval/Asaltante_M.png",
                        
                        "Futurista_1": "Diseños/Futuristica/Base_Central_F.png",
                        "Futurista_2": "Diseños/Futuristica/Muro_F.png",
                        "Futurista_3": "Diseños/Futuristica/Torre_Basica_F.png",
                        "Futurista_4": "Diseños/Futuristica/Torre_Fuerte_F.png",
                        "Futurista_5": "Diseños/Futuristica/Torre_Magica_F.png",
                        "Futurista_6": "Diseños/Futuristica/Soldado_Rapido_F.png",
                        "Futurista_7": "Diseños/Futuristica/Tanque_Pesado_F.png",
                        "Futurista_8": "Diseños/Futuristica/Unidad_Medica_F.png",
                        "Futurista_9": "Diseños/Futuristica/Asaltante_F.png",
                        
                        "Naturaleza_1": "Diseños/Natural/Base_Central_N.png",
                        "Naturaleza_2": "Diseños/Natural/Muro_N.png",
                        "Naturaleza_3": "Diseños/Natural/Torre_Basica_N.png",
                        "Naturaleza_4": "Diseños/Natural/Torre_Fuerte_N.png",
                        "Naturaleza_5": "Diseños/Natural/Torre_Magica_N.png",
                        "Naturaleza_6": "Diseños/Natural/Soldado_Rapido_N.png",
                        "Naturaleza_7": "Diseños/Natural/Tanque_Pesado_N.png",
                        "Naturaleza_8": "Diseños/Natural/Unidad_Medica_N.png",
                        "Naturaleza_9": "Diseños/Natural/Asaltante_N.png",
                        
                        "Oscura_1": "Diseños/Oscuro/Base_Central_O.png",
                        "Oscura_2": "Diseños/Oscuro/Muro_O.png",
                        "Oscura_3": "Diseños/Oscuro/Torre_Basica_O.png",
                        "Oscura_4": "Diseños/Oscuro/Torre_Fuerte_O.png",
                        "Oscura_5": "Diseños/Oscuro/Torre_Magica_O.png",
                        "Oscura_6": "Diseños/Oscuro/Soldado_Rapido_O.png",
                        "Oscura_7": "Diseños/Oscuro/Tanque_Pesado_O.png",
                        "Oscura_8": "Diseños/Oscuro/Unidad_Medica_O.png",
                        "Oscura_9": "Diseños/Oscuro/Asaltante_O.png",
                        
                        "Robótica_1": "Diseños/Robotico/Base_Central_R.png",
                        "Robótica_2": "Diseños/Robotico/Muro_R.png",
                        "Robótica_3": "Diseños/Robotico/Torre_Basica_R.png",
                        "Robótica_4": "Diseños/Robotico/Torre_Fuerte_R.png",
                        "Robótica_5": "Diseños/Robotico/Torre_Magica_R.png",
                        "Robótica_6": "Diseños/Robotico/Soldado_Rapido_R.png",
                        "Robótica_7": "Diseños/Robotico/Tanque_Pesado_R.png",
                        "Robótica_8": "Diseños/Robotico/Unidad_Medica_R.png",
                        "Robótica_9": "Diseños/Robotico/Asaltante_R.png"}
        
        #este for permite ajustar el tamaño de las imágenes a cada cuadro del canvas
        for clave, ruta in ruta_sprites.items():
                try:
                        img_pil=Image.open(ruta)       #lo carga en pillow, y así modificarlo fácilmente
                        img_pil=img_pil.resize((TAM,TAM), Image.Resampling.LANCZOS)   #los ajusta
                        SPRITES[clave]=ImageTk.PhotoImage(img_pil)   #vuelve a subirlo a tkinter para que este los implemente
                except FileNotFoundError:
                        print(f"ERROR: No se encontró {ruta}")
                        SPRITES[clave]=None
                except Exception as e:
                        print(f"ERROR al cargar {clave}: {e}")
                        SPRITES[clave]=None

def Abrir_mapa(root, user_def, user_ata, fac_def, fac_ata):
        global matriz, TAM, jugador_actual, ronda_actual, rondas_defensor, rondas_atacante, danio_realizado_ronda
        global usuario_defensor_actual, usuario_atacante_actual, faccion_defensor_actual, faccion_atacante_actual
        
        usuario_defensor_actual = user_def
        usuario_atacante_actual = user_ata
        faccion_defensor_actual = fac_def
        faccion_atacante_actual = fac_ata
        
        ventana = tk.Toplevel(root)
        ventana.title("Campos de Batalla Campal Sin-igual")
        ventana.geometry("950x660")
        
        # Mandamos a llamar a la carga ahora que la ventana 'root' y 'ventana' existen
        cargar_sprites()
        
        tk.Label(ventana, text=f"Batalla: {faccion_defensor_actual} vs {faccion_atacante_actual}", font=("Times New Roman", 20, "bold"), bg="#DBD225").pack(fill="x")
        
        label_ronda_info = tk.Label(ventana, text=f"Ronda: {ronda_actual}   |   {usuario_defensor_actual}: {rondas_defensor}   |   {usuario_atacante_actual}: {rondas_atacante}", font=("Times New Roman", 12, "bold"), bg="#DBD225")
        label_ronda_info.pack(pady=2)

        canvas = tk.Canvas(ventana, width=len(matriz[0])*TAM, height=len(matriz)*TAM, bg="#34495E")
        canvas.place(x=40, y=115)
                
        lista_defensas = []
        lista_tropas = []
        en_combate = False  

        def resetear_y_cerrar():
                global matriz, ronda_actual, rondas_defensor, rondas_atacante, danio_realizado_ronda, jugador_actual
                nonlocal en_combate
                en_combate = False
                matriz = [[0]*15 for _ in range(15)]
                matriz[7][2] = 1 
                ronda_actual = 1; rondas_defensor = 0; rondas_atacante = 0; danio_realizado_ronda = 0; jugador_actual = "defensor"
                ventana.destroy()

        ventana.protocol("WM_DELETE_WINDOW", resetear_y_cerrar)

        def dibujar_mapa_editor():
                canvas.delete("all")
                for fila in range(len(matriz)):
                        for col in range(len(matriz[fila])):
                                x1, y1 = col * TAM, fila * TAM
                                x2, y2 = x1 + TAM, y1 + TAM
                                valor = matriz[fila][col]
                                if valor == 0: 
                                        canvas.create_rectangle(x1, y1, x2, y2, fill="#4b9416", outline="#2C3E50")
                                else:
                                        es_def = valor in [1, 2, 3, 4, 5]
                                        fac_llave = faccion_defensor_actual if es_def else faccion_atacante_actual
                                        clave_sprite = f"{fac_llave}_{valor}"
                                        img = SPRITES.get(clave_sprite)
                                        
                                        if img:
                                                #ahora la imagen que se ponga queda dentro del cuadro y centrado
                                                canvas.create_image(x1 + TAM//2, y1 + TAM//2, image=img)
                                        else:
                                                # Respaldo visual simple por si el archivo no existe
                                                color_back = "#7F8C8D" if es_def else "#E74C3C"
                                                canvas.create_rectangle(x1, y1, x2, y2, fill=color_back, outline="#2C3E50")

        def dibujar_combate_tiempo_real():
                canvas.delete("all")
                canvas.create_rectangle(0, 0, len(matriz[0])*TAM, len(matriz)*TAM, fill="#4b9416", outline="")
                
                for d in lista_defensas:
                        clave_sprite = f"{faccion_defensor_actual}_{d.id_tipo}"
                        img = SPRITES.get(clave_sprite)
                        
                        if img:
                                canvas.create_image(d.x, d.y, image=img)
                        else:
                                r = TAM // 2
                                canvas.create_rectangle(d.x - r, d.y - r, d.x + r, d.y + r, fill="#7F8C8D", outline="black")
                        
                        r_barra = TAM // 2
                        canvas.create_rectangle(d.x - r_barra, d.y - r_barra - 6, d.x + r_barra, d.y - r_barra - 2, fill="red")
                        ratio = max(0, d.hp / d.vida_max)
                        canvas.create_rectangle(d.x - r_barra, d.y - r_barra - 6, d.x - r_barra + (TAM * ratio), d.y - r_barra - 2, fill="green")
                        
                for t in lista_tropas:
                        clave_sprite = f"{faccion_atacante_actual}_{t.id_tipo}"
                        img = SPRITES.get(clave_sprite)
                        
                        if img:
                                canvas.create_image(t.x, t.y, image=img)
                        else:
                                r = TAM // 3
                                canvas.create_oval(t.x - r, t.y - r, t.x + r, t.y + r, fill="#E74C3C", outline="black")
                        
                        canvas.create_rectangle(t.x - TAM//2, t.y - (TAM//3) - 6, t.x + TAM//2, t.y - (TAM//3) - 2, fill="red")
                        ratio = max(0, t.hp / t.vida_max)
                        canvas.create_rectangle(t.x - TAM//2, t.y - (TAM//3) - 6, t.x - TAM//2 + (TAM * ratio), t.y - (TAM//3) - 2, fill="light green")

        oro_def_var = tk.IntVar(value=600)
        oro_ata_var = tk.IntVar(value=750)
        texto_oro_def = tk.StringVar(value=f"{usuario_defensor_actual} - Oro: ${oro_def_var.get()}")
        texto_oro_ata = tk.StringVar(value=f"{usuario_atacante_actual} - Oro: ${oro_ata_var.get()}")

        def actualizar_interfaz_oro():
                texto_oro_def.set(f"{usuario_defensor_actual} - Oro: ${oro_def_var.get()}")
                texto_oro_ata.set(f"{usuario_atacante_actual} - Oro: ${oro_ata_var.get()}")

        herramienta = tk.IntVar(value=2)
        label_turno = tk.Label(ventana, text=f"EDITANDO: {usuario_defensor_actual}", font=("Times New Roman", 12, "bold"), bg="#3AD80A", fg="black")
        label_turno.place(x=680, y=115)

        costos_defensa = {2: 50, 3: 100, 4: 250, 5: 180}
        costos_ataque = {6: 75, 7: 200, 8: 120, 9: 150}

        frame_tools = tk.Frame(ventana, bg="#3AD80A", relief=tk.GROOVE, bd=2)
        frame_tools.place(x=680, y=155, width=240)
        tk.Label(frame_tools, textvariable=texto_oro_def, font=("Times New Roman", 11, "bold"), bg="#3AD80A").pack(anchor="w", padx=5, pady=2)
        opciones_defe = {"Muro ($50)": 2, "Torre Básica ($100)": 3, "Torre Pesada ($250)": 4, "Torre Mágica ($180)": 5}
        for texto, valor in opciones_defe.items(): tk.Radiobutton(frame_tools, text=texto, variable=herramienta, value=valor, bg="#3AD80A").pack(anchor="w", padx=10)
                
        frame_tools_ata = tk.Frame(ventana, bg="#CE2222", relief=tk.GROOVE, bd=2)
        tk.Label(frame_tools_ata, textvariable=texto_oro_ata, font=("Times New Roman", 11, "bold"), bg="#CE2222", fg="white").pack(anchor="w", padx=5, pady=2)
        opciones_ata = {"Soldado Rápido ($75)": 6, "Tanque Pesado ($200)": 7, "Unidad Médica ($120)": 8, "Asaltante ($150)": 9}
        for texto, valor in opciones_ata.items(): tk.Radiobutton(frame_tools_ata, text=texto, variable=herramienta, value=valor, bg="#CE2222", fg="black", selectcolor="#CE2222").pack(anchor="w", padx=10)

        def editor_atacante():                  
                global jugador_actual
                if en_combate: return
                jugador_actual = "atacante"; herramienta.set(6) 
                label_turno.config(text=f"EDITANDO: {usuario_atacante_actual}", bg="#CE2222", fg="white")
                frame_tools.place_forget(); frame_tools_ata.place(x=680, y=155, width=240)  
                
        def editor_defensor():
                global jugador_actual
                if en_combate: return
                jugador_actual = "defensor"; herramienta.set(2)
                label_turno.config(text=f"EDITANDO: {usuario_defensor_actual}", bg="#3AD80A", fg="black")
                frame_tools_ata.place_forget(); frame_tools.place(x=680, y=155, width=240)  

        def bucle_combate():
                global ronda_actual, rondas_defensor, rondas_atacante, matriz, danio_realizado_ronda
                nonlocal en_combate 
                if not en_combate: return

                base_central = next((d for d in lista_defensas if d.id_tipo == 1), None)
                
                # para que cuando la base central sea destruida, automáticamente gana el atacante
                if base_central is None or base_central.hp <= 0:
                        en_combate = False
                        import Menu_principal_BCS
                        Menu_principal_BCS.actualizar_victorias(usuario_atacante_actual, "atacante")
                        messagebox.showinfo("FIN DE PARTIDA", f"💥 ¡LA BASE CENTRAL HA SIDO DESTRUIDA!\n👑 ¡{usuario_atacante_actual} ha ganado la partida completa! 👑")
                        resetear_y_cerrar()
                        return

                atacantes_activos = [t for t in lista_tropas if t.ataque > 0]
                
                # cuando la base del defensor logra sobrevivir (o sea se logró defender), entonces el defensor gana
                if len(lista_tropas) == 0 or len(atacantes_activos) == 0:
                        rondas_defensor += 1
                        if rondas_defensor == 3:
                                en_combate = False
                                import Menu_principal_BCS
                                Menu_principal_BCS.actualizar_victorias(usuario_defensor_actual, "defensor")
                                messagebox.showinfo("FIN DE PARTIDA", f"👑 ¡{usuario_defensor_actual} HA REPELIDO LAS 3 RONDAS Y GANADO EL JUEGO! 👑")
                                resetear_y_cerrar()
                        else:
                                finalizar_ronda_limpieza("¡Las defensas repelieron el ataque!")
                        return

                # Movimiento de Unidades Atacantes
                for t in lista_tropas:
                        if t.id_tipo == 8: 
                                aliados_en_rango = [a for a in lista_tropas if a != t and math.hypot(a.x - t.x, a.y - t.y) <= t.rango and a.hp < a.vida_max]
                                if aliados_en_rango:
                                        target = min(aliados_en_rango, key=lambda x: x.hp)
                                        target.hp = min(target.hp + 2, target.vida_max)
                                if atacantes_activos: objetivo_mov = min(atacantes_activos, key=lambda a: math.hypot(a.x - t.x, a.y - t.y))
                                elif lista_defensas: objetivo_mov = min(lista_defensas, key=lambda d: math.hypot(d.x - t.x, d.y - t.y))
                                else: objetivo_mov = None

                                if objetivo_mov:
                                        dist = math.hypot(objetivo_mov.x - t.x, objetivo_mov.y - t.y)
                                        if dist > 25:
                                                dx, dy = objetivo_mov.x - t.x, objetivo_mov.y - t.y
                                                angle = math.atan2(dy, dx)
                                                t.x += math.cos(angle) * t.velocidad; t.y += math.sin(angle) * t.velocidad
                                continue 
                        
                        if lista_defensas:
                                objetivo = min(lista_defensas, key=lambda d: math.hypot(d.x - t.x, d.y - t.y))
                                dist = math.hypot(objetivo.x - t.x, objetivo.y - t.y)
                                if dist <= t.rango:
                                        objetivo.hp -= t.ataque; danio_realizado_ronda += t.ataque 
                                        oro_ata_var.set(oro_ata_var.get() + 2) 
                                        if objetivo.hp <= 0:
                                                oro_ata_var.set(oro_ata_var.get() + objetivo.recompensa); lista_defensas.remove(objetivo)
                                        actualizar_interfaz_oro()
                                else:
                                        dx, dy = objetivo.x - t.x, objetivo.y - t.y; angle = math.atan2(dy, dx)
                                        t.x += math.cos(angle) * t.velocidad; t.y += math.sin(angle) * t.velocidad

                # Ataque de Torres Defensivas
                for d in lista_defensas:
                        if d.ataque > 0 and lista_tropas:
                                en_rango = [t for t in lista_tropas if math.hypot(t.x - d.x, t.y - d.y) <= d.rango]
                                if en_rango:
                                        target_tropa = min(en_rango, key=lambda t: math.hypot(t.x - d.x, t.y - d.y))
                                        target_tropa.hp -= d.ataque
                                        if target_tropa.hp <= 0:
                                                oro_def_var.set(oro_def_var.get() + target_tropa.recompensa); actualizar_interfaz_oro(); lista_tropas.remove(target_tropa)

                dibujar_combate_tiempo_real()
                ventana.after(33, bucle_combate)

        def iniciar_fase_combate():
                nonlocal en_combate, lista_defensas, lista_tropas
                if en_combate: return
                lista_defensas.clear(); lista_tropas.clear()
                for f in range(len(matriz)):
                        for c in range(len(matriz[f])):
                                val = matriz[f][c]
                                if val in [1, 2, 3, 4, 5]: lista_defensas.append(EstructuraDefensiva(val, f, c))
                                elif val in [6, 7, 8, 9]: lista_tropas.append(TropaAtacante(val, f, c))
                if not lista_tropas:
                        messagebox.showwarning("SIN TROPAS", "El Atacante debe desplegar tropas primero.")
                        return
                en_combate = True; btn_jugar.config(state="disabled"); bucle_combate()

        def finalizar_ronda_limpieza(mensaje_resultado):
                global ronda_actual, rondas_defensor, rondas_atacante, matriz, danio_realizado_ronda
                nonlocal en_combate
                en_combate = False
                messagebox.showinfo("RESULTADO DE LA RONDA", f"Ronda {ronda_actual} Finalizada.\n{mensaje_resultado}")
                ronda_actual += 1
                label_ronda_info.config(text=f"Ronda: {ronda_actual}   |   {usuario_defensor_actual}: {rondas_defensor}   |   {usuario_atacante_actual}: {rondas_atacante}")
                matriz = [[0]*15 for _ in range(15)]
                for d in lista_defensas: matriz[d.fila][d.col] = d.id_tipo  
                oro_def_var.set(oro_def_var.get() + 300)
                oro_ata_var.set(oro_ata_var.get() + 300 + int(danio_realizado_ronda * 0.25))
                danio_realizado_ronda = 0; actualizar_interfaz_oro()
                btn_jugar.config(state="normal"); editor_defensor(); dibujar_mapa_editor()

        def click_mapa(event):          
                global matriz, jugador_actual
                if en_combate: return
                col, fila = event.x // TAM, event.y // TAM
                if fila < len(matriz) and col < len(matriz[0]):
                        if not puede_modificar(fila, col, jugador_actual):
                                messagebox.showwarning("ERROR", "No puedes modificar esta casilla."); return 
                        if matriz[fila][col] != 0: return
                        id_herramienta = herramienta.get()
                        if jugador_actual == "defensor":
                                costo = costos_defensa.get(id_herramienta, 0)
                                if oro_def_var.get() >= costo: oro_def_var.set(oro_def_var.get() - costo); matriz[fila][col] = id_herramienta; actualizar_interfaz_oro()
                        elif jugador_actual == "atacante":
                                costo = costos_ataque.get(id_herramienta, 0)
                                if oro_ata_var.get() >= costo: oro_ata_var.set(oro_ata_var.get() - costo); matriz[fila][col] = id_herramienta; actualizar_interfaz_oro()
                        dibujar_mapa_editor()
                
        def click_derecho(event):         
                global matriz, jugador_actual
                if en_combate: return
                col, fila = event.x // TAM, event.y // TAM
                if fila < len(matriz) and col < len(matriz[0]):
                        if not puede_modificar(fila, col, jugador_actual): return 
                        valor_actual = matriz[fila][col]
                        if valor_actual == 0: return
                        if jugador_actual == "defensor" and valor_actual in costos_defensa: oro_def_var.set(oro_def_var.get() + costos_defensa[valor_actual]) 
                        elif jugador_actual == "atacante" and valor_actual in costos_ataque: oro_ata_var.set(oro_ata_var.get() + costos_ataque[valor_actual])
                        matriz[fila][col] = 0; actualizar_interfaz_oro(); dibujar_mapa_editor()

        tk.Button(ventana, text=f"Editor {usuario_defensor_actual}", command=editor_defensor, font=("Times New Roman", 11, "bold"), bg="#3AD80A").place(x=680, y=50, width=115)
        tk.Button(ventana, text=f"Editor {usuario_atacante_actual}", command=editor_atacante, font=("Times New Roman", 11, "bold"), bg="#CE2222", fg="white").place(x=805, y=50, width=115)
        btn_jugar = tk.Button(ventana, text="⚔️ ¡Iniciar Batalla! ⚔️", command=iniciar_fase_combate, font=("Times New Roman", 13, "bold"), bg="#de3125", fg="white")
        btn_jugar.place(x=680, y=415, width=240)

        canvas.bind("<Button-1>", click_mapa); canvas.bind("<Button-3>", click_derecho)    
        dibujar_mapa_editor()
        tk.Button(ventana, text="Salir", command=resetear_y_cerrar, font=("Times New Roman", 12, "bold"), bg="#ce0a1a").place(x=740, y=520, width=120)
        ventana.mainloop()
