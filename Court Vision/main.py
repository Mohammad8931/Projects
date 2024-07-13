import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
import math

# Initialize video capture from a file
video_capture = cv2.VideoCapture('Videos/vid (1).mp4')

# Initialize the color finder with HSV color values
color_finder = ColorFinder(False)
hsv_values = {'hmin': 8, 'smin': 124, 'vmin': 13, 'hmax': 24, 'smax': 255, 'vmax': 255}

# Lists to store the X and Y positions of the ball
ball_positions_x = []
ball_positions_y = []

# List of X values for trajectory prediction
trajectory_x = [x for x in range(0, 1300)]

# Flags to control the start of processing and prediction
start_processing = True
is_prediction_valid = False

while True:
    if start_processing:
        if len(ball_positions_x) == 10:
            start_processing = False

        # Read a frame from the video
        success, frame = video_capture.read()

        # Crop the frame to focus on the relevant area
        frame = frame[0:900, :]

        # Create copies of the frame for different processing steps
        frame_prediction = frame.copy()
        frame_result = frame.copy()

        # Detect the ball based on the color values
        frame_ball, mask = color_finder.update(frame, hsv_values)
        frame_contours, contours = cvzone.findContours(frame, mask, 200)

        # If a ball is detected, store its position
        if contours:
            ball_positions_x.append(contours[0]['center'][0])
            ball_positions_y.append(contours[0]['center'][1])

        # If we have detected positions, calculate the trajectory
        if ball_positions_x:
            if len(ball_positions_x) < 18:
                # Fit a polynomial to the detected positions
                coefficients = np.polyfit(ball_positions_x, ball_positions_y, 2)

            # Draw the detected positions and the trajectory
            for i, (posX, posY) in enumerate(zip(ball_positions_x, ball_positions_y)):
                position = (posX, posY)
                cv2.circle(frame_contours, position, 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame_result, position, 10, (0, 255, 0), cv2.FILLED)

                if i == 0:
                    cv2.line(frame_contours, position, position, (0, 255, 0), 2)
                    cv2.line(frame_result, position, position, (0, 255, 0), 2)
                else:
                    cv2.line(frame_contours, (ball_positions_x[i - 1], ball_positions_y[i - 1]), position, (0, 255, 0), 2)
                    cv2.line(frame_result, (ball_positions_x[i - 1], ball_positions_y[i - 1]), position, (0, 255, 0), 2)

            # Predict the future positions based on the trajectory
            for x in trajectory_x:
                y = int(coefficients[0] * x ** 2 + coefficients[1] * x + coefficients[2])
                cv2.circle(frame_prediction, (x, y), 2, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame_result, (x, y), 2, (255, 0, 255), cv2.FILLED)

            # Predict whether the shot will be a basket
            if len(ball_positions_x) < 10:
                a, b, c = coefficients
                c = c - 593
                x_intercept = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
                is_prediction_valid = 300 < x_intercept < 430

            # Display the prediction result
            if is_prediction_valid:
                cvzone.putTextRect(frame_result, "Basket", (50, 150), colorR=(0, 200, 0), scale=5, thickness=10, offset=20)
            else:
                cvzone.putTextRect(frame_result, "No Basket", (50, 150), colorR=(0, 0, 200), scale=5, thickness=10, offset=20)

        # Draw the basket line
        cv2.line(frame_contours, (330, 593), (430, 593), (255, 0, 255), 10)

        # Resize the result frame for display
        frame_result = cv2.resize(frame_result, (0, 0), None, 0.7, 0.7)

        # Display the result frame
        cv2.imshow("Basketball Shot Predictor", frame_result)

    # Wait for the 's' key to restart processing
    key = cv2.waitKey(100)
    if key == ord("a"):
        start_processing = True
