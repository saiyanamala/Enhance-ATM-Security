from tkinter import *
import tkinter as tk
from tkinter import messagebox
import time
import pyttsx3 as sp
import cv2
import sqlite3 as sql
from datetime import datetime
import requests
import base64
from io import BytesIO
from PIL import Image
import face_recognition
import random
import string
from twilio.rest import Client


def atmsay(output):
    spkear=sp.init()
    rate=spkear.getProperty('rate')
    spkear.setProperty('rate',185)
    spkear.say(output)
    say=spkear.runAndWait()
    return say

def generate_otp(length=6):
    global otp
    otp = ''.join(random.choices(string.digits, k=length))
    return otp



def sms(url_link,phone):
            num=generate_otp()
            account_sid='AC1f6986778bdb80394ef7749a8f6446f0'
            auth_token='24c07b6f33589fb6c7189c89052b0a75'
            client=Client(account_sid,auth_token)
            message=client.messages.create(body='the user image link '+url_link+' and the otp :'+num,from_='+17753709200',to='+91'+phone)


def upload_image_to_imgbb( image_path):
    api_key="7cc8b981a8bd4bd83c205dd38930031f"
    endpoint = "https://api.imgbb.com/1/upload"

    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    
    data = {
        "key": api_key,
        "image": base64_image,
    }

    
    response = requests.post(endpoint, data=data)

    
    json_response = response.json()

    
    if json_response["success"] == True:
        return json_response['data']['url']
    else:
        
        return None



root=tk.Tk()
root.title('ATM Assistent')
root.geometry('1080x720')
frame1=Frame(root,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
frame1.place(x=0,y=0)

l1=Label(root,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
l1.place(x=430,y=260)

l2=Label(root,text='Please enter the ATM card number',font=("ArialGreek 15"),bg='#8DFC04')
l2.place(x=400,y=320)

def imageCapture():
    imageCapture=Toplevel(root)
    imageCapture.title("ATM Assistent")
    imageCapture.geometry('1080x720')

    frame2=Frame(imageCapture,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
    frame2.place(x=0,y=0)

    l1=Label(imageCapture,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
    l1.place(x=430,y=260)

    l2=Label(imageCapture,text='please click the continue button for further steps',font=("ArialGreek 15"),bg='#8DFC04')
    l2.place(x=310,y=320)
    def imagetodatabase():
        global entered_otp
        conn = sql.connect('ATMdata.db')
        cursor = conn.cursor()

        image_id=id.get()
        cursor.execute('SELECT IMAGE FROM IMAGES WHERE id = ?', (image_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            image_data = result[0]
            image = Image.open(BytesIO(image_data))
            image.save('output_image.jpg')

        face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        cap=cv2.VideoCapture(0)
        while True:
                    ret,frame=cap.read()
                    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                    faces=face_cascade.detectMultiScale(gray,minNeighbors=5,minSize=(30,30))
                    if len(faces)>0:
                        cv2.imwrite('test.jpg',frame)
                        atmsay('captured')
                        break
                    else:
                        atmsay("make face clear")
        cap.release()




        image_of_person1 = face_recognition.load_image_file('output_image.jpg')
        image_of_person2 = face_recognition.load_image_file('test.jpg')


        encoding_of_person1 = face_recognition.face_encodings(image_of_person1)[0]
        encoding_of_person2 = face_recognition.face_encodings(image_of_person2)[0]


        results = face_recognition.compare_faces([encoding_of_person1], encoding_of_person2)


        if results[0]:
            l3=Label(imageCapture,text='pleas click the ok button for atm operations',font=("ArialGreek 15"),bg='#8DFC04')
            l3.place(x=600,y=520)
            atmopbtn=Button(imageCapture,text="Ok",width=20,height=0,command=pincheck).place(x=700,y=560)
        else:
            user_image_url=upload_image_to_imgbb('test.jpg')
            conn = sql.connect('ATMdata.db')
            cursor = conn.cursor()

            image_id=id.get()
            cursor.execute('SELECT PHONE_NO FROM IMAGES WHERE id = ?', (image_id,))
            result = cursor.fetchone()
            conn.close()

            phone=result[0]

            sms(user_image_url,phone)
            atmsay('sms was sent')
            l4=tk.Label(imageCapture,text='please enter the otp',font=("ArialGreek 15"),bg='#8DFC04')
            l4.place(x=600,y=520)
            entered_otp=tk.Entry(imageCapture,font=('Arial',14))
            entered_otp.place(x=700,y=560)
            atmopbtn=Button(imageCapture,text="enter",width=20,height=0,command=checkotp).place(x=700,y=600)
            


        
    imagebtn=Button(imageCapture,text="Continue",width=20,height=0,command=imagetodatabase).place(x=440,y=360)
def checkotp():
    if(entered_otp.get()==otp):
        pincheck()
    else:
        atmsay("not allowed to use atm")
def pincheck():
    pincheck=Toplevel(root)
    pincheck.title("ATM Assistent")
    pincheck.geometry('1080x720')

    frame2=Frame(pincheck,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
    frame2.place(x=0,y=0)

    l1=Label(pincheck,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
    l1.place(x=430,y=260)
    
    l2=Label(pincheck,text='please enter the ATM PIN number',font=("ArialGreek 15"),bg='#8DFC04')
    l2.place(x=350,y=320)

    e=tk.Entry(pincheck,show='X',font=('Arial',14))
    e.place(x=440,y=360)
    def verify():
        pin=str(e.get())
        if pin==data["pin"]:
            atmoperations()
        else:
            tk.messagebox.showwarning("wrong password","Invalid Password")

    confrimbtn=Button(pincheck,text="CONFRIM",width=20,height=0,command=verify).place(x=460,y=400)

def atmoperations():
    atmoperations=Toplevel(root)
    atmoperations.title("ATM Assistent")
    atmoperations.geometry('1080x720')

    frame2=Frame(atmoperations,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
    frame2.place(x=0,y=0)

    l1=Label(atmoperations,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
    l1.place(x=430,y=260)
    
    l2=Label(atmoperations,text='please select the operation to perform',font=("ArialGreek 15"),bg='#8DFC04')
    l2.place(x=350,y=320)

    withdrawalbtn=Button(atmoperations,text="WITHDRAWAL",width=20,height=0,command=withdrawal).place(x=100,y=550)
    rechargebtn=Button(atmoperations,text="RECHARGE",width=20,height=0,command=recharge).place(x=100,y=620)
    balancebtn=Button(atmoperations,text="BALANCE",width=20,height=0,command=balance).place(x=800,y=550)
    depositbtn=Button(atmoperations,text="DEPOSIT",width=20,height=0,command=deposit).place(x=800,y=620)
def withdrawal():
    withdrawal=Toplevel(root)
    withdrawal.title("ATM Assistent")
    withdrawal.geometry('1080x720')

    frame2=Frame(withdrawal,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
    frame2.place(x=0,y=0)

    l1=Label(withdrawal,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
    l1.place(x=430,y=260)
    l2=Label(withdrawal,text='Enter the amount',font=("ArialGreek 15"),bg='#8DFC04')
    l2.place(x=350,y=320)

    e=tk.Entry(withdrawal,show=None,font=('Arial',14))
    e.place(x=440,y=360)
    def wioper():
        if(data['amount']>0 and int(e.get())<=data['amount']) and int(e.get())>100 and int(e.get())%100==0:
            data['amount']=data['amount']-int(e.get())
            atmsay("please wait while transaction is processing")
            time.sleep(10)
            atmsay('please collect money')
            tk.messagebox.showinfo("withdrawal","please collect money")
        else:
            atmsay("You account not have sufficient and valid amount") 
    conbtn=Button(withdrawal,text="CONFRIM",width=20,height=0,command=wioper).place(x=460,y=400)

def deposit():
    deposit=Toplevel(root)
    deposit.title("ATM Assistent")
    deposit.geometry('1080x720')

    frame2=Frame(deposit,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
    frame2.place(x=0,y=0)

    l1=Label(deposit,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
    l1.place(x=430,y=260)
    l2=Label(deposit,text='Deposit Amount here',font=("ArialGreek 15"),bg='#8DFC04')
    l2.place(x=410,y=320)
    l3=Label(deposit,text='Account Number',font=("ArialGreek 15"),bg='#8DFC04')
    l3.place(x=300,y=400)

    e1=tk.Entry(deposit,show=None,font=('Arial',15))
    e1.place(x=500,y=400)

    l4=Label(deposit,text='Enter Amount',font=("ArialGreek 15"),bg='#8DFC04')
    l4.place(x=300,y=450)

    e2=tk.Entry(deposit,show=None,font=('Arial',15))
    e2.place(x=500,y=450)
    

    def deop():
        if data['account.no']==str(e1.get()) and int(e2.get())%100==0:
            atmsay("please place the money at the deposit holder")
            time.sleep(5)
            data['amount']=data['amount']+int(e2.get())
            atmsay("the money was deposited into your account")
            tk.messagebox.showinfo("deposit","the money was deposited into your account")
        else:
            atmsay("Enter the valid details")
            
    conbtn=Button(deposit,text="CONFRIM",width=20,height=0,command=deop).place(x=390,y=500)        
            

def recharge():
    recharge=Toplevel(root)
    recharge.title("ATM Assistent")
    recharge.geometry('1080x720')

    frame2=Frame(recharge,width=1080,height=720,relief=RIDGE,borderwidth=5,bg='#8DFC04')
    frame2.place(x=0,y=0)

    l1=Label(recharge,text='RGUKT ATM',font=("ArialGreek 20 bold"),bg='#8DFC04')
    l1.place(x=430,y=260)
    l2=Label(recharge,text='Recharge Mobial here',font=("ArialGreek 15"),bg='#8DFC04')
    l2.place(x=410,y=320)
    l3=Label(recharge,text='Phone NO',font=("ArialGreek 15"),bg='#8DFC04')
    l3.place(x=300,y=400)

    e1=tk.Entry(recharge,show=None,font=('Arial',15))
    e1.place(x=500,y=400)

    l4=Label(recharge,text='Enter Amount',font=("ArialGreek 15"),bg='#8DFC04')
    l4.place(x=300,y=450)

    e2=tk.Entry(recharge,show=None,font=('Arial',15))
    e2.place(x=500,y=450)

    def rech():
        if data['amount']>=int(e2.get()):
            data['amount']=data['amount']-int(e2.get())
            atmsay("you recharge is successfull")
            tk.messagebox.showinfo("recharge","you recharge is successfull")
        else:
            atmsay("your account not have sufficient balance")

    conbtn=Button(recharge,text="CONFRIM",width=20,height=0,command=rech).place(x=390,y=500)

def balance():
    atmsay("please check your balance in the information box")
    tk.messagebox.showinfo("recharge","Aval Balance:"+str(data['amount']))


global id
id=Entry(root,show=None,font=('Arial',14))
id.place(x=420,y=360)
insertbtn=Button(root,text="ENTER",width=20,height=0,command=imageCapture).place(x=460,y=390)

root.mainloop()
