from tkinter import *
# not a class
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pw():
    pw_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # _ => loops 8/9/10 of times and pick random letter from letters list
    letter_list = [random.choice(letters) for _ in range(nr_letters)]
    symbols_list = [random.choice(symbols) for _ in range(nr_symbols)]
    number_list = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = letter_list + symbols_list + number_list
    random.shuffle(password_list)

    password = "".join(password_list)

    # -----  if not using join() ------------
    # password = ""
    # for char in password_list:
    #   password += char
    # ---------------------------------------

    # insert pw into pw_input
    pw_input.insert(0, password)
    # copy pw
    pyperclip.copy(password)


# ---------------------------- Search website ------------------------------- #

def find_password():
    web = web_input.get().strip()
    if len(web) == 0:
        messagebox.showinfo(title="Error", message="Please enter website")
    else:
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
                # pw_result = data[web]["password"]
                # email_result = data[web]["email"]
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="Data not found")
        # except KeyError as keyerror:
        #     messagebox.showinfo(title="Error", message=f"Website {keyerror}  not found")
        else:
            if web in data:
                pw_result = data[web]["password"]
                email_result = data[web]["email"]
                messagebox.showinfo(title=web, message=f"Email: {email_result} \n Password: {pw_result}")
            else:
                messagebox.showinfo(title="Error", message=f"Website {web} not found")


# ---------------------------- SAVE PASSWORD ------------------------------- #

# def save_data_to_database(new_data):
#     try:
#         with open("data.json", "r") as data_file:
#             data = json.load(data_file)
#     except FileNotFoundError:
#         with open("data.json", "w") as data_file:
#             json.dump(new_data, data_file, indent=4)
#     else:
#         data.update(new_data)
#         with open("data.json", "w") as data_file:
#             json.dump(data, data_file, indent=4)
#     finally:
#         web_input.delete(0, END)
#         pw_input.delete(0, END)
#

def save_to_database(data, new_data):
    data.update(new_data)
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


def ok_to_save(web, email, pw):
    is_ok = messagebox.askokcancel(title=web, message=f"These are the details entered:\n"
                                                      f"Email:{email} \nWebsite:{web}\nPassword:{pw}\n"
                                                      f"Is it ok to save?")
    return is_ok


def save():
    web = web_input.get().strip()
    email = email_input.get().strip()
    pw = pw_input.get().strip()
    new_data = {
        web: {
            "email": email,
            "password": pw
        }
    }

    if len(web) == 0 or len(pw) < 1:
        messagebox.showinfo(title="Error", message="Please do not leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            ok_save = ok_to_save(web, email, pw)
            if ok_save:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
        else:
            if web in data:
                email_result = data[web]["email"]
                is_ok_overwrite = messagebox.askokcancel(title="Duplication",
                                                         message=f" password at {web} is already existed. \n Do you "
                                                                 f"want to overwrite the previous data with "
                                                                 f"email: {email_result}?")
                if is_ok_overwrite:
                    ok_save = ok_to_save(web, email, pw)
                    if ok_save:
                        save_to_database(data, new_data)

            else:
                ok_save = ok_to_save(web, email, pw)
                if ok_save:
                    save_to_database(data, new_data)
        finally:
            web_input.delete(0, END)
            pw_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# Label
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Button
gen_pw_button = Button(text="Generate Password", command=generate_pw)
gen_pw_button.grid(column=2, row=3)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# Entry
web_input = Entry(width=24)
web_input.grid(column=1, row=1)
web_input.focus()

email_input = Entry(width=42)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(0, "karen@gmail.com")

pw_input = Entry(width=24)
pw_input.grid(column=1, row=3)

window.mainloop()
