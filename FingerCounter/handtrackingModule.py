import cv2
import mediapipe as mp
import time


class HandTracking:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize mediapipe hand detector
        self.mphands = mp.solutions.hands
        self.hand = self.mphands.Hands()
        self.mpdraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
 
        while True:
            # Process image for hand tracking
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hand.process(imgRGB)

            # Draw landmarks if hands are detected and draw is True
            if self.results.multi_hand_landmarks and draw:
                for handlms in self.results.multi_hand_landmarks:
                    self.mpdraw.draw_landmarks(img, handlms, self.mphands.HAND_CONNECTIONS)
            return img
        
    def findpositions(self,img, handnumber = 0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handnumber]
            for id, lm in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(0,0,255),cv2.FILLED)

        return lmlist

# Main guard to allow script execution only if run directly
if __name__ == "__main__":
    
    # Timing variables for FPS calculation
    cTime = 0
    pTime = 0
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    detector = HandTracking()
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