import cv2
import pytesseract
import easyocr
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
cap = cv2.VideoCapture('C:/Users/facum/PycharmProjects/armas/MP5SD_Death_Headshot_Pacificador.mkv')

reader = easyocr.Reader(['en', 'es'])
ret, frame = cap.read()

x = 1400
y = 50
ancho = 600
alto = 70

recorte = frame[y:y + alto, x:x + ancho]
img_gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
dst = cv2.detailEnhance(recorte, sigma_s=10, sigma_r=1)
color2 = cv2.resize(dst, (640, 128))

img_gauss = cv2.GaussianBlur(img_gris, (5, 5), 0)
img_unsharp = cv2.addWeighted(img_gris, 2.0, img_gauss, -1.2, 2)
frame2 = cv2.resize(img_unsharp, (640, 128))
dst2 = cv2.resize(img_unsharp, (640, 128))
#
# # Binarizar la imagen
_, thr = cv2.threshold(img_gris, 80, 255, cv2.THRESH_BINARY_INV)
#
# # thr = cv2.Canny(img_gris, 10, 255) Trzar los bordes de las imagenes
#
#
# # Kernel
kernel = np.ones((3, 3), np.uint8)


#
# # Erosion (agranda los pixeles negros)
# erosion = cv2.erode(thr, kernel, iterations=1)
#
# # Dilatacion (agranda los pixeles blancos)
# dilatacion = cv2.dilate(erosion, kernel, iterations=1)
#
# # Opening (dilatacion + erosion)
# opening = cv2.morphologyEx(thr, cv2.MORPH_RECT, kernel, iterations=1)
#
# # Closing (erosion + dilatacion)
# closing = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, kernel, iterations=1)
#
# # Buscar el contorno
# contorno, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(recorte, contorno, -1, (0, 255, 0))
#
# # rellenar
# cv2.fillPoly(closing, contorno, color=(255, 255, 255))
#
# cv2.imshow("Imagen binarizada", thr)# no tan bien
# cv2.imshow("Imagen Gris Mejorada", dst2) # no tan bien pero detecta ONLY le falt la i
# cv2.imshow("Imagen DST", color2) # 'TJ Frl', Only
# cv2.imshow("Imagen Gris", dst) # no tan bien 'TJ FrI',Dnly
# cv2.imshow('Mejorada con CV2', img_unsharp) # no tan bien
# cv2.imshow('Mejorada con CV2 y agrandada', frame2) # TJFrl, Only
# cv2.imshow("Imagen Dilatada", dilatacion)
# cv2.imshow("Imagen Erosionda", erosion)
# cv2.imshow("Imagen Opening", opening)
# cv2.imshow("Imagen Closing", closing)
# cv2.imshow("Imagen con contorno", recorte)


# img = cv2.imread('C:/Users/facum/PycharmProjects/videoExtractor/jpg_from_videos/aa.png')

# texto = pytesseract.image_to_string(img_unsharp)

def outside_central_zone(image_shape, coord, central_zone_ratio=0.3):
    height, width = image_shape[:2]
    x1, y1 = coord[0]
    x2, y2 = coord[1]

    central_x_min = int(width * (1 - central_zone_ratio) / 2)
    central_x_max = int(width * (1 + central_zone_ratio) / 2)
    central_y_min = int(height * (1 - central_zone_ratio) / 2)
    central_y_max = int(height * (1 + central_zone_ratio) / 2)

    not_central_zone = (
            x2 < central_x_min or
            x1 > central_x_max or
            y2 < central_y_min or
            y1 > central_y_max
    )

    return not_central_zone


def apply_blur_detected_text(image, coords):
    for (top_left, bottom_right) in coords:
        x1, y1 = map(int, top_left)
        x2, y2 = map(int, bottom_right)

        x1 = max(0, min(x1, image.shape[1] - 1))
        y1 = max(0, min(y1, image.shape[0] - 1))
        x2 = max(0, min(x2, image.shape[1] - 1))
        y2 = max(0, min(y2, image.shape[0] - 1))

        if y2 > y1 and x2 > x1:
            image[y1:y2, x1:x2] = cv2.GaussianBlur(
                image[y1:y2, x1:x2], (95, 95), 0)
        else:
            print(f"Invalid coords or empty area: {(x1, y1)}, {(x2, y2)}")

    return image


while True:
    min_font_size_ratio = 0.04
    filtered_results = []

    results = reader.readtext(color2)
    print(results)
    cv2.waitKey(0)

    for result in results:
        bbox = result[0]
        text_confidence = result[2]
        font_size = (bbox[2][1] - bbox[0][1]) / color2.shape[0]

        if text_confidence > min_font_size_ratio and font_size >= min_font_size_ratio and outside_central_zone(
                color2.shape, (bbox[0], bbox[2])):
            filtered_results.append(result)

    if filtered_results:
        coords = [(result[0][0], result[0][2])
                  for result in filtered_results]
        img_blurred = apply_blur_detected_text(color2, coords)
        base_filename, ext = os.path.splitext('_2_1_3')
        new_filename = f"{base_filename}_blurred{ext}"

        # cv2.imwrite(new_filename, img_blurred)

        # os.remove(image_path)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
            print(f"Text found: {filtered_results} \n")
            break

#     print(f"Blurred image saved and original replaced at: {image_path}")
#
#     return True, new_filename
#
# else:
#     print(f"No text detected on path: {image_path}")
#     return True, image_path

cap.release()
cv2.destroyAllWindows()
