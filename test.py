import sqlite3

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob(emp_id, photo):
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_blob_query = """INSERT INTO test
                                  (id, photo) VALUES (?, ?)"""

        emp_photo = convert_to_binary_data(photo)
        # Преобразование данных в формат кортежа
        data_tuple = (emp_id, emp_photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

insert_blob(5,"Услуги школы/Английский язык.jpg")
insert_blob(6,"Услуги школы/Португальский язык.jpg")