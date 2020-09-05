import sys
import os
from PyQt5 import QtGui
import firebase_admin
import requests
import  language
from google.cloud import storage
from firebase_admin import credentials
# from firebase_admin import storage
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox ,QTableWidgetItem
from  PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.uic import loadUi
import firebase.firebase as firebase
from datetime import datetime
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
path = firebase.FirebaseApplication("https://smartlib-68d41.firebaseio.com/",None)
# cred = credentials.Certificate('smartlib-68d41-firebase-adminsdk-mwsgj-50844f23d9.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'smartlib-68d41.appspot.com'
# })
credential_path = r"C:\Users\Prateek\PycharmProjects\EDI\venv\smartlib-68d41-firebase-adminsdk-mwsgj-50844f23d9.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
client = storage.Client()
bucket = client.get_bucket('smartlib-68d41.appspot.com')
# credentials = service_account.Credentials.from_service_account_file('smartlib-68d41-firebase-adminsdk-mwsgj-50844f23d9.json')
# client = language.LanguageServiceClient(credentials=cred)
data = {}

class main(QMainWindow):

    def __init__(self):

        super(main,self).__init__()
        loadUi('mains.ui',self)
        self.setStyleSheet(open("style.qss", "r").read())
        self.setWindowTitle("Smart Library System")

        self.end_session.clicked.connect(self.end)
        self.scan_button.clicked.connect(self.scan)
        self.return_scan.clicked.connect(self.returnBook)
        self.return_end_session.clicked.connect(self.return_end)
        self.search_button.clicked.connect(self.search_user)
        self.add_student.clicked.connect(self.addStudent)
        self.book_add.clicked.connect(self.addBook)
        self.add.clicked.connect(self.chooseImg)
        self.student_delete.clicked.connect(self.studentDelete)
        self.book_delete.clicked.connect(self.bookDelete)
        self.ad_search.clicked.connect(self.studentAttend)

    def studentAttend(self):
        k = 0
        attend_date = self.ad_date.text()
        studentData =path.get('student_log/'+ attend_date + '/',None)
        if(studentData != None):
            self.display_student.setText(str(len(studentData)))
            print(studentData)

            self.ad_table.setRowCount(len(studentData))
            self.ad_table.setColumnCount(2)
            self.ad_table.setHorizontalHeaderLabels(['GR number','time'])
            for x in studentData.values():
                z = 0
                for i in x.values():
                    if(z == 1):

                        i = datetime.fromtimestamp(i/1000).time()
                    self.ad_table.setItem(k, z , QTableWidgetItem(str(i)))
                    z = + 1
                # print(i)
                k = k + 1
        else:
            QMessageBox.warning(self, "Error", "Date doesn't exist.")

            # self.ad_list.addItem(str(studentData[x]))



    def bookDelete(self):
        bookId = self.book_id.text()
        bookRef = path.get('books/' + bookId + "/", None)
        if( bookRef != None):
            bid = bookRef['book_id']
            pic = bookRef['image_url']
            pic = pic[58:]
            
            # blob = bucket.blob(img_url)
            #
            # blob.delete()
            storage_client = storage.Client()
            bucket = storage_client.get_bucket('smartlib-68d41.appspot.com')
            bucket.get_blob(pic).delete()
            path.delete('/books/' + bid, None)
            QMessageBox.warning(self, "DELETED", "DELETED SUCCESSFULLY.")
        else:
            QMessageBox.warning(self, "Error", "Book doesn't exist.")






    def studentDelete(self):
        uid  = self.student_id.text()
        if(path.get('Students/' + uid + "/", None) != None):
            path.delete('/Students/' + uid, None)
            QMessageBox.warning(self, "DELETED", "DELETED SUCCESSFULLY.")
        else:
            QMessageBox.warning(self, "Error", "Student doesn't exist.")

    def addBook(self):
        addName = self.book_name.text()
        addAuthor = self.book_author.text()
        addShelf = self.book_shelf.text()
        addCategory = self.category_book.text()
        if( addName != ""):
            if(addAuthor != ""):
                if(addShelf != ""):
                    if(addCategory != ""):
                        book_count = path.get("count",None)
                        bid = "BID" + str(book_count)
                        data["book_name"] = addName
                        data["book_id"] = bid
                        data["shelf_no"] = addShelf
                        data["author"] = addAuthor
                        data["isAvail"] = True
                        data["category"] = addCategory
                        book_count = book_count + 1
                        path.put(url='/', name="count", data=book_count)
                        path.put("books/", bid, data)
                        QMessageBox.about(self,"ADDED","Successfully added")
                        self.book_name.clear()
                        self.category_book.clear()
                        self.book_author.clear()
                        self.book_shelf.clear()
                        self.book_img.clear()
                    else:
                        QMessageBox.warning(self, "Error", "Enter Category.")
                else:
                    QMessageBox.warning(self, "Error", "Enter shelf number.")
            else:
                QMessageBox.warning(self, "Error", "Enter author name.")
        else:
            QMessageBox.warning(self, "Error", "Enter book name.")

    def chooseImg(self):
        # print('hello')
        name = QFileDialog.getOpenFileName(self,'Single File')
        # print("name",name[0])
        # print("type", name[1])
        imagePath = name[0]
        pixmap = QtGui.QPixmap(name[0])
        pixmap = pixmap.scaledToWidth(600)
        self.book_img.setPixmap(pixmap)

        book_count = path.get("count", None)
        bid = "BID" + str(book_count)
        imageBlob = bucket.blob("Book_images/" + bid + "/" + os.path.basename(imagePath))
        imageBlob.upload_from_filename(imagePath)
        # print(imageBlob.public_url)
        data["image_url"] = imageBlob.public_url
        print(data['image_url'])
        # addBook(self,imagePath)

        # client = storage.Client()
        # bucket = client.get_bucket('smartlib-68d41.appspot.com')
        # imageBlob = bucket.blob("Book_images/ha.jpg")
        # imageBlob.upload_from_filename(imagePath)



    def addStudent(self):
        addName = self.add_name.text()
        addDiv = self.add_div.text()
        addBranch = self.add_branch.text()
        addEmail = self.add_email.text()
        addMobile = self.add_mobile.text()
        addAddress = self.add_address.text()
        addGrno = self.add_grno.text()

        if(addName != ""):
            if(addDiv != ""):
                if(addBranch != ""):
                    if(addGrno != ""):
                        if(addAddress != ""):
                            if(addMobile != ""):
                                if(addEmail != ""):
                                    dataa = {
                                    "name": addName,
                                    "grno": addGrno,
                                    "div": addDiv,
                                    "email": addEmail,
                                    "address": addAddress,
                                    "mobile": addMobile,
                                    "total_count": 3,
                                    "book_count": 0,
                                    "branch": addBranch
                                    }
                                    path.put("Students/", addGrno,dataa)
                                    QMessageBox.about(self, "ADDED", "Successfully added")
                                    self.add_branch.clear()
                                    self.add_grno.clear()
                                    self.add_name.clear()
                                    self.add_mobile.clear()
                                    self.add_div.clear()
                                    self.add_address.clear()
                                    self.add_email.clear()

                                else:
                                    QMessageBox.warning(self, "Error", "Enter student email.")
                            else:
                                QMessageBox.warning(self, "Error", "Enter student Mobile.")
                        else:
                            QMessageBox.warning(self, "Error", "Enter student Address.")
                    else:
                        QMessageBox.warning(self, "Error", "Enter student GR no.")
                else:
                    QMessageBox.warning(self, "Error", "Enter student Branch.")
            else:
                QMessageBox.warning(self, "Error", "Enter student Division.")
        else:
            QMessageBox.warning(self, "Error", "Enter student Name.")

        self.add_branch.clear()
        self.add_grno.clear()
        self.add_name.clear()
        self.add_mobile.clear()
        self.add_div.clear()
        self.add_address.clear()
        self.add_email.clear()
    def search_user(self):

        user_uid = self.search.text()
        data = path.get('Students/' + user_uid + '/', None)
        if(data == None):
            QMessageBox.warning(self, "Error", "Invalid Gr number.")
        else:

            self.search_name.setText(data.get('name', None))
            self.search_grno.setText(data.get('grno', None))
            self.search_division.setText(data.get('div', None))
            booksref = path.get('Students/' + user_uid + '/book_issued/', None)
            if(booksref == None):
                pass
            else:
                bids = list(booksref)
                for x in range(len(bids)):
                    bookId = booksref[bids[x]]
                    # print(bookId['issue_time'])
                # text = bookId['book_id'] + "      " + datetime.fromtimestamp(bookId['time']  )
                    self.search_list.addItem(bookId['book_id'])

            # , datetime.fromtimestamp(booksref[bids[]]


        # print(user_uid)
    def return_end(self):
        #self.return_book_issued.clear()
        self.return_name.clear()
        self.return_grno.clear()
        self.return_division.clear()
        self.return_list.clear()



    def returnBook(self):
        cap = cv2.VideoCapture(0)
        string = ""
        while (True):
            ret, frame = cap.read()
            qr_code = pyzbar.decode(frame)
            for word in qr_code:
                string = (word.data).decode('utf-8')
                string = list(string.split(","))
                print(string[0])

            cv2.imshow("frame", frame)

            # if string is []:
            #     continue
            # else:
            #     break

            if (cv2.waitKey(1) == 13):
                break

            if (len(string)):
                uid = string[0]
                print(len(string))
                data = path.get('Students/' + uid + '/', None)
                self.return_name.setText(data.get('name', None))
                self.return_grno.setText(data.get('grno', None))
                self.return_division.setText(data.get('div', None))
                count = data.get('book_count', None)
                for x in range(1, (len(string))):
                    bid = string[x]
                    booksref = path.get('Students/' + uid + '/book_issued/'+ bid + '/', None)

                    if (booksref != None):
                        self.return_list.addItem(bid)
                        now = datetime.now()
                        timestamp = datetime.timestamp(now)
                        booksref['return_time'] = timestamp
                        if (path.get('Students/' + uid + '/book_issued/', None) == None):

                            # print(datetime.fromtimestamp(timestamp))
   
                            count -= 1
                            path.post('Students/' + uid + '/book_returned/', booksref)
                            path.put('Students/' + uid + '/', "book_count", count)
                            # path.put('Students/' + uid + '/', "book_returned/" + bid + "/return_time", timestamp)
                            path.put('books/' + bid ,'/isAvail', True)
                            path.delete('/Students/' + uid + '/book_issued/' + bid, None)
                            QMessageBox.warning(self, "Return", "Book returned.")
                        else:

                            count -= 1
                            print(path.post('Students/' + uid + '/book_returned/', booksref))
                            path.put('Students/' + uid + '/', "book_count", count)
                            # path.put('Students/' + uid + '/', "book_returned/" + bid + '/return_time', timestamp)
                            path.put('books/' + bid ,'/isAvail', True)
                            path.delete('/Students/' + uid + '/book_issued/' + bid, None)
                            QMessageBox.warning(self, "Return", "Book returned.")




                    else:
                        QMessageBox.warning(self, "Error", "Invalid Book.")

                break

        cap.release()
        cv2.destroyAllWindows()

    def scan(self):
        cap = cv2.VideoCapture(0)
        string = ""
        while (True):
            ret, frame = cap.read()
            qr_code = pyzbar.decode(frame)
            for word in qr_code:
                string = (word.data).decode('utf-8')
                string = list(string.split(","))
                print(string[0])

            cv2.imshow("frame", frame)

            # if string is []:
            #     continue
            # else:
            #     break

            if (cv2.waitKey(1) == 13):

                break

            if (len(string)):

                uid = string[0]
                # print(len(string))
                data = path.get('Students/' + uid + '/', None)
                self.name.setText(data.get('name', None))
                self.grno.setText(data.get('grno',None))
                self.division.setText(data.get('div', None))
                count = data.get('book_count', None)

                tcount = data.get('total_count', None)
                lenght = (len(string) - 1)
                # print(count, tcount)

                for x in range(1, (len(string))):
                    if (tcount > count):
                        bid = string[x]
                        booksref = data = path.get('books/' + bid + '/', None)
                        if(booksref != None):
                            count += 1


                            now = datetime.now()
                            self.book_issued.addItem(bid)
                            # self.book_issued.SetValue(bid)
                            timestamp = datetime.timestamp(now)
                            userdata = {

                                "book_id": bid,
                                "issue_time": timestamp

                            }
                            if (path.get('Students/' + uid + '/book_issued/', None) == None):
                                path.put('Students/' + uid + '/', "book_issued/" + bid, userdata)
                                path.put('books/' + bid, '/isAvail', False)
                                path.put('Students/' + uid + '/', "book_count", count)
                                QMessageBox.warning(self, "Issued", "Book issued successfully.")


                            else:
                                path.put('Students/' + uid + '/', 'book_issued/' + bid, userdata)
                                path.put('Students/' + uid + '/', "book_count", count)
                                path.put('books/' + bid, '/isAvail', False)
                                QMessageBox.warning(self, "Issued", "Book issued successfully.")


                            if(len(string ) == (x+1)):
                                break
                        else:

                            QMessageBox.warning(self, "Error", "Book is invalid.")
                            break

                    else:
                    # if ((tcount - count) <= 0):
                        QMessageBox.warning(self, "Error", "Limit exceeded")
                        break

                    #
                    # else:
                    #
                    #      QMessageBox.warning(self, "Error", "Limit Exceeded, No of books you can issue is", (tcount - count))
                    #
                    #      break
            if(len(string)):
                break


        cap.release()
        cv2.destroyAllWindows()

    def end(self):

        self.book_issued.clear()
        self.name.clear()
        self.grno.clear()
        self.division.clear()


app = QApplication(sys.argv)
url = " "
widget = main()
widget.show()
sys.exit(app.exec())