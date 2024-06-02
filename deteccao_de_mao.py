import cv2
import mediapipe as mp
import pygame
import multiprocessing
import os
import pyautogui  # Usado para simular teclas do teclado

def acao_especial():
    acao = 1
    #print(acao)
    return acao

def iniciar_jogo():
    # Inicia o jogo
    os.system("python jogo_dino.py")

def detectar_mao():
    # Inicializa o Pygame (necessário para enviar eventos)
    pygame.init()

    video = cv2.VideoCapture(0)  # abrir câmera

    hands = mp.solutions.hands  # configuração do mediapipe
    Hands = hands.Hands(max_num_hands=1)  # número máximo de mãos que o algoritmo reconhece
    mpDraw = mp.solutions.drawing_utils  # desenhar as ligações entre os pontos nas mãos

    while True:
        success, img = video.read()
        if not success:
            break
        frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converter para RGB a imagem capturada
        results = Hands.process(frameRGB)  # processar a imagem com mediapipe
        handPoints = results.multi_hand_landmarks  # extraindo as coordenadas dos pontos do desenho da mão
        h, w, _ = img.shape  # extraindo as dimensões da imagem
        pontos = []
        if handPoints:  # verifica se a variável não está vazia
            for points in handPoints:  # retornar as coordenadas de cada ponto
                mpDraw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)  # desenhar os pontos
                # podemos enumerar esses pontos da seguinte forma
                for id, cord in enumerate(points.landmark):  # enumerar cada ponto da mão
                    cx, cy = int(cord.x * w), int(cord.y * h)
                    cv2.putText(img, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    pontos.append((cx, cy))

                dedos = [8, 12, 16, 20]
                contador = 0
                if pontos:
                    if pontos[4][0] < pontos[3][0]:  # lógica para o dedão
                        contador += 1
                    for x in dedos:
                        if pontos[x][1] < pontos[x-2][1]:  # lógica do dedo abaixado, sem o dedão
                            contador += 1  # quantos dedos estão levantados

                cv2.rectangle(img, (80, 10), (200, 110), (255, 0, 0), -1)
                cv2.putText(img, str(contador), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)

                # Chama a função especial se o contador for igual a 1
                if contador == 1:
                    acao_especial()  # Chama a função para pressionar a tecla de espaço
                    print("Acionado")
            
                    
        cv2.imshow('Imagem', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Criar e iniciar processos para detectar mãos e iniciar o jogo
    process_jogo = multiprocessing.Process(target=iniciar_jogo)
    process_deteccao = multiprocessing.Process(target=detectar_mao)

    process_jogo.start()
    process_deteccao.start()

    # Aguardar os processos terminarem
    process_jogo.join()
    process_deteccao.join()
