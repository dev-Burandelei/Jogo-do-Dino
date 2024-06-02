import cv2
import mediapipe as mp
import subprocess
import pygame

def pular():
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    pygame.event.post(event)

# Inicia o jogo em um subprocess
subprocess.Popen(["python", "jogo-dino.py"])

video = cv2.VideoCapture(0) #abrir câmera

hands = mp.solutions.hands #conf do mediapipe
Hands = hands.Hands(max_num_hands=1)#numero máximo de mãos que o algoritmo reconhece
mpDwaw = mp.solutions.drawing_utils #desenhar as ligações entre os pontos nas mãos

while True:
    success, img = video.read() 
    frameRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #converter para RGBa imagem capturada
    results = Hands.process(frameRGB) #processar a imagem com mediapipe
    handPoints = results.multi_hand_landmarks #extraindo as coordenadas dos pontos do desenho da mão
    h, w, _ = img.shape #extraindo as dimensões da imagem
    pontos = []
    if handPoints: #verifica se a variável n está vazia
        for points in handPoints: #retornar as coordenadas de cada ponto
            mpDwaw.draw_landmarks(img, points,hands.HAND_CONNECTIONS) #desenhar os pontos
            #podemos enumerar esses pontos da seguinte forma
            for id, cord in enumerate(points.landmark): #enumerar cada ponto da mão
                cx, cy = int(cord.x * w), int(cord.y * h)
                cv2.putText(img, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                pontos.append((cx,cy))

            dedos = [8,12,16,20]
            contador = 0
            if pontos:
                if pontos[4][0] < pontos[3][0]: #lógica para o dedão
                    contador += 1
                for x in dedos:
                   if pontos[x][1] < pontos[x-2][1]: #lógica do dedo abaixado, sem o dedão
                       contador +=1 #quantos dedos estão levantados

            cv2.rectangle(img, (80, 10), (200,110), (255, 0, 0), -1)
            cv2.putText(img,str(contador),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)
            #print(contador)

             # Chama a função especial se o contador for igual a 1
            if contador == 1:
                pular()
                
    cv2.imshow('Imagem',img)
    cv2.waitKey(1)
    #if cv2.waitKey(1) & 0xFF == 27: # pressione ESC para sair
        #break


#cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)


# for id,cord in enumerate(points.landmark):
#     cx, cy = int(cord.x * w), int(cord.y * h)
#     cv2.putText(img, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     pontos.append([cx,cy])
#     if pontos:
#         print(pontos)