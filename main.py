
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
 
    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)
#REFACTORED CODE USING LIST COMPREHENSION
# password_list = [random.choice(letters) for _ in range(nr_letters)] + \
#                 [random.choice(symbols) for _ in range(nr_symbols)] + \
#                 [random.choice(numbers) for _ in range(nr_numbers)]

# random.shuffle(password_list)

# password = "".join(password_list)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password_entry.insert(0, password)  # Insert the generated password into the password entry field
    pyperclip.copy(password)#copies to clipboard of computer



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get().upper()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website:{
        "email": email,
        "password": password
        }
                }

    if website == "" or email == "" or password == "":
        messagebox.showerror(title="Error", message="Please make sure all fields are filled!")
    else:
        is_ok = messagebox.askyesnocancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it okay to save?")
        
        if is_ok:
            with open("data.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)

                #updating old data with new data
                data.update(new_data) 
            with open("data.json", "w") as data_file: #has to be in w mode, not a because a will append, causing dict error (no comma between entries)
                #saving new data appending to nested dict
                json.dump(data, data_file, indent = 4)

                
                # json.dump(new_data, data_file, indent = 4)

                #data adding and reading
            # with open("data.json", "a") as data_file:
                # json.dump(new_data, data_file, indent = 4)
                #to read from json and show in terminal
                # with open("data.json", "r") as data_file:
                #     data = json.load(data_file)
                # print(data)

            # Clear the input fields after saving
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- Search functionality ------------------------------- #
def find_password():
    with open("data.json", "r") as data_file:
                #reading old data
        data = json.load(data_file)

    website = website_entry.get().upper()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No details for the website exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass")
window.config(padx=20, pady = 20)

canvas = Canvas(width=200, height = 200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=logo_img)
# timer_text = canvas.create_text(100,130,text="00:00", fill = "white", font = (FONT_NAME, 35, "bold"))


# Using grid layout
canvas.grid(row=0, column=1)

# Label
website_label = Label(text="Website")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus() #directs focus to this widget, adds typing cursor into widget
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0,"faaizrehman@gmail.com") #prefills email, you can use END index instead of 0 index to allow entry after string
password_entry = Entry(width=20)
password_entry.grid(row=3, column=1)


# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)  
generate_password_button.grid(column=2, row=3)

search_button = Button(text="Search", command = find_password)
search_button.grid(row=1, column=3)


# password_entry.insert(0,generate_password)

add_button = Button(text="Add", width = 36, command=save_data)  
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()