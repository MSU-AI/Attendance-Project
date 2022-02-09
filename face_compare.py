#import face_recognition
from simple_facerec import SimpleFacerec
import cv2


#loadnthe camera

cap = cv2.VideoCapture(0)


#Encode faces from folder

sfr = SimpleFacerec()

# Put images you want to recognize in this folder
# Example: (if any bias, the list is generated by GitHub copilot)
# face_images/
#   - elon-musk.jpg
#   - steve-jobs.jpg
#   - mark-zuckerberg.jpg
#   - bill-gates.jpg
#   - donald-trump.jpg
sfr.load_encoding_images("./face_images/")


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
    
    # press q or esc (key 27) to quit
    if key == ord('q') or key == 27:
        break
    
    
cap.release()

cv2.destroyAllWindows()