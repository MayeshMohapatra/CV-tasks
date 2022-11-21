# Code to count people in and out of a room/area
import cv2  # OpenCV library
import numpy as np  # Numpy library

video = cv2.VideoCapture("People-Counter\escalator.mp4")  # Video capture object

counter = 0  # Counter to count people in and out of the room/area
released = False  # Boolean to check if the person has been counted or not

while True:
    ret, img = video.read()  # Read video frame by frame
    # cv2.imshow("Video", img)
    # cv2.waitKey(0)  # Show video frame by frame
    # break
    # print(img.size)  # Print image shape
    img = cv2.resize(
        img,
        (1100, 720),
    )  # Resize frame
    # img = cv2.resize(img,)  # Resize video frame
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert video frame to grayscale
    x, y, w, h = 490, 230, 30, 150  # Set ROI coordinates
    imgTh = cv2.adaptiveThreshold(
        imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12
    )  # Apply adaptive threshold to grayscale image to get binary image
    kernel = np.ones((8, 8), np.uint8)  # Kernel for dilation
    imgDil = cv2.dilate(imgTh, kernel, iterations=2)  # Dilate binary image

    clip = imgDil[y : y + h, x : x + w]  # Clip the box from the image ##recorte
    white = cv2.countNonZero(
        clip
    )  # Count the number of white pixels in the box ##brancos

    if (
        white > 4000 and released == True
    ):  # If white pixels are more than 4000 and the person is not released
        counter += 1  # Increment counter
    if white < 4000:  # If white pixels are less than 4000
        released = True  # Set released to True
    else:
        released = False

    if released == False:  # If person is not released
        cv2.rectangle(
            img, (x, y), (x + w, y + h), (0, 255, 0), 4
        )  # Draw green rectangle
    else:
        cv2.rectangle(
            img, (x, y), (x + w, y + h), (255, 0, 255), 4
        )  # Draw magenta rectangle

    # cv2.putText(img, str(white), (x - 30, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1,) #print number of white pixels
    # cv2.rectangle(img, (575, 155), (575 + 88, 155 + 85), (255, 255, 255), -1) # Draw a rectangle to cover the counter
    cv2.putText(
        img,
        str(counter),
        (x + 100, y + 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        3,
        (255, 0, 0),
        5,
    )  # Display the number of people in the box

    cv2.imshow("Video", img)
    cv2.waitKey(20)  # Show video frame by frame
