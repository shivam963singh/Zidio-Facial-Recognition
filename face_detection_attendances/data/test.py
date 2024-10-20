from sklearn.neighbors import KNeighborsClassifier
import cv2 as cv
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# this voice put voice in the program 

def speak(str1):
      speak = Dispatch(("SAPI.SpVoice"))
      speak.speak(str1)


harcascade = ('data/Model/haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)


with open('data/datas/names.pkl','rb') as f:
        Labels = pickle.load(f)
with open('data/datas/faces_data.pkl','rb') as f:
        FACES = pickle.load(f)

# using KNN algorithm 

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,Labels)

 #adding background imgae

img_background =cv.imread('data/background_modified.png')

print('shapes of Faces Matrix --> ',FACES.shape)

#creating a row and column to store attendance in csv

COL_NAMES = ['NAME','TIME','DATE']

while True: 
        sucess,img =cap.read()
        facecascade =cv.CascadeClassifier(harcascade)
        img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

        face = facecascade.detectMultiScale(img_gray,1.3,4)

        for(x,y,w,h) in face:
                        crop_img = img[y:y+h,x:x+w, :]
                        resized_img = cv.resize(crop_img,(50,50)).flatten().reshape(1,-1)
                        output = knn.predict(resized_img)
                        
                        ts = time.time()
                        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                        timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")
                        exist = os.path.isfile("data/Attendance/Attendance_" + date + ".csv")

                        cv.putText(img,str(output[0]),(x,y-15),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0,),5)
                        attendance =[str(output[0]),str(timestamp),str(date)]
        img_background[162:162 + 480,55:55+640] = img
        cv.imshow("Face is ",img_background)
        k =cv.waitKey(1)
        if k  == ord('o'):
                speak("Attendance Taken..")
                time.sleep(5)
                if exist:
                        with open("data/Attendance/Attendance_" + date +".csv","+a") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(attendance)
                                csvfile.close()
                else:
                        with open("data/Attendance/Attendance_" + date +".csv","+a") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(COL_NAMES)
                                writer.writerow(attendance)
                                csvfile.close()
        if k ==ord('q'):
                break
                

cap.release()
cv.destroyAllWindows()
