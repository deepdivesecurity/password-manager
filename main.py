from tkinter import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

def main() -> None:
    window = Tk()
    window.title("Password Manager")
    window.config(padx=20, pady=20)

    canvas = Canvas(window, width=200, height=200, bg="white", highlightthickness=0)
    bg_image = PhotoImage(file="assets/logo.png")
    canvas.create_image(100, 100, image=bg_image)

    canvas.pack(padx=20, pady=20)
    
    window.mainloop()
    

if __name__ == "__main__":
    main()