import random

import cv2.cv2 as cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel
from sklearn import metrics
from sklearn.svm import SVC

import classify_utils
import demo_utils


class ClassificationWidget(QWidget):

    def __init__(self):
        super(ClassificationWidget, self).__init__()

        self.btn = QPushButton("Load Image", self)
        self.btn.clicked.connect(self.load_image)
        self.btn.resize(100, 30)
        self.btn.move(10, 10)

        self.prepare_btn = QPushButton("Prepare Data", self)
        self.prepare_btn.clicked.connect(self.prepare_data)
        self.prepare_btn.resize(120, 30)
        self.prepare_btn.move(356, 10)

        self.image_label = QLabel(self)
        self.image_label.setText("image")
        self.image_label.resize(320, 240)
        self.image_label.move(10, 50)
        self.image_label.setStyleSheet("border: 1px solid red")

        self.threshold_label = QLabel(self)
        self.threshold_label.setText("threshold image")
        self.threshold_label.resize(320, 240)
        self.threshold_label.move(356, 50)
        self.threshold_label.setStyleSheet("border: 1px solid red")

        self.cv_svm_btn = QPushButton("OpenCV SVM", self)
        self.cv_svm_btn.clicked.connect(self.classify_cv_svm)
        self.cv_svm_btn.resize(120, 30)
        self.cv_svm_btn.move(10, 310)

        self.result_label = QLabel(self)
        self.result_label.setText("result")
        self.result_label.resize(320, 240)
        self.result_label.move(10, 350)
        self.result_label.setStyleSheet("border: 1px solid red")

        self.sklearn_svm_btn = QPushButton("sklearn SVM", self)
        self.sklearn_svm_btn.clicked.connect(self.classify_sklearn_svm)
        self.sklearn_svm_btn.resize(120, 30)
        self.sklearn_svm_btn.move(356, 310)

        self.result_label2 = QLabel(self)
        self.result_label2.setText("sklearn result")
        self.result_label2.resize(320, 240)
        self.result_label2.move(356, 350)
        self.result_label2.setStyleSheet("border: 1px solid red")

        self.image = None
        self.light_image = None
        self.threshold_image = None

        self.features = []

        self.training_data = None
        self.responses_data = None

        self.test_data = None
        self.test_responses_data = None

        self.svm = None

    def load_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './classify_data', "Image files (*.jpg *.png *.pgm)")

        if len(fname) > 0:
            self.image = cv2.imread(fname)

            demo_utils.show_cvimage_to_label(self.image, self.image_label)
            self.light_image = cv2.imread('./classify_data/pattern.pgm')

            self.threshold_image = classify_utils.preprocess_image(self.image, self.light_image)

            demo_utils.show_cvimage_to_label(self.threshold_image, self.threshold_label)

    def prepare_data(self):

        training_list =[]
        responses_list = []
        test_list = []
        test_responses_list = []

        num_for_test= 20

        self.load_train_data("./classify_data/nut/tuerca_%04d.pgm", 0, num_for_test, training_list, responses_list, test_list, test_responses_list)
        self.load_train_data("./classify_data/ring/arandela_%04d.pgm", 1, num_for_test, training_list, responses_list, test_list, test_responses_list)
        self.load_train_data("./classify_data/screw/tornillo_%04d.pgm", 2, num_for_test, training_list, responses_list, test_list, test_responses_list)

        print("Num of train samples: %d " % len(responses_list))
        print("Num of test samples: %d " % len(test_responses_list))

        self.training_data = np.array([ x[0] for x in training_list] , dtype=np.float32)
        self.responses_data = np.array(responses_list, dtype=np.int32)

        self.test_data = np.array([ x[0] for x in test_list], dtype=np.float32)
        self.test_responses_data = np.array(test_responses_list, dtype=np.int32)

        print(self.training_data.shape)

        print(self.responses_data.shape)

    def load_train_data(self, folder, label, num_for_test, training_list, responses_list, test_list, test_response_list):
        vc = cv2.VideoCapture()

        ret = vc.open(folder)

        print("open result:" + str(ret))

        if not ret:
            return False

        index = 0
        while True:
            ret, frame = vc.read()

            if not ret:
                break

            pre_image = classify_utils.preprocess_image(frame, self.light_image)

            features = classify_utils.extract_feautre(pre_image)

            for i in range(0, len(features)):

                # if int(label) == 2 and int(features[i][0][2]) == 1:
                #     print("found violation")
                #     print(features[i][0])

                if index >= num_for_test:
                    training_list.append(features[i])
                    responses_list.append(label)

                else:
                    test_list.append(features[i])
                    test_response_list.append(label)

                index += 1

        return True

    def classify_cv_svm(self):

        self.svm = cv2.ml.SVM_create()
        self.svm.setType(cv2.ml.SVM_C_SVC)
        self.svm.setNu(0.05)
        self.svm.setKernel(cv2.ml.SVM_CHI2)
        self.svm.setDegree(1.0)

        # self.svm.setC(2.67)
        self.svm.setGamma(2.0)
        # TermCriteria(TermCriteria::MAX_ITER, 100, 1e-6));
        self.svm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1.e-06))

        self.svm.train(self.training_data, cv2.ml.ROW_SAMPLE, self.responses_data)
        # self.svm.save('svm_data.dat')

        result = self.svm.predict(self.test_data)

        print(result[1].shape)

        print(self.test_responses_data.shape)

        # result = np.aarray(result, dtype=np.int32)

        result1 = np.array([x[0] for x in result[1]], dtype=np.int32)

        print(result1.shape)

        mask = result1 == self.test_responses_data
        correct = np.count_nonzero(mask)
        print("Accuracy cv svm: %0.4f" % (correct * 100.0 / len(result1)))
        output = self.image.copy()

        font = cv2.FONT_HERSHEY_SIMPLEX

        # fontScale
        fontScale = 0.5

        # Blue color in BGR
        color1 = (255, 0, 0)

        # Line thickness of 2 px
        thickness = 1

        self.features = classify_utils.extract_feautre(self.threshold_image)
        print(self.features)

        for i in range(0, len(self.features)):

            sample_data = np.array([self.features[i][0]], dtype=np.float32)

            # print(sample_data.shape)

            result = self.svm.predict(sample_data)

            print(self.features[i][0])
            print(result[1][0][0])

            label = int(result[1][0][0])

            org = (int(self.features[i][1][0]), int(self.features[i][1][1]))

            if label == 0:
                color = (255, 0, 0)
                text = "NUT"
            elif label == 1:
                color = (0, 255, 0)
                text = "RING"
            else:
                color = (0, 0, 255)
                text = "SCREW"

            output = cv2.putText(output, text, org, font,
                                 fontScale, color, thickness)

            demo_utils.show_cvimage_to_label(output, self.result_label)

    def classify_sklearn_svm(self):

        svc = SVC()
        svc.fit(self.training_data, self.responses_data)

        predicted = svc.predict(self.test_data)
        print("Confusion matrix:\n%s" %
        metrics.confusion_matrix(self.test_responses_data,
                                   predicted))
        print("Accuracy: %0.4f" % metrics.accuracy_score(self.test_responses_data,
                                                     predicted))

        output = self.image.copy()

        font = cv2.FONT_HERSHEY_SIMPLEX

        # fontScale
        fontScale = 0.5

        # Blue color in BGR
        color1 = (255, 0, 0)

        # Line thickness of 2 px
        thickness = 1

        self.features = classify_utils.extract_feautre(self.threshold_image)
        print(self.features)

        for i in range(0, len(self.features)):

            sample_data = np.array([self.features[i][0]], dtype=np.float32)

            # print(sample_data.shape)

            result = svc.predict(sample_data)

            print(self.features[i][0])
            print(result[0])

            label = int(result[0])

            org = (int(self.features[i][1][0]), int(self.features[i][1][1]))

            if label == 0:
                color = (255, 0, 0)
                text = "NUT"
            elif label == 1:
                color = (0, 255, 0)
                text = "RING"
            else:
                color = (0, 0, 255)
                text = "SCREW"

            output = cv2.putText(output, text, org, font,
                                 fontScale, color, thickness)

            demo_utils.show_cvimage_to_label(output, self.result_label2)







