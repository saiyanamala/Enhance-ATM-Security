import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize((250, 250), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
        insert_into_database(file_path)


def insert_into_database(file_path):
    with open(file_path, 'rb') as file:
        image_data = file.read()
    conn = sqlite3.connect('ATMdata.db')  
    cursor = conn.cursor()
    cursor.execute("INSERT INTO IMAGES (ID,IMAGE,PHONE_NO) VALUES (?,?,?)", (int(id.get()),image_data,phone.get()))
    conn.commit()
    conn.close()

    l=tk.Label(root,text='Uploaded Successfully',font=("ArialGreek 15"))
    l.place(x=320,y=200)


def display_records():
    connection = sqlite3.connect('ATMdata.db') 
    cursor = connection.cursor()
    cursor.execute("SELECT ID,PHONE_NO FROM IMAGES")
    records = cursor.fetchall()

    columns =['CARD_NUMBER','PHONE_NUMBER']

    

    record_tree = ttk.Treeview(root)
    record_tree.pack(expand=True, fill="both")
    
    for row in record_tree.get_children():
        record_tree.delete(row)

    print(columns)
    
    record_tree["columns"] =columns
    record_tree.heading("#0", text="SI.NO")
    for col in columns:
        record_tree.heading(col, text=col)
        record_tree.column(col, width=100)  
    

    for idx, record in enumerate(records, start=1):
        record_tree.insert("", tk.END, text=idx, values=record)
    
    cursor.close()
    connection.close()

root = tk.Tk()
root.title("Insert Image into SQL Database")
root.geometry('1080x720')


label = tk.Label(root)
label.place(x=420,y=420)
global id
global phone

l1=tk.Label(root,text='ATM CARD NUMBER:',font=("ArialGreek 15"))
l1.place(x=100,y=100)
id=tk.Entry(root,font=('Arial',14))
id.place(x=460,y=100)
l2=tk.Label(root,text='PHONE NO:',font=("ArialGreek 15"))
l2.place(x=100,y=160)
phone=tk.Entry(root,font=('Arial',14))
phone.place(x=460,y=160)

button = tk.Button(root, text="Select Image", command=select_image)
button.place(x=320,y=200)

count_button = tk.Button(root, text="Count Records", command=display_records)
count_button.place(x=900,y=40)
 


root.mainloop()
