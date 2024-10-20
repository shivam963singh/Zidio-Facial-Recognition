import cv2 as cv
import pickle
import numpy as np
import os

#  harcascade algorithm for Face detection 
harcascade = ('data/Model/haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)
faces_data=[] # creating a empty list to store face data 
i =0 
name = input("Enter your Name: ")
cap.set(3,440) # width
cap.set(4,380) # height
while True: 
    sucess,img =cap.read()
    facecascade =cv.CascadeClassifier(harcascade)
    img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY) # converting image to gray scale

    face = facecascade.detectMultiScale(img_gray,1.3,4)

    for(x,y,w,h) in face:
        crop_img = img[y:y+h,x:x+w, :]
        resized_img = cv.resize(crop_img,(50,50))
        if len(faces_data)<= 100 and i%10 ==0:
            faces_data.append(resized_img)
        i=i+1
        cv.putText(img,str(len(faces_data)),(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(50,0,210),1)
        cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0,),5)

    cv.imshow("Face is ",img)
    if cv.waitKey(1) & 0xFF == ord('q') or len(faces_data) == 100:
        break

cap.release()
cv.destroyAllWindows()
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100,-1)

#making a names and face file using pickle library 

if 'names.pkl' not in os.listdir('data/datas/'): # if it's not present create it 
    names = [name]*100
    with open('data/datas/names.pkl','wb') as f:
        pickle.dump(names,f)
else:
    with open('data/datas/names.pkl','rb') as f:
         names = pickle.load(f)
    names = names + [name]*100
    with open('data/datas/names.pkl','wb') as f:
        pickle.dump(names,f)

if 'faces_data.pkl' not in os.listdir('data/datas/'): # if it's not present create it 
    with open('data/datas/faces_data.pkl','wb') as f:
        pickle.dump(faces_data,f)
else:
    with open('data/datas/faces_data.pkl','rb') as f:
        faces_data = pickle.load(f)
    faces = np.append(faces,faces_data,axis=0)
    with open('data/datas/faces_data.pkl','wb') as f:
        pickle.dump(names,f)