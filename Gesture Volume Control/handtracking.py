import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hand = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    results = hand.process(imgRGB)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)
            for id, lm in enumerate(handlms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img,(cx,cy),5,(0,0,255),cv2.FILLED)
            
            
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
    
    cv2.imshow("image",img)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()


