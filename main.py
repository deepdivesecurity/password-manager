from tkinter import *
from tkinter import messagebox
from pathlib import Path
from urllib.parse import urlparse
import random
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import os

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

# ---------------------------- HELPER FUNCTIONS ------------------------------- #
def parse_url(website: Entry) -> str: 
    url = website.get().strip()

    if not url.startswith(("http://", "https://")):
        url_to_parse = f"http://{url}"
    else:
        url_to_parse = url

    domain = urlparse(url_to_parse).netloc

    if domain.startswith("www."):
        domain = domain[4:]

    return domain.split('.')[0]

def derive_key(password: str, salt: bytes): 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    # URL-safe base64-encoded bytes Fernel key
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filepath: str, password: str) -> None: 
    # Generate salt
    salt = os.urandom(16)

    # Get key from password and salt
    key = derive_key(password, salt)

    # Create a Fernet object using the key
    fernet = Fernet(key)

    # Open the file to be encrypted in binary read mode
    with open(filepath, 'rb') as f:
        original = f.read()

    # Encrypt the file content
    encrypted = fernet.encrypt(original)

    # Overwrite the original file with the encrypted data
    with open(filepath, 'wb') as f:
        f.write(salt)
        f.write(encrypted)

def decrypt_file(filepath: str, password: str) -> bytes: 
    if not os.path.exists(filepath):
        raise FileNotFoundError("File does not exist.")

    # Read the encrypted data from the file
    with open(filepath, 'rb') as f:
        encrypted = f.read()

    salt = encrypted[:16]
    encrypted_data = encrypted[16:]

    key = derive_key(password, salt)
    fernet = Fernet(key)

    try: 
        # Decrypt the encrypted data
        return fernet.decrypt(encrypted_data)
    except: 
        raise ValueError("Decryption failed.")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password(password_text: Entry) -> None: 
    letters_list = [random.choice(LETTERS) for _ in range(random.randint(8, 10))]
    numbers_list = [random.choice(NUMBERS) for _ in range(random.randint(2, 4))]
    symbols_list = [random.choice(SYMBOLS) for _ in range(random.randint(2, 4))]
    password_list = letters_list + numbers_list + symbols_list
    random.shuffle(password_list)
    password = "".join(password_list)
    password_text.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password(website: Entry, email: Entry, password: Entry) -> None: 
    if not website.get() or not email.get() or not password.get(): 
        messagebox.showerror("Error", message="Insufficient information provided.")
        return

    file_path = Path("data/passwords.txt")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to save these details?")
    if answer: 
        try: 
            with open(file_path, "a") as file: 
                file.write(f"{website.get()} | {email.get()} | {password.get()}\n")
                messagebox.showinfo(title="Password Saved", message="Password saved successfully.")
        except: 
            messagebox.showerror(title="Error", message="Error saving details. Please try again.")

    website.delete(0, END)
    email.delete(0, END)
    password.delete(0, END)
    website.focus()

# ---------------------------- UI SETUP ------------------------------- #

def main() -> None:
    window = Tk()
    window.title("Password Manager")
    window.config(padx=50, pady=50)

    canvas = Canvas(window, width=200, height=200, bg="white", highlightthickness=0)
    bg_image = PhotoImage(file="assets/logo.png")
    canvas.create_image(100, 100, image=bg_image)
    canvas.grid(row=0, column=1)

    # Labels
    web_lbl = Label(text="Website: ")
    web_lbl.grid(row=1, column=0)

    eml_lbl = Label(text="Email/Username: ")
    eml_lbl.grid(row=2, column=0)

    pas_lbl = Label(text="Password: ")
    pas_lbl.grid(row=3, column=0)

    # Text Boxes
    web_txt = Entry()
    web_txt.grid(row=1, column=1)
    web_txt.focus()

    eml_txt = Entry(width=35)
    eml_txt.grid(row=2, column=1, columnspan=2)

    pas_txt = Entry(width=21)
    pas_txt.grid(row=3, column=1)

    # Buttons
    btn_search = Button(text="Search", width=13)
    btn_search.grid(row=1, column=2)

    btn_gen_pas = Button(text="Generate Password", command=lambda: gen_password(pas_txt))
    btn_gen_pas.grid(row=3, column=2)

    btn_add = Button(text="Add", width=36, command=lambda: save_password(web_txt, eml_txt, pas_txt))
    btn_add.grid(row=4, column=1, columnspan=2)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()