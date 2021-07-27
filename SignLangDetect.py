from typing import ItemsView
from asyncio.tasks import sleep
import cv2
import mediapipe as mp
# import os
# import time
import asyncio
import pyrebase
# import firebase_admin
# from firebase_admin import credentials, messaging
from datetime import datetime
from pusher_push_notifications import PushNotifications

# config Firebase
config = {
    "apiKey" : "AIzaSyDkFn3LdpjPly4w31eL6CAQIktzSclaMg0",
    "authDomain" : "astroapp-cbf26.firebaseapp.com",
    "databaseURL" : "https://astroapp-cbf26-default-rtdb.firebaseio.com",
    "projectId" : "astroapp-cbf26",
    "storageBucket" : "astroapp-cbf26.appspot.com",
    "serviceAccount" : r"C:\Users\user\env-AstroProject\serviceAccAstro.json"
}

firebaseConnect = pyrebase.initialize_app(config)
# storage = firebase_strorage.storage()
db = firebaseConnect.database()
# cred = credentials.Certificate("serviceAccAstro.json")
# firebase_admin.initialize_app(cred)

pn_client = PushNotifications(
    instance_id='664b9c5f-0e58-442f-a7e4-4f7c7e0c2b87',
    secret_key='A975DDC2A5253248B6DEA2167B6ADBFC20BE8473F27B671D0D50FF1103EA3F7A',
)

#declare
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
# directory = r'D:\satrio\Python-SignLangDetection\output' #output
signGesture = [8, 12, 16, 20]
jempol_sign = 4
now = datetime.now() 
time_stamp = now.strftime("%d-%m-%Y %H-%M-%S")
timeNow = now.strftime("%H-%M")
tanggal = now.strftime("%Y-%m-%d")

# os.chdir(directory) #output Path

#Sign Language Logic
while True :
    ret, img, = cap.read()
    # img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)  
    
    if results.multi_hand_landmarks :
        for hand_landmark in results.multi_hand_landmarks :
            lm_list = []
            for id, lm in enumerate(hand_landmark.landmark) :
                lm_list.append(lm)

            sign_status = []

            for sign in signGesture :
                x, y = int(lm_list[sign].x * w), int(lm_list[sign].y * h)
                cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)

                if lm_list[sign].x < lm_list[sign - 2].x :
                     cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                     sign_status.append(True)
                
                else :
                    sign_status.append(False)

            if all(sign_status) :
                if lm_list[jempol_sign].y < lm_list[jempol_sign - 1].y < lm_list[jempol_sign - 2].y :
                    cv2.putText(img, "MINUM", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 3)
                    print("MINUM")
                    # fileName = f'minum_{time_stamp}.jpg'
                    # cv2.imwrite(fileName, img, [int (cv2.IMWRITE_JPEG_QUALITY), 30])
                    # storage.child(fileName).put(fileName)
                    db.child("Riwayat Aktivitas")
                    dataset = {
                        'nama_aktivitas' : 'Minum',
                        'jam' : timeNow,
                        'tanggal' : tanggal
                    }

                    async def minum ():
                        await asyncio.sleep(2)
                        db.push(dataset)
                    asyncio.run(minum())

                    #cons variable
                    TOPIC = "aktivitas"
                    ALERT_NOTIF = "Report Created"
                    TITLE_NOTIF = "Aktivitas Pasien"
                    BODY_NOTIF = "Pasien membutuhkan minum"
                    response = pn_client.publish(
                        interests=[TOPIC],
                        publish_body={'apns': {'aps': {'alert': ALERT_NOTIF}},
                                        'fcm': {'notification': {'title': TITLE_NOTIF, 'body': BODY_NOTIF}}}
                    )

            elif sign_status == [True, True, True, False]:
                if lm_list[jempol_sign].y < lm_list[jempol_sign - 1].y < lm_list[jempol_sign - 2].y :
                    cv2.putText(img, "MAKAN", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 3)
                    print("MAKAN")
                    # fileName = f'makan_{time_stamp}.jpg'
                    # cv2.imwrite(fileName, img, [int (cv2.IMWRITE_JPEG_QUALITY), 30])
                    # storage.child(fileName).put(fileName)
                    db.child("Riwayat Aktivitas")
                    dataset = {
                        'nama_aktivitas' : 'Makan',
                        'jam' : timeNow,
                        'tanggal' : tanggal
                    }

                    async def makan():
                        await asyncio.sleep(2)
                        db.push(dataset)
                    asyncio.run(makan())
                    
                    #cons variable
                    TOPIC = "aktivitas"
                    ALERT_NOTIF = "Report Created"
                    TITLE_NOTIF = "Aktivitas Pasien"
                    BODY_NOTIF = "Pasien membutuhkan makan"
                    response = pn_client.publish(
                        interests=[TOPIC],
                        publish_body={'apns': {'aps': {'alert': ALERT_NOTIF}},
                                        'fcm': {'notification': {'title': TITLE_NOTIF, 'body': BODY_NOTIF}}}
                    )

            elif sign_status == [False, True, True, True]:
                if lm_list[jempol_sign].y < lm_list[jempol_sign - 1].y < lm_list[jempol_sign - 2].y :
                    cv2.putText(img, "PIPIS", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 3)
                    print("PIPIS")
                    # fileName = f'pipis_{time_stamp}.jpg'
                    # cv2.imwrite(fileName, img, [int (cv2.IMWRITE_JPEG_QUALITY), 30])
                    # storage.child(fileName).put(fileName)
                    db.child("Riwayat Aktivitas")
                    dataset = {
                        'nama_aktivitas' : 'Pipis',
                        'jam' : timeNow,
                        'tanggal' : tanggal
                    }

                    async def pipis():
                        await asyncio.sleep(2)
                        db.push(dataset)
                    asyncio.run(pipis())
            
                    #cons variable
                    TOPIC = "aktivitas"
                    ALERT_NOTIF = "Report Created"
                    TITLE_NOTIF = "Aktivitas Pasien"
                    BODY_NOTIF = "Pasien membutuhkan pergi ke kamar mandi"
                    response = pn_client.publish(
                        interests=[TOPIC],
                        publish_body={'apns': {'aps': {'alert': ALERT_NOTIF}},
                                        'fcm': {'notification': {'title': TITLE_NOTIF, 'body': BODY_NOTIF}}}
                    )

            elif sign_status == [False, False, True, True]: 
                if lm_list[jempol_sign].y < lm_list[jempol_sign - 1].y < lm_list[jempol_sign - 2].y :
                    cv2.putText(img, "PUP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 3)
                    print("PUP")
                    # fileName = f'pup_{time_stamp}.jpg'
                    # cv2.imwrite(fileName, img, [int (cv2.IMWRITE_JPEG_QUALITY), 30])
                    # storage.child(fileName).put(fileName)
                    db.child("Riwayat Aktivitas")
                    dataset = {
                        'nama_aktivitas' : 'Pup',
                        'jam' : timeNow,
                        'tanggal' : tanggal
                    }

                    async def pup():
                        await asyncio.sleep(2)
                        db.push(dataset)
                    asyncio.run(pup())

                    #cons variable
                    TOPIC = "aktivitas"
                    ALERT_NOTIF = "Report Created"
                    TITLE_NOTIF = "Aktivitas Pasien"
                    BODY_NOTIF = "Pasien membutuhkan pergi ke kamar mandi"
                    response = pn_client.publish(
                        interests=[TOPIC],
                        publish_body={'apns': {'aps': {'alert': ALERT_NOTIF}},
                                        'fcm': {'notification': {'title': TITLE_NOTIF, 'body': BODY_NOTIF}}}
                    )
            
            mp_draw.draw_landmarks(img, hand_landmark,
                                   mp_hands.HAND_CONNECTIONS,
                                   mp_draw.DrawingSpec((0, 0, 255), 2, 2),
                                   mp_draw.DrawingSpec((0, 255, 0), 4, 2)
                                   )

            
    cv2.imshow("ASTRO Sign Language", img)
   
    if cv2.waitKey(1) == ord('q') :
        break
    
