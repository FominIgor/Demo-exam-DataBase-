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
            loginbutton=Worker(email,password)
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
        data = cur.execute(f"""SELECT Client.id, Client.first_name AS "Фамилия клиента", Client.second_name AS "Имя клиента", Client.last_name  AS "Отчество клиента", Uslugi.name_usl  AS "Название услуги", Worker.first_name AS "Фамилия учителя", Worker.second_name AS "Имя учителя",Worker.last_name AS "Отчество учителя", Main.date_usl AS "дата начала", Main.time_usl AS "Время начала"
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
    
class Worker(QDialog): 
    def __init__(self,email,password):
        super(Worker, self).__init__()
        loadUi("worker.ui",self)
        self.conn = sqlite3.connect('LearnSchoolDB.db')
        cur = self.conn.cursor()
        data = cur.execute(f"""SELECT Main.id , Worker.first_name AS "Фамилия учителя", Worker.second_name AS "Имя учителя",Worker.last_name AS "Отчество учителя", Client.id AS "id клиента", Client.second_name AS "Фамилия клиента", Client.first_name AS "Имя клиента",  Client.last_name AS "Отчество клиента", Uslugi.name_usl AS "Название услуги",  Main.date_usl AS "дата начала", Main.time_usl AS "Время начала"
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
            cur.execute(f"""insert into client(second_name, first_name, last_name, gender, phone, data_start, Email, data_reg)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}')""")
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

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()

    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotouslugu(self):
        pushButton_3=Uslugu()
        widget.addWidget(pushButton_3)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Swod(QDialog):
    def __init__(self):
        super(Swod, self).__init__()
        loadUi("svod.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_2.clicked.connect(self.gotouslugu)
        self.pushButton_1.clicked.connect(self.gotoclient)
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
        row = [self.leFio.text(), self.dateEdit.text(),
               self.timeEdit.text(), self.leEmail.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into main(id_usl, date_usl, time_usl, id_client)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')""")
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

class Uslugu(QDialog):
    def __init__(self):
        super(Uslugu, self).__init__()
        loadUi("uslugu.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('LearnSchoolDB.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from uslugu;")
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
        

    def update_twStaffs(self, query="select * from uslugu"):
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
        row = [self.leFio.text(), self.leFio_2.text(), self.leFio_3.text(),
               self.lePhone.text(), self.leEmail.text(), self.leEmail_2.text(),]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into uslugu(name_usl, price, sale, price_finish, duration, image)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}')""")
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
            cur.execute(f"delete from uslugu where id_usl = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from uslugu where {col} like '{val}'")

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()



    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from main where {col} like '{val}'")

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()

    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)



app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(700)
widget.show()
app.exec_()