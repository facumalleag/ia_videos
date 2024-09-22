import easyocr
import cv2
import os
import csv

notif = [
    ["Tirador", "Neutralizado"]
]
with open('out.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(notif)
    csvfile.flush()
    csvfile.close()


# path='C:/Users/facum/PycharmProjects/tesis_convo/images'

def process_text(path):
    lector = easyocr.Reader(['en', 'es'], gpu=False)
    images = [f for f in os.listdir(path) if f.endswith(('.jpg', '.png', '.bmp'))]

    for image in images:
        image_path = os.path.join(path, image)
        imagen = cv2.imread(image_path)
        text = lector.readtext(imagen, contrast_ths=0.4,
                               adjust_contrast=0.5, text_threshold=0.5)
        with open('out.csv', 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(csvfile)
            # leer ultima fila del archivo
            for fila_leida in reader:
                ultima_fila = fila_leida
            aux0 = ''.join(map(str, ultima_fila[0]))
            aux1 = ''.join(map(str, ultima_fila[1]))
            print(aux0)
            print(aux1)
            if text.__len__() != 0 and (aux1 != text[1][1] or aux0 != text[0][1]):
                # texto = pytesseract.image_to_string(frame)
                writer.writerow([text[0][1], text[1][1]])
                print("Agregue: ", text[0][1])
                print("Agregue: ", text[1][1])
                # print("TEXTO: " + texto)
                csvfile.flush()

    return 0

# INPUT_FOLDER = "app/temp/images/images_amazon"
#
# # this needs to run only once to load the model into memory
# reader = easyocr.Reader(['es', 'en'])
#
#
# def apply_blur_detected_text(image, coords):
#     for (top_left, bottom_right) in coords:
#         x1, y1 = map(int, top_left)
#         x2, y2 = map(int, bottom_right)
#
#         x1 = max(0, min(x1, image.shape[1] - 1))
#         y1 = max(0, min(y1, image.shape[0] - 1))
#         x2 = max(0, min(x2, image.shape[1] - 1))
#         y2 = max(0, min(y2, image.shape[0] - 1))
#
#         if y2 > y1 and x2 > x1:
#             image[y1:y2, x1:x2] = cv2.GaussianBlur(
#                 image[y1:y2, x1:x2], (95, 95), 0)
#         else:
#             print(f"Invalid coords or empty area: {(x1, y1)}, {(x2, y2)}")
#
#     return image
#
#
# def outside_central_zone(image_shape, coord, central_zone_ratio=0.3):
#     height, width = image_shape[:2]
#     x1, y1 = coord[0]
#     x2, y2 = coord[1]
#
#     central_x_min = int(width * (1 - central_zone_ratio) / 2)
#     central_x_max = int(width * (1 + central_zone_ratio) / 2)
#     central_y_min = int(height * (1 - central_zone_ratio) / 2)
#     central_y_max = int(height * (1 + central_zone_ratio) / 2)
#
#     not_central_zone = (
#             x2 < central_x_min or
#             x1 > central_x_max or
#             y2 < central_y_min or
#             y1 > central_y_max
#     )
#
#     return not_central_zone
#
#
# def text_detector(image_path, min_font_size_ratio=0.04):
#     filtered_results = []
#
#     print(f"Processing... Looking for text on image path: {image_path}...")
#
#     image = cv2.imread(image_path)
#
#     if image is None:
#         print(f"Error: Error loading {image_path}")
#         return False, None
#
#     results = reader.readtext(image)
#
#     for result in results:
#         bbox = result[0]
#         text_confidence = result[2]
#         font_size = (bbox[2][1] - bbox[0][1]) / image.shape[0]
#
#         if text_confidence > min_font_size_ratio and font_size >= min_font_size_ratio and outside_central_zone(
#                 image.shape, (bbox[0], bbox[2])):
#             filtered_results.append(result)
#
#     if filtered_results:
#         coords = [(result[0][0], result[0][2])
#                   for result in filtered_results]
#         img_blurred = apply_blur_detected_text(image, coords)
#         base_filename, ext = os.path.splitext(image_path)
#         new_filename = f"{base_filename}_blurred{ext}"
#
#         cv2.imwrite(new_filename, img_blurred)
#
#         os.remove(image_path)
#
#         print(f"Text found: {filtered_results} \n")
#
#         print(f"Blurred image saved and original replaced at: {image_path}")
#
#         return True, new_filename
#
#     else:
#         print(f"No text detected on path: {image_path}")
#         return True, image_path
#
#
# cap = cv2.VideoCapture('C:/Users/facum/PycharmProjects/armas/AK47_Death_SimpleAsistencia_Pacificador_2.mkv')
# ret, frame = cap.read()
# res, file = text_detector(frame)
# cv2.imshow("File retornado", file)
