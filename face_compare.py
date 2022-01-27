#import face_recognition
from simple_facerec import SimpleFacerec
import cv2


#loadnthe camera

cap = cv2.VideoCapture(0)


#Encode faces from folder

sfr = SimpleFacerec()

sfr.load_encoding_images("/Users/abdullahbaqai/Desktop/MSU AI/images/")


while True:
    ret, frame = cap.read()
    
    #detect faces
    face_locations, face_names = sfr.detect_known_faces(frame)   
    
    #Draw rectangle and print names
    
    for face_loc, name in zip(face_locations, face_names):
        
        y1,x1,y2,x2 = face_loc[0],face_loc[1],face_loc[2],face_loc[3]
        
        cv2.putText(frame,name,(x1,y1 - 10),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2)
        
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,200),2)
    
    cv2.imshow('Frame',frame)
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
    
cap.release()

cv2.destroyAllWindows()