import pygame
import cv2
import mediapipe as mp
import numpy as np
import sys
import random


# Inicializamos Pygame
pygame.init()

#Set up clock
clock = pygame.time.Clock()

# Inicializar FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

#Inicializamos los mensajes
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 42)
text_surface = my_font.render('Has perdido', False, (255, 0, 0))

# Definimos las constantes para la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
camera_width=ANCHO_PANTALLA//3
camera_height=ALTO_PANTALLA//3

# Inicializar la webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

blanco=[255,255,255]
negro=[0,0,0]
rojo = (255,0,0)
verde = (0,255,255)
velocidad_misil =[0,3]


# Creamos la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Cohete")


# Definimos las constantes para el cohete
VELOCIDAD_MAX = 20
ACELERACION = 1


#ponemos fondo    
imagen_fondo = pygame.image.load("sprites/Blue Nebula 8 - 1024x1024.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
rect_pantalla = imagen_fondo.get_rect()

# Cargamos la imagen del cohete y establecemos su posición inicial
imagen_cohete = pygame.image.load("sprites/rocket.png")
imagen_cohete = pygame.transform.scale(imagen_cohete, (imagen_cohete.get_width() // 4, imagen_cohete.get_height() // 4))
posicion_cohete = [ANCHO_PANTALLA / 0.3, ALTO_PANTALLA / 0.3]
velocidad_cohete = [0, 0]
rect_cohete = imagen_cohete.get_rect()
rect_cohete.move_ip(posicion_cohete)

#Creamos lista 
Misiles = []
velocidades = []

imagen_misil = pygame.image.load("sprites/missile.png")
imagen_misil = pygame.transform.scale(imagen_misil, (imagen_misil.get_width() // 2, imagen_misil.get_height() // 2))

# Juego terminado
final = False

for i in range (5):
    rect_misil = imagen_misil.get_rect()
    Misiles.append(rect_misil)
    velocidades.append(random.randint(1,5))
    


# Definimos el bucle principal del juego
while True:
# Capturar frame de la webcam
    ret, frame = cap.read()

    # Convertir la imagen a RGB para procesarla con Facemesh
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar el rostro con Facemesh
    results = face_mesh.process(rgb)

    # Dibujar los puntos 1 y 10 de color rojo en el frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Transformar los puntos de Facemesh a coordenadas de la pantalla
            h, w, c = frame.shape
            landmarks = np.array([(lmk.x * w, lmk.y * h, lmk.z * w) for lmk in face_landmarks.landmark])
            point1 = landmarks[0]
            point10 = landmarks[9] 
            # Dibujar los puntos en el frame
            cv2.circle(frame, (int(point1[0]), int(point1[1])), 5, (0, 0, 255), -1)
            #cv2.circle(frame, (int(point10[0]), int(point10[1])), 5, (0, 0, 255), -1)
            #cv2.line(frame, (int(point1[0]), int(point1[1])), (int(point10[0]), int(point10[1])), (0, 0, 255), 2)

        # Redimensionar el frame para mostrarlo en la ventana
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (camera_width, camera_height))   
   
    # Manejamos los eventos del teclado y actualizamos la posición del cohete

    event_list = pygame.event.get()
    for evento in event_list:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                # Movemos el cohete hacia la izquierda
                velocidad_cohete[0] = -4
            elif evento.key == pygame.K_RIGHT:
                # Movemos el cohete hacia la derecha
                velocidad_cohete[0] = 4
                
    #mover la bola con la cara
       
    if point1[0]>233:
        velocidad_cohete[0] = -4
    elif point1[0]<233:
        velocidad_cohete[0] = 4    
    
    


    # Actualizamos la posición del cohete en función de la velocidad
    rect_cohete.move_ip(velocidad_cohete)

    # Comprobamos si el cohete está dentro de la pantalla
    rect_cohete.clamp_ip(rect_pantalla)

    # Dibujamos el cohete en la pantalla
    #pantalla.fill((255,255,255))
    pantalla.blit(imagen_fondo, (0, 0))
    pantalla.blit(imagen_cohete,rect_cohete)
    # Mostrar el frame en la ventana
    imagen_fondo.blit(frame, (0,0))

    contador = 0
    for rect_misil in Misiles:
        rect_misil.move_ip([0,velocidades[contador]])
        # Detectar colisión entre los objetos
        if rect_misil.colliderect(rect_cohete):
            print("Has estrellado")
            final = True
    
        if rect_misil.bottom >= ALTO_PANTALLA :
            rect_misil.x = random.randint (0,ANCHO_PANTALLA)
            rect_misil.y = 0
            velocidades[contador] = random.randint(1,5)
        pantalla.blit(imagen_misil,rect_misil)
        contador = contador + 1

    # Game over
    if final: 
        pantalla.blit(text_surface, (ANCHO_PANTALLA/2 - 120, ALTO_PANTALLA/2 - 40))
        velocidad_cohete = [0,0]
        velocidad_misil = [0,0]


    pygame.display.flip()
    clock.tick(60)
