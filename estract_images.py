import cv2
import time

cpt = 0
maxFrames = 600  # if you want 5 frames only.

cap = cv2.VideoCapture('C:/Users/facum/PycharmProjects/tesis/training/train/Busqueda_Partida_Competitiva_Nuke.mkv')
while cpt < maxFrames:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1048, 720))
    cv2.imshow("test window", frame)  # show image in window
    cv2.imwrite("C:/Users/facum/PycharmProjects/tesis/training/train/images/nuke%d.png" % cpt,
                frame)
    # time.sleep(0.5)
    cpt += 1
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
