import tkinter as tk
from tkinter import Label, Button, Text
from tkinter.messagebox import askyesno, showinfo
from tkinter.filedialog import asksaveasfilename
import tkinter.font as tkFont

import pyqrcode


class textToQr:
    def __init__(self, root) -> None:
        root.title("Text to QR")
        # setting window size
        width = 500
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        align_window = f'{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}'
        root.geometry(align_window)
        root.resizable(width=False, height=False)

        # fonts

        title_font = tkFont.Font(family='Times', size=16)
        enter_text_label_font = tkFont.Font(family='Times', size=12)
        display_qr_label_font = tkFont.Font(family='Times', size=10)
        # font for button elements
        button_font = tkFont.Font(family='Times', size=12)

        title_label = Label(root,
                            text="Text to QR Generator",
                            font=title_font,
                            justify="center")

        enter_text_label = Label(root,
                                 text="Enter Text",
                                 font=enter_text_label_font,
                                 justify="center")

        self.text_entry_box = Text(root)

        generate_button = Button(root,
                                 text="Generate Qr",
                                 font=button_font,
                                 justify="center",
                                 command=lambda: self.display_qr())

        self.display_qr_label = Label(root,
                                      text="QR code will be displayed here",
                                      font=display_qr_label_font, justify="center",
                                      borderwidth=2,
                                      relief="groove")

        save_button = Button(root,
                             text="Save",
                             font=button_font,
                             justify="center",
                             command=lambda: self.save_qr_as_image())

        exit_button = Button(root,
                             text="Exit",
                             font=button_font,
                             justify="center",
                             command=lambda: self.exit())

        # place all elements
        title_label.place(x=140, y=30, width=185, height=25)
        enter_text_label.place(x=20, y=80, width=70, height=25)
        self.text_entry_box.place(x=100, y=80, width=297, height=100)
        generate_button.place(x=195, y=190, width=85, height=25)
        self.display_qr_label.place(x=50, y=230, width=400, height=300)
        save_button.place(x=150, y=550, width=70, height=25)
        exit_button.place(x=250, y=550, width=70, height=25)

    def check_if_text_box_is_empty(self, text):
        try:
            check_empty_box = text == ''
            if check_empty_box:
                raise ValueError
        except ValueError:
            showinfo("No Text Entered", "Please enter text in the Entry box")

    def get_text(self):
        text = self.text_entry_box.get("1.0", "end-1c")
        return text

    def generate_qr(self):
        data = self.get_text()
        self.check_if_text_box_is_empty(text=data)
        qr_data = pyqrcode.create(data)
        return qr_data

    def display_qr(self):
        qr_data = self.generate_qr()
        temp_image_file = "QRCode.png"
        qr_data.png(temp_image_file, scale=4)
        self.image = tk.PhotoImage(file=temp_image_file)
        self.display_qr_label.configure(image=self.image)

    def save_qr_as_image(self):
        temp_image_file = "QRCode.png"
        image_file = open(temp_image_file, 'rb')
        read_image_file = image_file.read()
        save_as = asksaveasfilename(defaultextension='.png',
                                    filetypes=(("Png file", ".png"),
                                               ("jpeg file", '.jpg'))
                                    )
        if save_as:
            output_file = open(save_as, 'wb')
            output_file.write(read_image_file)
            output_file.close()
        image_file.close()

    def exit(self):
        confirm_exit = askyesno("Confirm Exit", "Do you want to exit?")
        if confirm_exit:
            root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = textToQr(root)
    root.protocol("WM_DELETE_WINDOW", app.exit)
    root.mainloop()
