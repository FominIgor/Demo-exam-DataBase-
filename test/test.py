import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
db = sqlite3.connect("LearnSchoolDB.db")
sql = db.cursor()

class Qualification(QDialog): 
    def __init__(self):
        super(Qualification, self).__init__()
        loadUi("qualification.ui",self)
        #кнопки образования
        self.pbInsert_3.clicked.connect(self.insert_staff)
        self.pbOpen_3.clicked.connect(self.open_file)
        self.pbDelete_3.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        #кнопки образовантельной орг.
        self.pbInsert_2.clicked.connect(self.insert_stafforg)
        self.pbOpen_2.clicked.connect(self.open_fileorg)
        self.pbDelete_2.clicked.connect(self.delete_stafforg)
        self.pbFind_2.clicked.connect(self.find_for_valorg)

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
        self.cbColNames.addItems(col_name)
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



    



app=QApplication(sys.argv)
mainwindow=Qualification()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(800)
widget.show()
app.exec_()