import cv2.cv2 as cv2
import numpy as np


def preprocess_image(image, light_image):

    noise_image = np.zeros(image.shape, np.uint8)

    cv2.medianBlur(image, 3, noise_image)

    img32 = np.float32(noise_image)
    light32 = np.float32(light_image)
    #
    devided = np.divide(img32, light32)

    sub_result = 1 - devided

    aux = abs(255 * sub_result)
    light_removed_image = np.uint8(aux)

    threshold_image = np.zeros(image.shape, np.uint8)
    cv2.threshold(light_removed_image, 50, 255, cv2.THRESH_BINARY, threshold_image)

    if threshold_image.ndim == 3:
        threshold_image = cv2.cvtColor(threshold_image, cv2.COLOR_RGB2GRAY)

    return threshold_image


def extract_feautre(threshold_image):

    # cv2.cvtColor(self.threshold_image, cv2.COLOR_RGB2GRAY, self.threshold_image)

    # print(threshold_image.shape)

    # circles = cv2.HoughCircles(threshold_image, cv2.HOUGH_GRADIENT, 1.2, 100)


    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours))

    features = []

    for i in range(0, len(contours)):

        mask = np.zeros(threshold_image.shape, np.uint8)
        cv2.drawContours(mask, contours, i, 1, cv2.FILLED, cv2.LINE_8, hierarchy, 1)

        area = np.sum(mask)
        # print(area)

        if area > 500:
            #The output of cv2.minAreaRect() is ((x, y), (w, h), angle)
            rect = cv2.minAreaRect(contours[i])

            # print(hierarchy[0][i])

            # print(rect)
            width = rect[1][0]
            height =rect[1][1]

            ar= height/width if width < height else width/height

            hole = 1 if hierarchy[0][i][2] > 0 else 0



            features.append(tuple(((area, ar, hole), rect[0])))

    return features