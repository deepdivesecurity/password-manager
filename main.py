from tkinter import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

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
    web_txt = Entry(width=35)
    web_txt.grid(row=1, column=1, columnspan=2)

    eml_txt = Entry(width=35)
    eml_txt.grid(row=2, column=1, columnspan=2)

    pas_txt = Entry(width=21)
    pas_txt.grid(row=3, column=1)

    # Buttons
    btn_gen_pas = Button(text="Generate Password")
    btn_gen_pas.grid(row=3, column=2)

    btn_add = Button(text="Add", width=36)
    btn_add.grid(row=4, column=1, columnspan=2)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()