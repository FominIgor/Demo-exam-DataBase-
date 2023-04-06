import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi


db = sqlite3.connect("LearnSchoolDB.db")
sql = db.cursor()



class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)

        
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.loginbutton.clicked.connect(self.loginfunction)
        self.createaccbutton.clicked.connect(self.gotocreate)
        

    def loginfunction(self):

        email=self.email.text()
        password=self.password.text()
        
        if email == "0000" and password == "0000":
            print("Вы зашли как админ")
            loginbutton=Client()
            widget.addWidget(loginbutton)
            widget.setCurrentIndex(widget.currentIndex()+1)
        sql.execute(f"SELECT * FROM Worker WHERE Email = '{email}' AND Password = '{password}';")
        db.commit() 
        

        if sql.fetchone() == None:
            sql.execute(f"SELECT * FROM Client WHERE Email = '{email}' AND Password = '{password}';")
            if sql.fetchone() == None:
                print("Такого пользователя нет")
            else:
                print('Welcome')
                loginbutton=ClientLog(email,password)
                widget.addWidget(loginbutton)
                widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print('Welcome')
            loginbutton=Workers(email,password)
            widget.addWidget(loginbutton)
            widget.setCurrentIndex(widget.currentIndex()+1)
    



    def gotocreate(self):
        createaccbutton=CreateAcc()
        widget.addWidget(createaccbutton)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.conn = None

    def createaccfunction(self):
        email = self.leEmail.text()
        password=self.leEmail_2.text()


        sql.execute(f"SELECT Email, Password FROM Client WHERE Email = '{email}' AND Password = '{password}'")

        if sql.fetchone() is None:
            sql.execute(f"""insert into Client(second_name, first_name, last_name, id_gender, phone, data_start, Email, Password, data_reg)
            values('{self.leFio.text()}', '{self.leFio_2.text()}', '{self.leFio_3.text()}', '{'1' if self.rbMale.isChecked() else '2'}', '{self.sbAge.text()}', '{self.lePhone.text()}', '{self.leEmail.text()}', '{self.leEmail_2.text()}', '{self.sbAge_2.text()}')""")
            db.commit()
            print('You have registered')
            signupbutton=Login()
            widget.addWidget(signupbutton)
            widget.setCurrentIndex(widget.currentIndex()+1)

        else:
            print('Такая запись уже существует')
            for i in sql.execute('SELECT * FROM users'):
                print(i)

class ClientLog(QDialog):
    
    def __init__(self,email,password):
        super(ClientLog, self).__init__()
        
        loadUi("client.ui",self)
        self.conn = sqlite3.connect('LearnSchoolDB.db')
        cur = self.conn.cursor()
        data = cur.execute(f"""SELECT Client.id, Client.second_name AS "Фамилия клиента", Client.first_name AS "Имя клиента", Client.last_name  AS "Отчество клиента", Uslugi.name_usl  AS "Название услуги",  Worker.second_name AS "Фамилия учителя",Worker.first_name AS "Имя учителя",Worker.last_name AS "Отчество учителя", Main.date_usl AS "дата начала", Main.time_usl AS "Время начала"
FROM Main
INNER JOIN Uslugi ON Main.id_usl = Uslugi.id_usl
INNER JOIN Worker ON Main.id_worker = Worker.id_worker
INNER JOIN Client ON Main.id_client = Client.id
WHERE Client.Email = "{email}" AND Client.Password = "{password}" ; """)
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
    
class Workers(QDialog): 
    def __init__(self,email,password):
        super(Workers, self).__init__()
        loadUi("worker.ui",self)
        self.conn = sqlite3.connect('LearnSchoolDB.db')
        cur = self.conn.cursor()
        data = cur.execute(f"""SELECT Main.id ,Worker.second_name AS "Фамилия учителя" , Worker.first_name AS "Имя учителя",Worker.last_name AS "Отчество учителя", Client.id AS "id клиента", Client.first_name AS "Фамилия клиента", Client.second_name AS "Имя клиента",  Client.last_name AS "Отчество клиента", Uslugi.name_usl AS "Название услуги",  Main.date_usl AS "дата начала", Main.time_usl AS "Время начала"
FROM Main
INNER JOIN Uslugi ON Main.id_usl = Uslugi.id_usl
INNER JOIN Worker ON Main.id_worker = Worker.id_worker
INNER JOIN Client ON Main.id_client = Client.id
WHERE Worker.Email = "{email}" AND Worker.Password = "{password}" ; """)
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()

class Client(QDialog):
    def __init__(self):
        super(Client, self).__init__()
        loadUi("clientAdm.ui",self)
        self.rbMale.setChecked(True)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_3.clicked.connect(self.gotouslugu)
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.qualification.clicked.connect(self.gotoqualification)
        self.worker.clicked.connect(self.gotoworcer)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from client")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from client"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):
        row = [self.leFio.text(), self.leFio_2.text(), self.leFio_3.text(),  'м' if self.rbMale.isChecked() else 'ж', self.lePhone.text(), self.sbAge.text(),
                self.leEmail.text(), self.sbAge_2.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Client(second_name, first_name, last_name, id_gender, phone, data_start, Email, Password, data_reg)
            values('{self.leFio.text()}', '{self.leFio_2.text()}', '{self.leFio_3.text()}', '{'1' if self.rbMale.isChecked() else '2'}', '{self.sbAge.text()}', '{self.lePhone.text()}', '{self.leEmail.text()}', '{self.leEmail_2.text()}', '{self.sbAge_2.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from client where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from client where {col} like '{val}'")


    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotouslugu(self):
        pushButton_3=Uslugu()
        widget.addWidget(pushButton_3)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoqualification(self):
        qualification=Qualification()
        widget.addWidget(qualification)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoworcer(self):
        worker=Worcer()
        widget.addWidget(worker)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Swod(QDialog):
    def __init__(self):
        super(Swod, self).__init__()
        loadUi("svodAdm.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_2.clicked.connect(self.gotouslugu)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.qualification.clicked.connect(self.gotoqualification)
        self.worker.clicked.connect(self.gotoworcer)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from main;")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from main"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):


        row = [self.leFio.text(),self.id_wor.text(), self.dateEdit.text(),
        self.timeEdit.text(), self.leEmail.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into main(id_usl, id_worker, date_usl, time_usl, id_client)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}','{row[4]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from main where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from main where {col} like '{val}'")


    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotouslugu(self):
        pushButton_2=Uslugu()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoqualification(self):
        qualification=Qualification()
        widget.addWidget(qualification)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoworcer(self):
        worker=Worcer()
        widget.addWidget(worker)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Uslugu(QDialog):
    def __init__(self):
        super(Uslugu, self).__init__()
        loadUi("usluguAdm.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.pushButton_5.clicked.connect(self.gotoqualification)
        self.worker.clicked.connect(self.gotoworcer)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from Uslugi;")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from Uslugi"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        
    def convert_to_binary_data(self):
        # Преобразование данных в двоичный формат
        with open(self.leEmail_2.text(), 'rb') as file:
            blob_data = sqlite3.Binary(file.read())
            print(blob_data)
        return blob_data
        
    def insert_staff(self):
        row = [self.leFio.text(), self.leFio_2.text(), self.leFio_3.text(),
               self.lePhone.text(), self.leEmail.text(), ]
        try:
            cur = self.conn.cursor()
            blob_data = sqlite3.Binary(open(self.leEmail_2.text(), 'rb').read())
            emp_photo = blob_data
            
            cur.execute(f"""insert into Uslugi(name_usl, price, sale, price_finish, duration, image)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', ?)""",  (emp_photo,))
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Uslugi where id_usl = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from Uslugi where {col} like '{val}'")

    # def closeEvent(self, event):
    #     if self.conn is not None:
    #         self.conn.close()
    #     event.accept()



    # def find_for_val(self):
    #     val = self.leFind.text()
    #     col = self.cbColNames.itemText(self.cbColNames.currentIndex())
    #     self.update_twStaffs(f"select * from main where {col} like '{val}'")

    # def closeEvent(self, event):
    #     if self.conn is not None:
    #         self.conn.close()
    #     event.accept()

    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoqualification(self):
        pushButton_5=Qualification()
        widget.addWidget(pushButton_5)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoworcer(self):
        worker=Worcer()
        widget.addWidget(worker)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Worcer(QDialog): 
    def __init__(self):
        super(Worcer, self).__init__()
        loadUi("WorcerAdm.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.pushButton_3.clicked.connect(self.gotouslugu)
        self.qualification.clicked.connect(self.gotoqualification)
        
        
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from Worker")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from Worker"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Worker(second_name, first_name, last_name, id_gender, id_qualification,phone, Email,passportseries, passportnumber, Password)
            values('{self.leFio.text()}', '{self.leFio_2.text()}', '{self.leFio_3.text()}', '{'1' if self.rbMale.isChecked() else '2'}', '{self.leEmail_5.text()}', '{self.lePhone.text()}', '{self.leEmail.text()}','{self.leEmail_3.text()}','{self.leEmail_4.text()}', '{self.leEmail_2.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Worker where id_worker = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from Worker where {col} like '{val}'")


    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoqualification(self):
        qualification=Qualification()
        widget.addWidget(qualification)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotouslugu(self):
        pushButton_3=Uslugu()
        widget.addWidget(pushButton_3)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Qualification(QDialog): 
    def __init__(self):
        super(Qualification, self).__init__()
        loadUi("qualification.ui",self)
        #кнопки образования
        self.pbInsert_3.clicked.connect(self.insert_staff)
        self.pbOpen_3.clicked.connect(self.open_file)
        self.pbDelete_3.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)

        self.pbInsert_2.clicked.connect(self.insert_stafforg)
        self.pbOpen_2.clicked.connect(self.open_fileorg)
        self.pbDelete_2.clicked.connect(self.delete_stafforg)
        self.pbFind_2.clicked.connect(self.find_for_valorg)
        
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.pushButton_5.clicked.connect(self.gotouslugu)
        self.worker.clicked.connect(self.gotoworcer)
        self.conn = None
    def open_file(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from qualification")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        
    
    def update_twStaffs(self, query="select * from qualification"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):
        
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into qualification(id_educational_organization, specialization, id_color_diploma, id_education_level)
            values( '{self.leFio_2.text()}', '{self.leFio_3.text()}', '{'2' if self.rbFemale.isChecked() else '1'}', '{self.leEmail.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from qualification where id_qualification = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from qualification where {col} like '{val}'")
        
    # функции для образовательных орг.
    def open_fileorg(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from educational_organization")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames_2.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffsorg(self, query="select * from educational_organization"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_stafforg(self):
        
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into educational_organization(organization)
            values( '{self.leFio_9.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_twStaffsorg()

    def delete_stafforg(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from educational_organization where id_educational_organization = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffsorg()


    def find_for_valorg(self):
        val = self.leFind_2.text()
        col = self.cbColNames_2.itemText(self.cbColNames_2.currentIndex())
        self.update_twStaffsorg(f"select * from educational_organization where {col} like '{val}'")



    def gotouslugu(self):
        pushButton_5=Uslugu()
        widget.addWidget(pushButton_5)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoworcer(self):
        worker=Worcer()
        widget.addWidget(worker)
        widget.setCurrentIndex(widget.currentIndex()+1)




app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(800)
widget.show()
app.exec_()