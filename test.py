import sqlite3

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = sqlite3.Binary(file.read())
    return blob_data

    

def update_all():
    sqlite_connection = sqlite3.connect('LearnSchoolDB.db')
    cursor = sqlite_connection.cursor()
    data = cursor.execute("select image from Uslugi")
    data_rows = data.fetchall()
    print(len(data_rows))
    
    for i in range (0,len(data_rows)-1):
        image = data_rows[i]
        image = str(image)
        image =  image.replace("('","")
        image =  image.replace("',)","")
        photo = f'Услуги школы\{image}'
        emp_photo = convert_to_binary_data(photo)
        cursor.execute(f"""UPDATE Uslugi
                                  SET image = (?)  WHERE image = '{image}' """ , (emp_photo,))
        sqlite_connection.commit()
    
update_all()
#update_blob('Китайский язык.jpg',"Услуги школы\Китайский язык.jpg")
