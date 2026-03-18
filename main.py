from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import random
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    gen_password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, gen_password)

    pyperclip.copy(gen_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = { website: { "email": email, "password": password}}

    # Check to see if any field is empty
    if len(website.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
        messagebox.showerror("Error", "Please fill all fields")

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if website in data.keys():
        overwrite = messagebox.askyesno("Warning", f"{website} already exists. Overwrite?")
        if not overwrite:
            return

    messagebox.askokcancel(title=website, message=f"These are your details:\n "
                                                          f"Email: {email}\n "
                                                          f"Password: {password} \n"
                                                          "Is it okay to save")

    data.update(new_data)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

def search():
    website = website_entry.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No Data Found")
    else:
        if website in data.keys():
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Credentials",
                                              message=f"Email: {email}"
                                              f"\nPassword: {password}\n")
        else:
            messagebox.showinfo("Credentials", "No credentials found")




# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

# Logo
canvas = Canvas(window, width=200, height=200, highlightthickness=0)
try:
    logo = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo)
except Exception as e:
    print("Logo not found:", e)
canvas.grid(row=0, column=0, columnspan=3)

# Website
website_label = Label(window, text="Website:")
website_label.grid(row=1, column=0, sticky="e")

website_entry = ttk.Entry(window)
website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
website_entry.focus()

# Email
email_label = Label(window, text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e")

email_entry = ttk.Entry(window)
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
email_entry.insert(0, "someone@email.com")

# Password
password_label = Label(window, text="Password:")
password_label.grid(row=3, column=0, sticky="e")

password_entry = ttk.Entry(window,show="*")
password_entry.grid(row=3, column=1, sticky="ew")

generate_password_button = ttk.Button(window, text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="ew")

# Search button
search_button = ttk.Button(window, text="Search", command=search)
search_button.grid(row=1, column=2, sticky="ew")

# Add Button
add_password_button = ttk.Button(window, text="Add Password", command=save)
add_password_button.grid(row=4, column=1, columnspan=2, sticky="ew")

# Make columns expand evenly
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)


window.mainloop()
