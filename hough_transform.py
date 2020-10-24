import cv2
import numpy as np
import os
from tkinter import *
from tkinter import filedialog as fd

"""
https://aishack.in/tutorials/hough-transform-basics/
https://livecodestream.dev/post/2020-05-26-hough-transformation/
"""


#os.system('clear')
root = Tk()
root.title('Hough Transform 霍夫变换v1.0')
root.geometry("800x600")

"""
Texts
"""
ls_texts = list(["Rho","Theta", "Threshold", "dp(1 in normal)",
                 "Higher Threshold(300 recommended)", "Circle Perfectness(0.9 recommended)", "Minimum Radius",
                 "Max Radius"])

"""
labels
"""
ls_labels = [None] * len(ls_texts)

for i in range(len(ls_labels)):
    ls_labels[i] = Label(root, text=ls_texts[i])
for i in range(len(ls_labels)):
    if i < 3:
        ls_labels[i].grid(row=i, column=0)
    else:
        ls_labels[i].grid(row=i-3, column=2)
"""
Entries
"""
ls_entries = []
for i in range(8):
    entry = Entry(borderwidth=5)
    ls_entries.append(entry)
for i in range(len(ls_entries)):
    ls_entries[i].insert(0, ls_texts[i])
for i in range(len(ls_entries)):
    if i < 3:
        ls_entries[i].grid(row=i, column=1)
    else:
        ls_entries[i].grid(row=i-3, column=3)

#img_name = ls_entries[0].get()

def hough_transform_line():
    """
    rho: Distance resolution of the accumulator in pixels.
    heta: Angle resolution of the accumulator in degrees, will be converted to radians(pi/theta)
    threshold:  Accumulator threshold parameter. Only those lines are returned that get enough
    """
    img_name = fd.askopenfilename()
    rho = int(ls_entries[0].get())
    theta = int(ls_entries[1].get())
    threshold = int(ls_entries[2].get())
    img = cv2.imread(img_name)
    #img = cv2.imread('banana.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray,50,150,apertureSize=3)
    #cv2.imshow('image',edges)
    #key = cv2.waitKey(0)
    lines = cv2.HoughLines(edges, rho, theta*(np.pi/180), threshold)

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
    cv2.imwrite('hough_lines.jpg',img)


#img_name2 = ls_entries[4].get()

def hough_transform_circle():
    """
    .   @param circles Output vector of found circles. Each vector is encoded as  3 or 4 element
    .   floating-point vector \f$(x, y, radius)\f$ or \f$(x, y, radius, votes)\f$ .
    .   @param dp Inverse ratio of the accumulator resolution to the image resolution. For example, if
    .   dp=1 , the accumulator has the same resolution as the input image. If dp=2 , the accumulator has
    .   half as big width and height. For #HOUGH_GRADIENT_ALT the recommended value is dp=1.5,
    .   unless some small very circles need to be detected.
    .   @param minDist Minimum distance between the centers of the detected circles. If the parameter is
    .   too small, multiple neighbor circles may be falsely detected in addition to a true one. If it is
    .   too large, some circles may be missed.
    .   @param param1 First method-specific parameter. In case of #HOUGH_GRADIENT and #HOUGH_GRADIENT_ALT,
    .   it is the higher threshold of the two passed to the Canny edge detector (the lower one is twice smaller).
    .   Note that #HOUGH_GRADIENT_ALT uses #Scharr algorithm to compute image derivatives, so the threshold value
    .   should normally be higher, such as 300 or normally exposed and contrasty images.
    .   @param param2 Second method-specific parameter. In case of #HOUGH_GRADIENT, it is the
    .   accumulator threshold for the circle centers at the detection stage. The smaller it is, the more
    .   false circles may be detected. Circles, corresponding to the larger accumulator values, will be
    .   returned first. In the case of #HOUGH_GRADIENT_ALT algorithm, this is the circle "perfectness" measure.
    .   The closer it to 1, the better shaped circles algorithm selects. In most cases 0.9 should be fine.
    .   If you want get better detection of small circles, you may decrease it to 0.85, 0.8 or even less.
    .   But then also try to limit the search range [minRadius, maxRadius] to avoid many false circles.
    .   @param minRadius Minimum circle radius.
    .   @param maxRadius Maximum circle radius. If <= 0, uses the maximum image dimension. If < 0, #HOUGH_GRADIENT returns
    .   centers without finding the radius. #HOUGH_GRADIENT_ALT always computes circle radiuses.
    """
    img_name2 = fd.askopenfilename()
    dp = float(ls_entries[3].get())
    p1 = int(ls_entries[4].get())
    p2 = float(ls_entries[5].get())
    minR = int(ls_entries[6].get())
    maxR = int(ls_entries[7].get())
    # Read image as gray-scale
    img = cv2.imread(img_name2, cv2.IMREAD_COLOR)
    # Convert to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    img_blur = cv2.medianBlur(gray, 5)
    # Apply hough transform on the image
    #circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0]/64, param1=200, param2=10, minRadius=5, maxRadius=200)
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, dp, img.shape[0] / 64, param1=p1, param2=p2, minRadius=minR, maxRadius=maxR)

    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (255, 255, 255), 1)
            # Draw inner circle
            cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 2)
    cv2.imwrite('hough_circle.jpg',img)


"""
buttons 
"""
t1 = 'Generate Hough Lines'
start_transform_lines = Button(root, text=t1, command=hough_transform_line)
start_transform_lines.grid(column=1)
t2 = 'Generate Hough Circles'
start_transform_circles= Button(root, text=t2, command=hough_transform_circle)
start_transform_circles.grid(column=3)
root.mainloop()
