import cv2
import numpy as np
"""
https://aishack.in/tutorials/hough-transform-basics/
https://livecodestream.dev/post/2020-05-26-hough-transformation/
"""
"""
img = cv2.imread('Sample_scene.jpg')
#img = cv2.imread('banana.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,50,150,apertureSize = 3)
#cv2.imshow('image',edges)
#key = cv2.waitKey(0)
lines = cv2.HoughLines(edges,1,np.pi/180,1400)

for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(255,255,255),1)

cv2.imwrite('houghlines3.jpg',img)

"""
# Read image as gray-scale
img = cv2.imread('Sample_scene.jpg', cv2.IMREAD_COLOR)
# Convert to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image to reduce noise
img_blur = cv2.medianBlur(gray, 5)
# Apply hough transform on the image
circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0]/64, param1=200, param2=10, minRadius=5, maxRadius=200)
# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Draw outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (255, 255, 255), 1)
        # Draw inner circle
        cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 2)
cv2.imwrite('houghlines3.jpg',img)