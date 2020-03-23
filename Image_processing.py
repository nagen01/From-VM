# -*- coding: utf-8 -*-
"""
Spyder Editor

This Program captures the image from webcam, process with
AWS cognitive services, Compares what you said is same as expected or not
"""
import cv2
import boto3
from contextlib import closing
from pygame import mixer
#import json
import speech_recognition as sr
import pyttsx3
import re

r = sr.Recognizer()
with sr.Microphone() as source:
    #r.adjust_for_ambient_noise(source)
    print("Who are you boy or girl ?")
    engine = pyttsx3.init()
    engine.say('Who are you boy or girl ?')
    engine.runAndWait()
    audio = r.listen(source)
    
    user_input_found = False
    input_gender_found = False
    try:
        text = r.recognize_google(audio)
        print('You said : {}'.format(text))
        user_input = ('{}'.format(text))
        user_input_found = True
    except:
        print("Sorry couldn't recognize your voice")

if user_input_found:
    print(user_input)
    man_match = re.search('boy',user_input)
    woman_match = re.search('girl',user_input)
    if man_match:
        input_gender = 'man'
        input_gender_found =True
    elif woman_match:
        input_gender = 'woman'
        input_gender_found = True
    else:
        print('Tell your gender correctly')
        engine.say('Tell your gender correctly')
        engine.runAndWait()

if input_gender_found:
    print(input_gender)
else:
    print('Gender not found')

video=cv2.VideoCapture(0)
check, frame = video.read()
#cv2.imshow("Color Frame",frame)
cv2.imwrite('test.jpg',frame)

#if __name__ == "__main__":
#    client=boto3.client('rekognition', region_name='eu-west-1')
#    image = open('test.jpg','rb')
#    response = client.detect_lab2els(Image={'Bytes': image.read()},MinConfidence=50)    
    #response = client.detect_text(Image={'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()})
	
if __name__ == "__main__":    
    client=boto3.client('rekognition', region_name='eu-west-1')    

    response = client.detect_labels(Image={'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()},MinConfidence=50)
    print('Detected labels')
    gender_present = False
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        print(type(label['Confidence']))
        #if label['Name'] == 'Human':# and label['Confidence'] > 80.0:
        #    person = label['Name']
        #if label['Name'] == 'Person':# and label['Confidence'] > 80.0:
        #    person = label['Name']
        if label['Name'] == 'Man':# and label['Confidence'] > 70.0:
            gender = label['Name']
            gender_present = True            
        if label['Name'] == 'Woman':# and label['Confidence'] > 70.0:
            gender = label['Name']
            gender_present = True

#print(person)
#print(gender)
#if gender_present:
#    print('Gender found')
#else:
#    print('Gender not found')
            
    if gender_present:
        response = client.detect_moderation_labels(Image={'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()})
        unwanted_content__not_found = True
        #print('Unwanted content')
        #print('Detected labels for ' + photo)    
        for label in response['ModerationLabels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))
            print (label['ParentName'])
            unwanted_content__not_found = False
               
        response = client.detect_faces(Image={'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()},Attributes=['ALL'])
        if unwanted_content__not_found: 
            #print('Detected faces for ' + frame)    
            for faceDetail in response['FaceDetails']:
                if input_gender_found:
                    if input_gender == gender.lower():                        
                        my_text = ('Yes you are ' + gender + ' between ' + str(faceDetail['AgeRange']['Low']) 
                              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
                    else:                        
                        my_text = ('You are telling a lie actually you are a ' + gender + ' between ' 
                              + str(faceDetail['AgeRange']['Low']) 
                              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
                else:                        
                    my_text = ('Either you are not telling or we could not recognize your gender but we are able to detect you as a ' + gender 
                          + ' between ' + str(faceDetail['AgeRange']['Low'])                           
                          + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        else:
            my_text = ('Image has unwanted content')
            #print('Here are the other attributes:')
            #print(json.dumps(faceDetail, indent=4, sort_keys=True))

    client=boto3.client('polly', region_name='eu-west-1')	
    print(my_text)
	
    response = client.synthesize_speech(Text=my_text, OutputFormat='mp3', VoiceId='Joanna')
    
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            data = stream.read()
            fo = open("pollytest.mp3", "wb")
            fo.write( data )
            fo.close()   
    
    mixer.init()
    mixer.music.load("pollytest.mp3")
    mixer.music.play()
	
cv2.waitKey(0)
cv2.destroyAllWindows()

