#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 12:49:56 2019

@author: nilesh
"""
#importing libraries
import cv2,os,pickle
import face_recognition as fr

#creating blank lists
known_face_encodings_list=[]
known_names=[]
ids=[]
font=cv2.FONT_HERSHEY_SIMPLEX

#creating image's directory
try:
    cwd=os.getcwd()
    print(cwd)
    os.mkdir(cwd+"/dataset_images")
except:
    print()

#funtions for Capturing image
def image_taker(dir_name,student_id):
    cam=cv2.VideoCapture(0)
    counter=0
    flag=0  

    while cam.isOpened():
        frame=cam.read()[1]
        
        #converting BGR frame to RGB frame
        rgb_frame=frame[:,:,::-1]
        
        #getting locations of faces present
        faces=fr.face_locations(rgb_frame)
        for (top,right,bottom,left) in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
        cv2.putText(frame, "Press 'C' to capture image", (0 , 35), font, 1.0, (255, 255, 255), 2)
        cv2.imshow("live",frame)
            
            #handler
        if cv2.waitKey(100) & 0xFF==ord('q'):
            if flag==0:
                #remove if image is not created to avoid any issue
                os.rmdir(dir_name)
            break
        if cv2.waitKey(100) & 0xFF==ord('c'):
            
            #saving imaegs
            cv2.imwrite(dir_name+"/image,"+str(student_id)+","+str(counter)+".jpg",frame)
            flag=1
            print("captured")
            cv2.destroyAllWindows()
    cam.release()
    cv2.destroyAllWindows()
   
    
    
     

#setting up student Id
choice='y'

#getting last student id and creating next id
try:
    with open("ids.txt",'rb') as file_data:
        labels=pickle.load(file_data)
    student_id=max(labels)+1
except FileNotFoundError:
    student_id=0
    
while(choice=='y'):
    
    print(student_id)

    student_name=input("Enter student name: ")
    
    #defining directory name where images will be stored
    cwd=os.getcwd()+"/dataset_images/"
    dir_name=cwd+student_name+","+str(student_id)
    
    #using try to avoid error when directory is already present
    try:
        os.mkdir(dir_name)
        print("check")
        image_taker(dir_name,student_id)
        print("check")
    except:
        print("Student name already exits.")
    
    choice=input("Add another:")
    if choice=='y':
        student_id=student_id+1
    


#getting face encoding from stored images
dataset_dir_name=os.getcwd()+"/dataset_images"
folder_names=os.listdir(dataset_dir_name)
for i in folder_names:
    dir_name=dataset_dir_name+"/"+i
    face_names=os.listdir(dir_name)
    for face_name in face_names:
        image_name=dir_name+"/"+face_name
        print(image_name)
        
        
        #loading images using face_recognition library
        known_face= fr.load_image_file(image_name)
        print(known_face)
        
        #getting encodings of faces
        known_face_encoding=fr.face_encodings(known_face)[0]
        student_name=i.split(",")[0]
        student_id_in=int(i.split(",")[1])
        
        #appending encodings,ids, names into lists
        known_face_encodings_list.append(known_face_encoding)
        known_names.append(student_name)
        ids.append(student_id_in)
    

print(known_names)
print(ids)

#storing data in files using pickle
with open("encodings.txt",'wb') as file_data:
    pickle.dump(known_face_encodings_list,file_data)

with open("name.txt",'wb') as file_data:
    pickle.dump(known_names,file_data)

with open("ids.txt",'wb') as file_data:
    pickle.dump(ids,file_data)