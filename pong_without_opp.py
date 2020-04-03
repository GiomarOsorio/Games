#importando la libreria pygame
import pygame
import random

#inicio de parametros de pygame y ventana
def IniciarVentana(ancho,alto):
	#incio de pygame
	pygame.init()
	
	#definiendo tamaño de ventana
	t_ventana = [ancho,alto]
	
	#retornando ventana y reloj
	return pygame.display.set_mode(t_ventana), pygame.time.Clock()
	

def DibujarSuperficieDelCampo(superficie):
	#rectangulo exterior
	lado_a = pygame.draw.line(superficie,(255,255,255), (30,30), (570,30),4)
	lado_b = pygame.draw.line(superficie,(255,255,255), (570,270), (570,30),4)
	lado_c = pygame.draw.line(superficie,(255,255,255), (30,270), (570,270),4)
	lado_d = pygame.draw.line(superficie,(255,255,255), (30,30), (30,270),4)
	
	#linea de visión de lados
	dlados = [pygame.draw.line(superficie,(0,0,0), (300,33), (300,268),1), False]
	DibujarDivisionDeLados(superficie)
	
	#retornado lados y division de lados
	return lado_a, lado_b, lado_c, lado_d, dlados


def DibujarDivisionDeLados(superficie):
	#división de lados
	for i in range(0,24):
		pygame.draw.line(superficie, (255,255,255), (298,31+(10*i)),(298,38+(10*i)), 1)
		
		
def IniciarJugadores(campo, color_jugador1, color_jugador2):
	#posición inicial de jugadores
	pos_Y = int(campo.get_size()[1]/2) - 25
	
	#creando variables del jugador1
	puntos_jugador1 = 0
	aceleracion1 = 0
	direccion1 = True
	movimiento1 = [aceleracion1, direccion1]
	jugador1 = pygame.draw.rect(campo, color_jugador1, [33,pos_Y,15,50], 0)
	
	#creando variables del jugador2	
	puntos_jugador2 = 0
	aceleracion2 = 0
	direccion2 = True
	movimiento2 = [aceleracion2,direccion2]
	jugador2 = pygame.draw.rect(campo, color_jugador2, [554 ,pos_Y,15,50], 0)

	#creando anotaciones
	Anotacion(campo, [1, jugador1, puntos_jugador1, color_jugador1, movimiento1])
	Anotacion(campo, [2, jugador2, puntos_jugador2, color_jugador2, movimiento2])
	
	#retornado jugador1 y jugador2
	return [1, jugador1, puntos_jugador1, color_jugador1, movimiento1], [2, jugador2, puntos_jugador2, color_jugador2, movimiento2]



def Anotacion(campo, jugador):
	#seleccionando fuente y valor de anotación
	fuente = pygame.font.Font('freesansbold.ttf', 24)
	texto = fuente.render(str(jugador[2]), True, jugador[3])
	
	#posición del texto en pantalla
	posicion = texto.get_rect()
	posicion.center = (165,14) if jugador[0] == 1 else (435,14)
	
	#borrado y dibujo de texto en pantalla
	campo.fill((0,0,0), posicion)
	campo.blit(texto, posicion)


def MoverJugador(campo, jugador, mov):
	#borrando rectangulo de jugador
	campo.fill((0,0,0), jugador[1])
	
	#determinando desplazamiento maximo superior e inferior
	if jugador[4][1]:
		desplazamiento = (219-int(jugador[1].y)) if (jugador[1].y + mov)>219 else (mov)
	elif not jugador[4][1]:
		desplazamiento = (33-int(jugador[1].y)) if (jugador[1].y - mov) < 33 else (-mov)
	
	#desplazando jugador a nueva posición
	jugador[1].move_ip(0,desplazamiento)
	
	#redibujando jugador		
	pygame.draw.rect(campo, jugador[3], jugador[1])

	#retornando jugador
	return jugador


def CrearPelota(campo,pos_pelota):
	direccion = 2
	direccion_xy = (1,-1) if pos_pelota == 1 else (-1,-1)
	aceleracion = 1
	color = (255,0,0)
	movimiento = False
	pelota = pygame.draw.rect(campo,color, [49,144,12,12], 0) if pos_pelota == 1 else pygame.draw.rect(campo,color, [542,144,12,12], 0)
	return [pelota, movimiento, direccion, direccion_xy, aceleracion, color]


def MoverPelota(pelota,campo):
	#posibles movimientos de la pelota
	movimientos = {
		1: (0,-1), #arriba
		2: (1,-1), #arriba, derecha
		3: (1,0), #derecha
		4: (1,1), #abajo, derecha
		5: (0,1), #abajo
		6: (-1,1), #izquierda, abajo
		7: (-1,0), #izquierda
		8: (-1,-1) #izquierda, arriba
	}
	
	#verificando si el movimiento de la pelota se encuentra dentro del diccionario "movimientos".
	if pelota[1] in movimientos.keys():
		#borrando pelota
		campo.fill((0,0,0), pelota[0])
		
		#cambiando movimiento de pelota
		pelota[3] = (movimientos[pelota[2]][0]*pelota[4], movimientos[pelota[2]][1]*pelota[4])
		#desplazando pelota
		pelota[0].move_ip(pelota[3])
		
		#redibujado de pelota
		pygame.draw.rect(campo, pelota[5], pelota[0])

def CambiarDireccion(direccion,choquejugador):
	#cambiando direccion de pelota
	#choque con lado superior e inferior
	mov_horizontales = {
		1: 5,
		2: 4,
		3: 7,
		4: 2,
		5: 1,
		6: 8,
		7: 3,
		8: 6
	}
	#choque con jugadores
	mov_jugador = {
		1: 5,
		2: 8,
		3: 7,
		4: 6,
		5: 1,
		6: 4,
		7: 3,
		8: 2 
	}	
	return mov_jugador[direccion] if choquejugador else mov_horizontales[direccion]

def Reinciar(campo, pelota, jugador_anotacion, jugador):
	#borrando pelota y jugadores de pantalla
	campo.fill((0,0,0), pelota[0])
	campo.fill((0,0,0), jugador[1])
	campo.fill((0,0,0), jugador_anotacion[1])
	
	#creando pelota
	pelota = CrearPelota(campo,jugador_anotacion[0])
	pelota[2] = 2 if (jugador_anotacion[0] == 1) else 8
	
	#anotacion del jugador
	jugador_anotacion[2] = jugador_anotacion[2] + 1
	Anotacion(campo, jugador_anotacion)
	
	#centrando jugadores en campo de juego
	jugador_anotacion[1].center = (jugador_anotacion[1].center[0],150)
	jugador[1].center = (jugador[1].center[0],150)
	
	#redibujando jugadores en pantalla
	pygame.draw.rect(campo, jugador_anotacion[3], jugador_anotacion[1])
	pygame.draw.rect(campo, jugador[3], jugador[1])
	
	#retornando pelota y jugadores
	return pelota, jugador_anotacion, jugador
	
def main():
	
	#iniciando juego
	campo, reloj = IniciarVentana(600,300)
	
	lado_a, lado_b, lado_c, lado_d, dlados = DibujarSuperficieDelCampo(campo)
		
	jugador1, jugador2 = IniciarJugadores(campo, (51, 153, 255), (153, 255, 102))
	
	pelota = CrearPelota(campo,jugador1[0])	
	
	
	#variable que controla loop
	salir = False
	
	#cuadros por segundo
	FPS = 60
	
	#ciclo de actualización del juego
	while not salir:
		
		#control de ejecucion del ciclo while
		reloj.tick(FPS)
		
		
		#verificando evento de boton salir y click en mouse
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN and not pelota[1]:
				#movimiento de pelota en base a la posición del mouse (en eje y) al hacer click
				if pygame.mouse.get_pos()[1] <= 110:
					pelota[2] = CambiarDireccion(4,False) if pelota[0].left == 49 else CambiarDireccion(3,False)
				elif pygame.mouse.get_pos()[1] >= 190:
					pelota[2] = CambiarDireccion(2,False) if pelota[0].left == 49 else CambiarDireccion(8,False)
				else:
					pelota[2] = CambiarDireccion(7,False) if pelota[0].left == 49 else CambiarDireccion(3,False)
				pelota[1] = True 
				
		
        #verificar presión de teclas flecha arriba y flecha abajo
		pressed = pygame.key.get_pressed()
		#fue presionada la tecla flecha arriba
		if pressed[pygame.K_UP] and not pressed[pygame.K_DOWN]: 
			jugador1[4][0] = 0 if jugador1[4][1] else jugador1[4][0] + 0.3
			jugador1[4][1] = False
			jugador1 = MoverJugador(campo, jugador1,1 + int(jugador1[4][0]))
			if not pelota[1]:
				campo.fill((0,0,0), pelota[0])
				pelota[0].move_ip(0, jugador1[1].center[1]-pelota[0].center[1])
				pygame.draw.rect(campo, pelota[5], pelota[0])
		#fue presionada tecla flecha abajo
		elif pressed[pygame.K_DOWN] and not pressed[pygame.K_UP]: 
			jugador1[4][0] = 0 if not jugador1[4][1] else jugador1[4][0] + 0.3
			jugador1[4][1] = True 
			jugador1 = MoverJugador(campo, jugador1,1 + int(jugador1[4][0]))
			if not pelota[1]:
				campo.fill((0,0,0), pelota[0])
				pelota[0].move_ip(0, jugador1[1].center[1]-pelota[0].center[1])
				pygame.draw.rect(campo, pelota[5], pelota[0])
		
		
		#mover la pelota solo si esta permitido
		if pelota[1]:		
			MoverPelota(pelota,campo)

		#mover jugador2 solo si esta la pelota en movimiento
		if random.randint(1,10)>=5 and pelota[1] and pelota[0].x > random.randint(270,330):
			jugador2[4][1] = True if pelota[3][1] == 1 else False
			jugador2[4][0] = jugador2[4][0] + 0.3
			jugador2 = MoverJugador(campo, jugador2,1 + int(jugador2[4][0]))
		else:
			jugador2[4][0] = 0
			
		#colision en superficies
		#rebote frontal en jugador2
		if (jugador2[1].left == pelota[0].right) and ((pelota[0].bottom < jugador2[1].bottom and pelota[0].bottom > jugador2[1].top) or (pelota[0].top > jugador2[1].bottom and pelota[0].top < jugador2[1].top)):
			pelota[2] = CambiarDireccion(pelota[2],True)
		#rebote frontal en jugador1
		elif (jugador1[1].right == pelota[0].left) and ((pelota[0].bottom < jugador1[1].bottom and pelota[0].bottom > jugador1[1].top) or (pelota[0].top > jugador1[1].bottom and pelota[0].top < jugador1[1].top)):
			pelota[2] = CambiarDireccion(pelota[2],True)
		#rebote en lado superior
		elif (lado_a.bottom == pelota[0].top):
			pelota[2] = CambiarDireccion(pelota[2],False)
		#anotación en lado derecho
		elif (lado_b.left - 1 == pelota[0].right):
			pelota, jugador1, jugador2 = Reinciar(campo, pelota, jugador1, jugador2)
		#rebote en lado inferior
		elif (lado_c.top - 1 == pelota[0].bottom):
			pelota[2] = CambiarDireccion(pelota[2],False)
		#anotacion en lado izquerdo
		elif (lado_d.right == pelota[0].left):
			pelota, jugador2, jugador1 = Reinciar(campo, pelota, jugador2, jugador1)
		
		#redibujado del division de lados
		if (pelota[0].center[0] == 292 and pelota[3][0] == -1) or (pelota[0].center[0] == 306 and pelota[3][0] == 1):
			campo.fill((0,0,0), dlados[0])
			dlados = [pygame.draw.line(campo,(0,0,0), (300,33), (300,268),1), False]
			DibujarDivisionDeLados(campo)
			
		#actualizacion de pantalla
		pygame.display.flip()
		
		
main()
