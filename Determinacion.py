import pygame
import math
import random
import os

pygame.init()
pygame.mixer.init()

X = 800
Y = 600
pantalla = pygame.display.set_mode((X, Y))
pygame.display.set_caption("The Strongest in History")
reloj = pygame.time.Clock()
FPS = 30

TEXTO_DIALOGO_BOSS = "Preparate para Morir!"
TEXTO_MISS         = "MISS"
TEXTO_MENU_PAGINA  = "MISS"
SIGNO = "!"

pygame.mixer.music.load("DBG.mp3")

alma = pygame.image.load("Undertale_Red_SOUL.webp")
alma_img = pygame.transform.scale(alma, (20, 20))
anatomia = pygame.image.load("anatomia.png")
anatomia_img = pygame.transform.scale(anatomia,(300,300)).convert_alpha()
tiempo_turno_jefe = 0

alto_hueco = 16

frame_1 = pygame.transform.scale(pygame.image.load("pixil-frame-1.png").convert_alpha(), (140, 140))
frame_2 = pygame.transform.scale(pygame.image.load("pixil-frame-2.png").convert_alpha(), (140, 140))
frame_3 = pygame.transform.scale(pygame.image.load("pixil-frame-3.png").convert_alpha(), (140, 140))
frame_4 = pygame.transform.scale(pygame.image.load("pixil-frame-4.png").convert_alpha(), (140, 140))
frame_5 = pygame.transform.scale(pygame.image.load("pixil-frame-5.png").convert_alpha(), (140, 140))
frame_6 = pygame.transform.scale(pygame.image.load("pixil-frame-6.png").convert_alpha(), (140, 140))
frame_7 = pygame.transform.scale(pygame.image.load("pixil-frame-7.png").convert_alpha(), (140, 140))
frame_8 = pygame.transform.scale(pygame.image.load("pixil-frame-8.png").convert_alpha(), (140, 140))
frame_9 = pygame.transform.scale(pygame.image.load("pixil-frame-9.png").convert_alpha(), (140, 140))

sprite_actual_boss = frame_6

activo_atacar = False

ANCHO_BARRA_ATAQUE = 680
ALTO_BARRA_ATAQUE  = 140

hp_player = 40

hp_boss_cabeza = 550
hp_boss_pecho = 500
hp_brazoIz_sup = 125
hp_brazoDe_sup = 125
hp_brazoIz_inf = 120
hp_brazoDe_inf = 120
hp_pierna_izquierda = 120
hp_pierna_derecha = 120

balas = []

p_hight = 400
p_width = 100

rectangulo0 = pygame.Rect(40,90, 40, 90)
p = pygame.Rect(180,60,p_width, p_hight)
p_right = pygame.Rect(360,60, p_width, p_hight)
p_y = pygame.Rect(300,30,100,400)

shrine = p_width + p_hight
ola = pygame.Rect(200,50,100,400)

partes_boss = [
    ("Cabeza", lambda: hp_boss_cabeza, lambda v: globals().update(hp_boss_cabeza=max(0, hp_boss_cabeza - v))),
    ("Pecho", lambda: hp_boss_pecho, lambda v: globals().update(hp_boss_pecho=max(0, hp_boss_pecho - v))),
    ("Brazo Izq Sup", lambda: hp_brazoIz_sup, lambda v: globals().update(hp_brazoIz_sup=max(0, hp_brazoIz_sup - v))),
    ("Brazo Der Sup", lambda: hp_brazoDe_sup, lambda v: globals().update(hp_brazoDe_sup=max(0, hp_brazoDe_sup - v))),
    ("Brazo Izq Inf", lambda: hp_brazoIz_inf, lambda v: globals().update(hp_brazoIz_inf=max(0, hp_brazoIz_inf - v))),
    ("Brazo Der Inf", lambda: hp_brazoDe_inf, lambda v: globals().update(hp_brazoDe_inf=max(0, hp_brazoDe_inf - v))),
    ("Pierna Izquierda", lambda: hp_pierna_izquierda, lambda v: globals().update(hp_pierna_izquierda=max(0, hp_pierna_izquierda - v))),
    ("Pierna Derecha", lambda: hp_pierna_derecha, lambda v: globals().update(hp_pierna_derecha=max(0, hp_pierna_derecha - v)))
]
opcion_parte = 0

damage_boss = 10
damage_Boss = True

tiempo_temblor = 0
duracion_temblor = 200
turno_actual = 1
es_turno_del_jefe = False

ruta_fuente = os.path.expanduser("~/.local/share/fonts/determinationmonoweb-webfont.ttf")
if not os.path.exists(ruta_fuente):
    ruta_fuente = "determinationmonoweb-webfont.ttf"

F  = pygame.font.Font(ruta_fuente, 170)   
F2 = pygame.font.Font(ruta_fuente, 50)  
F3 = pygame.font.Font(ruta_fuente, 50)  
F4 = pygame.font.Font(ruta_fuente, 25)  
HP = pygame.font.Font(ruta_fuente, 25)  
F5 = pygame.font.Font(ruta_fuente, 45)

negro       = (0, 0, 0)
blanco      = (255, 255, 255)
gris        = (120, 120, 120)
gris_oscuro = (40, 40, 40)
amarillo    = (255, 255, 0)
naranja     = (255, 165, 0)
rojo        = (255, 0, 0)
verde       = (0, 200, 0)

activo = True
escena = "menu"  
mensaje = True
advertencia = True
tiempo_inicio = 0

barra_x = (X - ANCHO_BARRA_ATAQUE) // 2  
barra_y = 220
cursor_ataque_x = barra_x
velocidade_cursor = 16
direccion_cursor = 1
resultado_golpe = None
tiempo_resultado = 0

proyectiles = []
movimiento_permitido = False

hitbox = pygame.Rect(180, 230, 440, 120)
borde_X, borde_Y = 392, 275
tamano = 15
V = 4

opcion_menu = 0

rect_fight = pygame.Rect(90, 450, 150, 50)
rect_act   = pygame.Rect(250, 450, 150, 50)
rect_item  = pygame.Rect(410, 450, 150, 50)
rect_mercy = pygame.Rect(569, 450, 150, 50)

signo_exclamacion = pygame.font.Font(ruta_fuente, 25) 
texto = F.render(TEXTO_MENU_PAGINA, True, blanco)
super_btn = F2.render("Fight", True, blanco)
recta = super_btn.get_rect(topleft=(350, 200))
super2_btn = F3.render("Quit", True, blanco)
recta2 = super2_btn.get_rect(topleft=(350, 250)) 
texto_boss = F4.render(TEXTO_DIALOGO_BOSS, True, blanco)
signo = signo_exclamacion.render(SIGNO, True, amarillo)

while activo:
    pos_mouse = pygame.mouse.get_pos()
    teclas = pygame.key.get_pressed()
    tiempo_actual = pygame.time.get_ticks()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            activo = False
        elif evento.type == pygame.KEYDOWN:
            if escena == "combate" and not es_turno_del_jefe:
                if evento.key == pygame.K_LEFT:
                    opcion_menu = (opcion_menu - 1) % 4
                elif evento.key == pygame.K_RIGHT:
                    opcion_menu = (opcion_menu + 1) % 4
                elif evento.key == pygame.K_SPACE:
                    if opcion_menu == 0:  
                        escena = "seleccionar_parte"

            elif escena == "seleccionar_parte":
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    opcion_parte = (opcion_parte - 1) % len(partes_boss)
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    opcion_parte = (opcion_parte + 1) % len(partes_boss)
                elif evento.key == pygame.K_SPACE:
                    escena = "ataque"
                    cursor_ataque_x = barra_x
                    direccion_cursor = 1
                    resultado_golpe = None

            elif escena == "ataque":
                if evento.key == pygame.K_SPACE and resultado_golpe is None:
                    centro_barra = barra_x + (ANCHO_BARRA_ATAQUE // 2)
                    distancia_al_centro = abs(cursor_ataque_x - centro_barra)
                    
                    ancho_rojo = ANCHO_BARRA_ATAQUE * 0.2      
                    ancho_amarillo = ANCHO_BARRA_ATAQUE * 0.35  
                    
                    if distancia_al_centro < (ancho_rojo / 2):
                        resultado_golpe = "-15"
                        partes_boss[opcion_parte][2](15)
                    elif distancia_al_centro < (ancho_amarillo / 2):
                        resultado_golpe = "-10"
                        partes_boss[opcion_parte][2](10)
                    elif distancia_al_centro < (ANCHO_BARRA_ATAQUE / 2):
                        resultado_golpe = "-5"
                        partes_boss[opcion_parte][2](5)
                    else:
                        resultado_golpe = "MISS"
                    
                    tiempo_resultado = pygame.time.get_ticks()
                    tiempo_temblor = pygame.time.get_ticks()
                    
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if escena == "menu":
                    if recta.collidepoint(evento.pos):
                        escena = "combate" 
                        pygame.mixer.music.play(-1)
                        tiempo_inicio = pygame.time.get_ticks()  
                        proyectiles.clear()
                    elif recta2.collidepoint(evento.pos):
                        activo = False 
                
                elif escena == "combate" and not es_turno_del_jefe:
                    if rect_fight.collidepoint(evento.pos):
                        escena = "seleccionar_parte"

    NX = borde_X
    NY = borde_Y

    if escena == "combate" and movimiento_permitido:
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            NX -= V
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            NX += V
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            NY += V
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            NY -= V
    
    if escena == "menu": 
        pantalla.fill(negro)
        if recta.collidepoint(pos_mouse):
            super_btn = F2.render("Fight", True, gris)
        else:
            super_btn = F2.render("Fight", True, blanco)

        if recta2.collidepoint(pos_mouse):
            super2_btn = F3.render("Quit", True, gris)
        else:
            super2_btn = F3.render("Quit", True, blanco)

        pantalla.blit(texto, (230, 40))
        pantalla.blit(super_btn, (350, 200))
        pantalla.blit(super2_btn, (350, 250))

    elif escena == "seleccionar_parte":
        pantalla.fill(negro)
        espacio_imagen_rect = pygame.Rect(450, 100, 300, 350)
        pygame.draw.rect(pantalla, gris_oscuro, espacio_imagen_rect)
        pygame.draw.rect(pantalla, blanco, espacio_imagen_rect, 2)
        
        titulo_sel = F4.render("SELECCIONA UNA PARTE (W/S y SPACE):", True, amarillo)
        pantalla.blit(titulo_sel, (50, 40))
        pantalla.blit(anatomia_img, (454, 110))

        for i, (nombre, func_get_hp, _) in enumerate(partes_boss):
            color_texto = amarillo if i == opcion_parte else blanco
            texto_parte = HP.render(f"> {nombre}: {func_get_hp()} HP" if i == opcion_parte else f"  {nombre}: {func_get_hp()} HP", True, color_texto)
            pantalla.blit(texto_parte, (60, 90 + (i * 40)))

    elif escena == "ataque":
        pantalla.fill(negro)
        
        offset_respiracion = math.sin(tiempo_actual * 0.005) * 3
        pos_sukuna_x = 330
        pos_sukuna_y = int(70 + offset_respiracion)
        
        if tiempo_actual - tiempo_temblor < duracion_temblor:
            pos_sukuna_x += random.randint(-4, 4)

        pantalla.blit(sprite_actual_boss, (pos_sukuna_x, pos_sukuna_y))
        
        centro_barra_x = barra_x + (ANCHO_BARRA_ATAQUE // 2)
        pygame.draw.rect(pantalla, verde, (barra_x, barra_y, ANCHO_BARRA_ATAQUE, ALTO_BARRA_ATAQUE))
        
        ancho_amarillo = ANCHO_BARRA_ATAQUE * 0.35
        pygame.draw.rect(pantalla, amarillo, (centro_barra_x - (ancho_amarillo // 2), barra_y, ancho_amarillo, ALTO_BARRA_ATAQUE))
        
        ancho_rojo = ANCHO_BARRA_ATAQUE * 0.10
        pygame.draw.rect(pantalla, rojo, (centro_barra_x - (ancho_rojo // 2), barra_y, ancho_rojo, ALTO_BARRA_ATAQUE))
        
        pygame.draw.rect(pantalla, blanco, (barra_x, barra_y, ANCHO_BARRA_ATAQUE, ALTO_BARRA_ATAQUE), 3)
        
        if resultado_golpe is None:
            cursor_ataque_x += velocidade_cursor * direccion_cursor
            if cursor_ataque_x >= barra_x + ANCHO_BARRA_ATAQUE - 5 or cursor_ataque_x <= barra_x:
                direccion_cursor *= -1
        
        pygame.draw.line(pantalla, blanco, (cursor_ataque_x, barra_y - 8), (cursor_ataque_x, barra_y + ALTO_BARRA_ATAQUE + 8), 6)

        if resultado_golpe is not None:
            texto_res = F5.render(resultado_golpe, True, blanco)
            rect_texto = texto_res.get_rect(center=(X // 2, barra_y - 35))
            pantalla.blit(texto_res, rect_texto)
            
            if pygame.time.get_ticks() - tiempo_resultado > 1000:
                resultado_golpe = None
                escena = "combate"
                movimiento_permitido = True
                turno_actual += 1
                es_turno_del_jefe = (turno_actual % 2 == 0)

    elif escena == "combate":
        pantalla.fill(negro) 
        texto_hp_jugador = F4.render(f"HP: {hp_player}", True, blanco)
        
        if turno_actual > 20:
            texto_turno = F4.render("Turno: Last Breath (Jefe)", True, rojo)
            texto_hp_boss = F4.render("Sukuna: ...", True, rojo)
        else:
            quien_turno = "Jefe" if es_turno_del_jefe else "Player"
            texto_turno = F4.render(f"Turno {turno_actual}/20 - [{quien_turno}]", True, amarillo if es_turno_del_jefe else blanco)
            texto_hp_boss = F4.render(f"Pecho HP: {hp_boss_pecho}", True, blanco)
        
        if mensaje and (pygame.time.get_ticks() - tiempo_inicio > 3500):
            mensaje = False  

        if mensaje:
            pantalla.blit(texto_boss, (460, 20))               
        
        pygame.draw.rect(pantalla, blanco, hitbox, 5) 
        pantalla.blit(texto_hp_jugador, (185, 360))
        pantalla.blit(texto_hp_boss, (185, 390))
        pantalla.blit(texto_turno, (185, 420))
        
        cuadrado2 = pygame.Rect(NX, NY, tamano, tamano)
        if hitbox.contains(cuadrado2):
            borde_X = NX
            borde_Y = NY

        # --- LÓGICA AVANZADA DE LOS CORTES DE EL BOSS(TURNO 2) ---
        if es_turno_del_jefe:
            if "tiempo_turno_jefe" not in globals() or tiempo_turno_jefe == 0:
                globals()["tiempo_turno_jefe"] = pygame.time.get_ticks()
                balas.clear()
                
            pos_hueco_y = random.randint(240, 290)

            tiempo_transcurrido = pygame.time.get_ticks() - globals()["tiempo_turno_jefe"]

            if 500 < tiempo_transcurrido < 2500 and random.randint(1, 25) == 1:
                corte_horizontal = {"rect": pygame.Rect(620, random.randint(260, 310), 80, 8), "tipo": "izquierda", "vel": 6}
                balas.append(corte_horizontal)



            if 700 < tiempo_transcurrido == activo_atacar == True:

             pygame.draw.rect(pantalla,blanco,ola, 90)    

             if advertencia:
                    pantalla.blit(signo, (270, 60))

            
            elif 3000 < tiempo_transcurrido < 5500 and random.randint(1, 40) == 1:
                            hueco_seguro = random.randint(200, 520)
                            for x_pos in range(190, 610, 50):
                                if abs(x_pos - hueco_seguro) > 35:
                                    corte_techo = {"rect": pygame.Rect(x_pos, 235, 35, 6), "tipo": "abajo", "vel": 2}
                                    balas.append(corte_techo) 
            
            if 1000 < tiempo_transcurrido < 2000 and random.randint(1, 30) == 1:
                nueva_advertencia = {
                    "rect": pygame.Rect(180, random.randint(240, 310), 440, 16),
                    "tipo": "advertencia_sans",
                    "tiempo_creacion": pygame.time.get_ticks()  
                }
                balas.append(nueva_advertencia)                        

            elif 6000 < tiempo_transcurrido < 8500 and random.randint(1, 50) == 1:
                corte_seguidor = {"rect": pygame.Rect(random.randint(200, 580), 240, 12, 12), "tipo": "perseguidor", "vel": 2}
                balas.append(corte_seguidor)

            if tiempo_transcurrido > 9000:
                globals()["tiempo_turno_jefe"] = 0
                es_turno_del_jefe = False
                turno_actual = 3
                balas.clear()

        for b in balas[:]:
            
            p = b["rect"]
            
            if b["tipo"] == "izquierda":
                p.x -= b["vel"]
            elif b["tipo"] == "abajo":
                p.y += b["vel"]
            elif b["tipo"] == "perseguidor":
                if p.x < cuadrado2.x: p.x += b["vel"]
                if p.x > cuadrado2.x: p.x -= b["vel"]
                if p.y < cuadrado2.y: p.y += b["vel"]
                if p.y > cuadrado2.y: p.y -= b["vel"]

            elif b["tipo"] == "advertencia_sans":
             tiempo_vida = pygame.time.get_ticks() - b["tiempo_creacion"]
                
            if tiempo_vida < 500:
                    #
                    pygame.draw.rect(pantalla, (100, 0, 0), p)
                    pantalla.blit(signo, (p.x + 20, p.y - 4))
                    continue 
            elif tiempo_vida < 1200:
                   
                    pygame.draw.rect(pantalla, blanco, p)
            else:
                    balas.remove(b)
                    continue
            
            if cuadrado2.colliderect(p):
                if damage_Boss:
                    hp_player -= 10
                balas.remove(b)
            elif not hitbox.contains(p) and b["tipo"] != "izquierda":
                balas.remove(b)
            elif p.x < 170:
                balas.remove(b)
            
        for p in proyectiles:
            p["rect"].y += p["vel_y"] 
            pygame.draw.arc(pantalla, blanco, p["rect"], 0, 3.9, 9)
             
            if cuadrado2.colliderect(p["rect"]):
                if damage_Boss == True:
                    hp_player -= 10
              
        if not es_turno_del_jefe:
            Q = F5.render("FIGHT", True, blanco)
            W = F5.render("ACT", True, blanco)
            E = F5.render("ITEM", True, blanco)
            R = F5.render("MERCY", True, blanco)
                
            pygame.draw.rect(pantalla, naranja, rect_fight, 2)
            pygame.draw.rect(pantalla, naranja, rect_act, 2)
            pygame.draw.rect(pantalla, naranja, rect_item, 2)
            pygame.draw.rect(pantalla, naranja, rect_mercy, 2)
            
            pantalla.blit(Q, (123, 450))
            pantalla.blit(W, (310, 450))
            pantalla.blit(E, (450, 450))
            pantalla.blit(R, (580, 450))
        
        pantalla.blit(alma_img, (borde_X, borde_Y))
        
        offset_respiracion_combate = math.sin(tiempo_actual * 0.005) * 3
        pantalla.blit(sprite_actual_boss, (330, int(80 + offset_respiracion_combate)))

    reloj.tick(FPS)
    pygame.display.flip()        

pygame.quit()