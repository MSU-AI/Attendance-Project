import cv2


# Load the cascade (the template that will be used to recognize faces!)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# To capture video from your webcam 
cap = cv2.VideoCapture(0)

while True:
    # Read the current frame in the VideoCapture
    frame = cap.read()[1]
    
    # Working with images as color images is computationally expensive. One workaround
    # is to convert the frame to grayscale (each pixel is less heavy but contains
    # equal information)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ####################### Detect the faces #################################
    ###### Hint: use the detectMultiScale method on face_cascade #############
    
    # What does this do? (Should be a float greater than 1)
    scale_factor = 1.3
    # What does this do? (Should be a positive integer)
    min_neighbors = 3
    
    # call detectMultiScale on the cascade and pass the frame and the previous variables
    faces = face_cascade.detectMultiScale(gray,scale_factor,min_neighbors)
    
    ##########################################################################    
    
    
    ############ Draw the rectangle around each face #########################
    # Note: Each face recognized in faces will be stored as a tuple of
    # (topLeft x coordinate, topLeft y coordinate, width, height)
    for (x, y, w, h) in faces:
        topLeft_coords = (x,y)
        # You have topLeft coordinates, how do you obtain the bottomRight coords with the height and width??
        bottomRight_coords = (x+w,y+h)
        rectangle_color = (0,0,255)  # (R, G, B)
        thickness = int(2)
        
        # Now call the cv2.rectangle function with those variables and the frame
        cv2.rectangle(frame,topLeft_coords,bottomRight_coords,rectangle_color,thickness)
    # The frame should contain the rectangle around the face
    # Display the frame
    cv2.imshow("Face Recognition. Press 'q' to quit.", frame)

    # Refresh every 30ms and check if any key is pressed
    # Try tweaking the refresh rate too
    k = cv2.waitKey(30) & 0xff 
    
    # If the key pressed was 'q' exit the loop
    if k == ord('q'):
        break
        
# Destroy the video window and release the video capture
cv2.destroyAllWindows()
cap.release()

# Face cascade is not the only one, can you try to recognize other objects with different cascades?

