import mediapipe as mp
import csv
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
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

# cap2 = ImrpoveQuality.return_video_updated('C:/Users/facum/PycharmProjects/project_ia/tflite-mediapipe-main'
#                                            '/freedomtech/video2.mp4',
#                                            'C:/Users/facum/PycharmProjects/project_ia/tflite-mediapipe-main'
#                                            '/freedomtech'
#                                            '/Video_output.mp4')


# base_options = python.BaseOptions(model_asset_path='best.tflite')
# options = vision.ObjectDetectorOptions(base_options=base_options,
#                                        # score_threshold=0.5,
#                                        # max_results=5,
#                                        # running_mode=vision.RunningMode.VIDEO
#                                        score_threshold=0.5
#                                        )
# detector = vision.ObjectDetector.create_from_options(options)
cap2 = cv2.VideoCapture('C:/Users/facum/PycharmProjects/armas/M4A1S_Kill_Asistencia_Pacificador.mkv')
x = 1400
y = 50
ancho = 600
alto = 70

fps = cap2.get(cv2.CAP_PROP_FPS)
intervalo = int(0.3 * fps)
contador = 0

while True:
    ret, frame = cap2.read()

    if not ret:
        break
    if contador % intervalo == 0:
        recorte = frame[y:y + alto, x:x + ancho]
        ultima_img=recorte
        img_gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
        # dst = cv2.detailEnhance(img_gris, sigma_s=10, sigma_r=1)
        # color2 = cv2.resize(dst, (640, 128))
        _, thr = cv2.threshold(img_gris, 80, 255, cv2.THRESH_BINARY)
        img_gauss = cv2.GaussianBlur(img_gris, (5, 5), 0)
        img_unsharp = cv2.addWeighted(img_gris, 2.0, img_gauss, -1.2, 2)
        color2 = cv2.resize(img_unsharp, (640, 128))
        if contador > 0:
            hist1 = cv2.calcHist([ultima_img], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([color2], [0], None, [256], [0, 256])
            simulitud = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
            porcentaje_simulitud = (1 - simulitud) * 100
            print(f'Porcentaje simulitud: {porcentaje_simulitud}', f'Contador: {contador}')  #{porcentaje_simulitud:.2f}%
            if porcentaje_simulitud < 30:
                print(f'Guardo print de imagen')
                cv2.imwrite(f'C:/Users/facum/PycharmProjects/tesis_convo/images/frame_{contador}.jpg', color2)
                ultima_img = color2
        else:
            cv2.imwrite(f'C:/Users/facum/PycharmProjects/tesis_convo/images/frame_{contador}.jpg', color2)
            ultima_img=color2

    contador += 1
    cv2.imshow("test window", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap2.release()
cv2.destroyAllWindows()
detecting_text.process_text('C:/Users/facum/PycharmProjects/tesis_convo/images')
# adjust_csv.eliminar_duplicados_y_ajustar_csv('out.csv')
