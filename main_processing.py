import cv2
import pytesseract
import easyocr
import detecting_text

MARGIN = -1  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
rect_color = (255, 0, 255)
TEXT_COLOR = (255, 0, 0)  # red

cap2 = cv2.VideoCapture('C:/Users/facum/PycharmProjects/armas/XM1014_Death_Simple_Pacificador.mkv')
# Recorte panel superior derecho
x = 1400
y = 50
ancho = 600
alto = 70
# recorte panel inferior izquierdo
x1 = 0
y1 = 880
ancho1 = 500
alto1 = 150

fps = cap2.get(cv2.CAP_PROP_FPS)
intervalo = int(0.3 * fps)
contador = 0

# Tiempo para capturar panel inf izquierdo
intervalo2 = int(2 * fps)
contador2 = 0

while True:
    ret, frame = cap2.read()

    if not ret:
        break
    if contador2 % intervalo2 == 0:
        recorte_inf = frame[y1:y1 + alto1, x1:x1 + ancho1]
        ultima_img = recorte_inf
        dst = cv2.detailEnhance(recorte_inf, sigma_s=12, sigma_r=3)
        if contador2 > 0:
            hist1 = cv2.calcHist([ultima_img], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([dst], [0], None, [256], [0, 256])
            simulitud = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
            porcentaje_diferencia = (1 - simulitud) * 100
            if porcentaje_diferencia < 30:
                print(f'Guardo print de imagen panel inferior')
                ultima_img = dst
                cv2.imwrite(f'C:/Users/facum/PycharmProjects/tesis_convo/images/panel_inf_{contador}.jpg', dst)
        else:
            ultima_img = dst
            cv2.imwrite(f'C:/Users/facum/PycharmProjects/tesis_convo/images/panel_inf_{contador}.jpg', dst)
    contador2 += 1
    if contador % intervalo == 0:
        recorte = frame[y:y + alto, x:x + ancho]
        img_gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
        ultima_img = img_gris
        # dst = cv2.detailEnhance(img_gris, sigma_s=10, sigma_r=1)
        # color2 = cv2.resize(dst, (640, 128))
        # _, thr = cv2.threshold(img_gris, 80, 255, cv2.THRESH_BINARY)
        img_gauss = cv2.GaussianBlur(img_gris, (5, 5), 0)
        img_unsharp = cv2.addWeighted(img_gris, 2.0, img_gauss, -1.2, 2)
        color2 = cv2.resize(img_unsharp, (640, 128))
        if contador > 0:
            hist1 = cv2.calcHist([ultima_img], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([color2], [0], None, [256], [0, 256])
            simulitud = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
            porcentaje_diferencia = (1 - simulitud) * 100
            print(f'Porcentaje simulitud: {porcentaje_diferencia}',
                  f'Contador: {contador}')  # {porcentaje_simulitud:.2f}%
            if porcentaje_diferencia < 35:
                print(f'Guardo print de imagen')
                cv2.imwrite(f'C:/Users/facum/PycharmProjects/tesis_convo/images/panel_sup_{contador}.jpg', color2)
                ultima_img = color2
        else:
            cv2.imwrite(f'C:/Users/facum/PycharmProjects/tesis_convo/images/panel_sup_{contador}.jpg', color2)
            ultima_img = color2
    contador += 1
    cv2.imshow("Juego CS 2", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap2.release()
cv2.destroyAllWindows()
detecting_text.process_text('C:/Users/facum/PycharmProjects/tesis_convo/images')
