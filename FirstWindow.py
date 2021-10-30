# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FirstWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import time
from datetime import datetime,timedelta
import datedelta
from passporteye import read_mrz
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
#import figerprint libraries

import tempfile
from datetime import datetime ,timedelta
import uuid
from pyfingerprint.pyfingerprint import PyFingerprint

from SecoundWindow import Ui_SecoundWindow
from OutWindow import Ui_OutWindow
import threading
My_thread = None
thread_res = None
passportId = 0
fingerinfo = [None] * 5
finger_count=0
from dotenv import load_dotenv
load_dotenv()



class Ui_FirstWindow(object):
    def setupUi(self, FirstWindow):
        FirstWindow.setObjectName("FirstWindow")
        FirstWindow.resize(1366, 768)
        FirstWindow.setMinimumSize(QtCore.QSize(1366, 768))
        FirstWindow.setMaximumSize(QtCore.QSize(1366, 768))
        FirstWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(FirstWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.ScanButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ScanButton.setFont(font)
        self.ScanButton.setObjectName("ScanButton")
        self.verticalLayout_2.addWidget(self.ScanButton, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        FirstWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FirstWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 28))
        self.menubar.setObjectName("menubar")
        FirstWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FirstWindow)
        self.statusbar.setObjectName("statusbar")
        FirstWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FirstWindow)
        QtCore.QMetaObject.connectSlotsByName(FirstWindow)
        
        
        #self.ScanButton.clicked.connect(scanPassport)
        #self.ScanButton.clicked.connect(self.finalscr)
        self.ScanButton.clicked.connect(self.Callapi)
        #self.ScanButton.clicked.connect(comparefingers)
    
        self.OutWindow = QtWidgets.QMainWindow()
        self.ui_FinalWindow = Ui_OutWindow()
        self.ui_FinalWindow.setupUi(self.OutWindow)

    
    def secondscr(self,response):
        self.SecoundWindow = QtWidgets.QMainWindow()
        self.ui = Ui_SecoundWindow()
        self.ui.setupUi(self.SecoundWindow)
        self.SecoundWindow.show()
        self.ui.setinfoPassportNum(self.SecoundWindow, "N8608414")
        self.ui.setinfoName(self.SecoundWindow, response["person_data"]["surname"] +" "+ response["person_data"]["other_name"])
        print("info - " ,response["person_data"]["surname"] +""+ response["person_data"]["other_name"])
        self.ui.setinfoSex(self.SecoundWindow,response["person_data"]["sex"]) 
        issued_date = datetime.strptime(response["person_data"]["issued_date"], '%Y-%m-%d').date()
        time_temp = issued_date + datedelta.datedelta(years=10)
        self.ui.setinfoDoE(self.SecoundWindow, str(time_temp))
        global thread_res
        thread_res = response 
        My_thread.start()
        

    def Callapi(self,Passport_id):
        r = requests.get('http://192.168.1.9/passport_db/index.php/person/get_two_fingers/N8608414')
        #r = requests.get('http://192.168.1.7/passport_db/index.php/person/get_two_fingers/'+ Passport_id)
        response = r.json()
        print("Status - ",response["status"])
        print("info - " ,response["person_data"]["surname"] +""+ response["person_data"]["other_name"])
        
        
        if bool(response["status"]) :
            self.secondscr(response)
            
        print("Person id - ",  response["scan_fingers"][0]["person_id"])
        print("Finger id - ",  response["scan_fingers"][1]["person_finger_id"])
            
        
        
    def retranslateUi(self, FirstWindow):
        _translate = QtCore.QCoreApplication.translate
        FirstWindow.setWindowTitle(_translate("FirstWindow", "FirstWindow"))
        self.label.setText(_translate("FirstWindow", "Welcome"))
        self.label_2.setText(_translate("FirstWindow", "Please place your passport on the scanner"))
        self.label_3.setText(_translate("FirstWindow", "Click the SCAN button or Press \"S\""))
        self.ScanButton.setText(_translate("FirstWindow", "SCAN"))

def scanPassport():
    #Current Date & Time
    os.system("date")

    #Instructions
    print (" Passport scanning Process Started...")
    time.sleep(2)
    print (" It will take few seconds...")
    time.sleep(2)
    print (" please wait...")
    time.sleep(2)
    print (" Scanning...")

    #Img Scan
    os.system("scanimage -x 125 -y 100 --resolution 300 --format=tiff > /home/pi/Scanner/filename1.tiff")
    print (" Scan Completed")

    #Img Convert tiff format to jpg format
    os.system("convert /home/pi/Scanner/filename1.tiff /home/pi/Scanner/filename1.jpg")

    # Process image
    placeimg = "/home/pi/Scanner/filename1.jpg"
    mrz = read_mrz(placeimg)

    # Obtain & show Img data
    mrz_data = mrz.to_dict()
    global passportId
    passportId = mrz_data['number'].replace("<", "")
    print(passportId)
    print('Passport ID     :'+ mrz_data['number'])



    #Get current date and time
    now = datetime.now()
    date_time = now.strftime("%y%m%d")
    print('Today           :'+ date_time)

    # Passport expiration date compare with Current date
    first_date = mrz_data['expiration_date']
    second_date = date_time
    
    #print(result)
    if second_date < first_date:
        print("***Your Passport is Valid***")
        #ui.Callapi(passportId)
       
        
    else:
        ui.ui_FinalWindow.show_img_ok(ui.ui_FinalWindow,"Your Passport Expired","Prob.png")
        
        ui.OutWindow.show()
        print("***Your Passport Expired***")
        
        

def scanfingurs():

    ui.ui.retryBtn1 = False
    global finger_count
    #fingerinfo.insert(0,str(thread_res["person_data"]["person_id"]))
    #fingerinfo.insert(1,thread_res["scan_fingers"][0]["person_finger_id"])
    #fingerinfo.insert(2,thread_res["scan_fingers"][1]["person_finger_id"])

    fingerinfo[0] = str(thread_res["person_data"]["person_id"])
    fingerinfo[1] = thread_res["scan_fingers"][0]["person_finger_id"]
    fingerinfo[2] = thread_res["scan_fingers"][1]["person_finger_id"]
    
        #Get current date & time
    now = datetime.now() 
    date_time = now.strftime("%Y_%m_%d %H.%M.%S")
    print("Date and Time:",date_time)
    print("Retry byn:", str(ui.ui.retryBtn1))

    ## Enrolls new finger
    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message_1: ' + str(e))
        exit(1)

    while(finger_count < 2 ):
        ui.ui.setinfo1(ui.SecoundWindow,str(thread_res["scan_fingers"][finger_count]["finger_name"]))
        
        ## Gets sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        
        #templateCount = int(f.getTemplateCount())
        #print('Currently used templates: ' + str(f.getTemplateCount())
        


        print('Waiting for finger...')
        ui.ui.setinfo(ui.SecoundWindow,"Waiting for finger...")


        ## Tries to enroll new finger
        try:


            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)

            ## Checks if finger is already enrolled
            result = f.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                positionNumber1 = positionNumber
                if ( f.deleteTemplate(positionNumber1) == True ):
                    print('Template deleted!')
                #exit(0)

            print('Remove finger...')
            ui.ui.setinfo(ui.SecoundWindow,"Remove finger...")
            time.sleep(3)
            
            ## Wait that finger is read again to ensure the finger
            print('Waiting for same finger again...')
            ui.ui.setinfo(ui.SecoundWindow,"Waiting for same finger again...")
            while ( f.readImage() == False ):
                pass
            
            print('Remove Finger...')
            ui.ui.setinfo(ui.SecoundWindow,"Remove finger...")
            time.sleep(3)
            
            ##Download and save finger image    
            print('Downloading image (this take a while)...')
            #global fileName
            fileName = str(uuid.uuid4())
            #imageDestination = '/tmp/FP_image.%s.bmp' % os.getpid()
            imageDestination = '/tmp/airport_Fingers.%s.bmp' % now.strftime("%m_%d_%Y_%H.%M.%S")
            temp = open(imageDestination, 'w+b')
            f.downloadImage(imageDestination)
            #print('The image was saved to "' + imageDestination + '".')

            ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(0x02)
            
            ## Compares the charbuffer1 with charbuffer2
            compare = f.compareCharacteristics()
            print('compare count - ' + str(compare) )
            if ( compare < 150 ):
            #if ( f.compareCharacteristics() == 0 ):
                raise Exception('Fingers do not match')
            
            ## Creates a template
            f.createTemplate()
            ##Manually Delete the temporary image template
        
            #positionNumber1 = input('Please enter the template position number you want to delete: ')
            positionNumber1 = int(0)
            if ( f.deleteTemplate(positionNumber1) == True ):
                print('Template deleted!')

        
            ## Saves template at new position number
            positionNumber = f.storeTemplate()
            print('Finger enrolled successfully!')
            ui.ui.setinfo(ui.SecoundWindow,"Finger enrolled successfully!")
            time.sleep(3)
            print('New template position #' + str(positionNumber))
            time.sleep(3)
            print('The download image was saved to "' + imageDestination + '".')
            time.sleep(3)
            
            #print(response)
            #fingerinfo.insert(finger_count+3,uploadfingers(imageDestination,fileName))
            fingerinfo[finger_count+3] = uploadfingers(imageDestination,fileName)
            finger_count = finger_count+1
        
                  
            
        except Exception as e:
            print('Operation failed!')
            print('Exception message_2: ' + str(e))
            ui.ui.setinfo(ui.SecoundWindow,str(e))
            ui.ui.initRetryBtn(ui.SecoundWindow,True)
            #exit(1)
            time.sleep(3)
            while (ui.ui.retryBtn1 == False):
                if ui.ui.retryBtn1:
                    break
                pass
            ui.ui.initRetryBtn(ui.SecoundWindow,False)    
            scanfingurs()
            

    #comparefingers()
    if (comparefingers() == True):
        ui.ui_FinalWindow.show_img_ok(ui.ui_FinalWindow,"Validation Successful \n" "Travel With Plesure.","ok.png")
        finger_count=0
        ui.OutWindow.show()
        exit(1)
                
    else:
        ui.ui_FinalWindow.show_img_ok(ui.ui_FinalWindow,"Error","No.png")
        finger_count=0
        ui.OutWindow.show()
        exit(1)
            
def uploadfingers(localfilepath,fileName):
    files = {'userfile': open(localfilepath, 'rb')}
    body_data = {'file_name': fileName}
    r = requests.post('http://192.168.1.9/passport_db/index.php/upload/do_upload', files=files, data=body_data)
    response = r.json()
    print ('done')
    print (response["upload_data"]["file_name"])
    return (response["upload_data"]["file_name"])

def comparefingers():
    print (fingerinfo)
    body_data = {'person_id': fingerinfo[0], 'finger_id_1': fingerinfo[1], 'finger_id_1_fingerprint': fingerinfo[3], 'finger_id_2': fingerinfo[2],'finger_id_2_fingerprint': fingerinfo[4]}
    r = requests.post('http://192.168.1.9/passport_db/index.php/person/check_gate_fingers',data=body_data)
    #print (r.text)
    response = r.json()
    print (response)
    return (response["matched"])

if __name__ == "__main__":
    import sys
    My_thread = threading.Thread(target=scanfingurs)
    app = QtWidgets.QApplication(sys.argv)
    FirstWindow = QtWidgets.QMainWindow()
    ui = Ui_FirstWindow()
    ui.setupUi(FirstWindow)
    FirstWindow.show()
    sys.exit(app.exec_())
