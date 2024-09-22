import time
import numpy as np
import cv2

cap = cv2.VideoCapture('C:/Users/facum/PycharmProjects/armas/AUG_Kill_SimpleAsistencia_Pacificador.mkv')


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        # If the video reaches the end, rewind it to the start
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    #     count += 1
    #     if count % 3 != 0:
    #        continue

    x = 1400
    y = 50
    ancho = 600
    alto = 400

    recorte = frame[y:y + alto, x:x + ancho]

    # cv2.imshow('Recorte', recorte)
    frame = cv2.resize(recorte, (1020, 600))
    hsv = cv2.cvtColor(recorte, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(recorte, recorte, mask=mask)

    # show thresholded image
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
