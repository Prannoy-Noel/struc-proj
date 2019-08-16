# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\get_boxes.py
# Compiled at: 2019-07-02 11:45:14
# Size of source mod 2**32: 5247 bytes
"""
Created on Fri Jun 21 14:35:46 2019

@author: Darshil
"""
import cv2

def isXinY(x, y):
    if x[0] > y[0] - 10 and x[1] > y[1] - 10 and x[2] < y[2] + 10 and x[3] < y[3] + 10:
        
            return True
    else:
        return False


def isXinY1(x, y):
    if x[0] > y[0] and x[1] > y[1] and x[2] < y[2] and  x[3] < y[3]:
        
            return True
    else:
        return False


def extract_boxes(image_path, to_remove):
    print(image_path)
    img = cv2.imread(image_path, 0)
#    shape = img.shape
    ret, thresh = cv2.threshold(img, 100, 255, 0)
    for item in to_remove:
        x1, y1, x2, y2 = item
        thresh[y1:y2, x1:x2] = 255

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    thresh = cv2.erode(thresh, kernel, iterations=1)
    thresh = 255 - thresh
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_c = cv2.imread(image_path)
    final_contours = []
    box_coords = []
    for i in range(1, len(contours)):
        x = []
        y = []
        for countour in contours[i]:
            y.append(countour[0][0])
            x.append(countour[0][1])

        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        in_flag = False
        for item in to_remove:
            if isXinY(item, [y_min, x_min, y_max, x_max]):
                in_flag = True
                break

        if in_flag == True:
            final_contours.append(contours[i])
            box_coords.append([y_min, x_min, y_max, x_max])

    dont_consider = [False] * len(box_coords)
    for i, item in enumerate(box_coords):
        for j in range(0, len(box_coords)):
            if i != j:
                if isXinY1(box_coords[i], box_coords[j]):
                    dont_consider[j] = True
    print('---------------')
    print(len(box_coords))
    final_boxes = []
    for i, k in enumerate(dont_consider):
        if not k:
            final_boxes.append(box_coords[i])

    print(len(final_boxes))
    for i in range(len(final_boxes)):
        y_min, x_min, y_max, x_max = final_boxes[i]
        cv2.rectangle(img_c, (y_min, x_min), (y_max, x_max), (0, 255, 0), 3)

#    cv2.imwrite(image_path[:-4] + '_boxes_original.jpg', img_c)
    return final_boxes


if __name__ == '__main__':
    dest_dir = 'C:\\Users\\IBM_ADMIN\\Desktop\\RICOH\\R&D\\box tree hierarchy\\data'
    image_path = 'C:\\Users\\IBM_ADMIN\\Desktop\\RICOH\\R&D\\box tree hierarchy\\data\\8_000003.tif'
    extract_table(dest_dir, image_path)
# okay decompiling get_boxes.cpython-36.pyc
