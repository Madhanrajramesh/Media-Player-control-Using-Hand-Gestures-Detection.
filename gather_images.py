import cv2
import os
import numpy as np

print("Enter the label name:- up, down, left,right,none,play,pause")
label_name = input("Enter the label name:-")
num_samples = int(input("Enter the number of samples:- "))

IMG_SAVE_PATH = 'train_images'
IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, label_name)

def preprocess_image(img):
    blur = cv2.GaussianBlur(img,(3,3),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv,np.array([2,0,0]),np.array([20,255,255]))
    kernel = np.ones((5,5))

    # Apply morphological transformations to filter out the background noise
    dilation = cv2.dilate(mask, kernel, iterations=1)
    # erosion = cv2.erode(dilation, kernel, iterations=1)

    # Apply Gaussian Blur and Threshold
    # filtered = cv2.GaussianBlur(mask, (3, 3), 0)
    ret, thresh = cv2.threshold(dilation, 70, 255, cv2.THRESH_BINARY)

    return thresh

def p2(img):
    kernel = np.ones((5,5),np.uint8)

    frame2 = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    lb = np.array([0,77,0])
    ub = np.array([255,255,255])  
    mask = cv2.inRange(frame2, lb, ub)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    img = cv2.cvtColor(opening,cv2.COLOR_BGR2RGB)
    return img

try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass
try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")

cap = cv2.VideoCapture(0)

start = False
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if count == num_samples:
        break
    
    frame = cv2.flip(frame,1)
    cv2.rectangle(frame, (300, 50), (600, 350), (255, 255, 255), 2)
    # thresh = preprocess_image(frame)

    if start:
        roi = frame[50:350, 300:600]
        save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(count + 1))
        cv2.imwrite(save_path, roi)
        count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Collecting {}".format(count),
            (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    
    # p2img = p2(frame)
    # cv2.imshow("p2",p2img)
    # cv2.imshow("thresh",thresh)
    cv2.imshow("Collecting images", frame)

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q'):
        break

print("\n{} image(s) saved to {}".format(count, IMG_CLASS_PATH))
cap.release()
cv2.destroyAllWindows()
