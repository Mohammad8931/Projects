import cv2
import time
import mediapipe as mp
import handtrackingModule as htm


# Timing variables for FPS calculation
cTime = 0
pTime = 0
# Initialize video capture
cap = cv2.VideoCapture(0)
detector = htm.HandTracking()
while True:
    # Capture frame-by-frame
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findpositions(img)
    
    if lmlist:
        print(lmlist[4])
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
    cv2.imshow("image",img)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break