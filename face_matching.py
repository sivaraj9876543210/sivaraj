import face_recognition
from PIL import Image, ImageDraw
import pytesseract
import argparse
import cv2
import os


def match_face(image):

    # load image and prepare drawing
    pic = face_recognition.load_image_file(image)
    face_locations = face_recognition.face_locations(pic)
    pill_image = Image.fromarray(pic)
    mock_image = ImageDraw.Draw(pill_image)

    # face recognition and segmentation
    recogn = face_recognition.face_encodings(pic, face_locations)

    real_locations = [face_locations[0], face_locations[0]]
    face_real = [recogn[0], recogn[0]]
    face_lic = recogn[1]

    faces_encodings = [
        recogn[0],
        recogn[1]
    ]

    faces_names = [
        "real",
        "lic"
    ]

    # highlight just the real face
    '''
    for (top, right, bottom, left), recogn in zip(real_locations, face_real):
        # Draw a box around the face using the Pillow module
        mock_image.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    '''

    # highlight real and license face
    for (top, right, bottom, left), recogn in zip(face_locations, recogn):
        # Draw a box around the face using the Pillow module
        mock_image.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # perform match
    matches = face_recognition.compare_faces(face_real, face_lic)
    print('Match: ' + str(matches[0]))

    return 'true' if matches[0] else 'false'

    # show face segmentation
    #pill_image.show()


def get_license_info(imagename):

    #load the example image and convert it to grayscale
    image = cv2.imread(imagename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file

    text = pytesseract.image_to_string(Image.open(filename))
    print(text)
    os.remove(filename)

    #Dictionary
    text_ascii= text.encode('ascii','ignore')
    print (text_ascii)

    list=text_ascii.split()

    t=0
    p=0
    for num in range(len(list)):
        word=list[num]
        if word[0] == "1" and t==0:
            Surname=list[num+1]
            t=1;
        elif word[0]=="2" and p==0:
            Name=list[num+1]
            p=1

    dic={
      "Name": Name,
      "Surname": Surname,
    }

    return dic
