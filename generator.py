import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sv_ttk
import time
from PIL import Image
from PIL import ImageTk
import os
import pyqrcode

class Application(tk.Frame):
    
    def __init__(self,master):
        super().__init__(master)
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        
        sv_ttk.set_theme("dark")
        root.title("QR Generator") #set window title
        root.geometry("520x800") #set window size
        try:
            root.iconbitmap("assets/qr-code.ico")
        except:
            pass
        # root.resizable(0,0) #remove maximize option
        root.update()
        # Center window
        root.minsize(root.winfo_width(), root.winfo_height())
        x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
        y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
        root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
        # root.config(bg="#015a2a")

        # Label Informing User
        labelEnterText = ttk.Label(root, text="Enter text:", font=("Courier", 48))
        labelEnterText.pack()
        
        # Entry
        global user_input
        user_input = tk.StringVar()
        global entryText
        entryText = ttk.Entry(root, textvariable=user_input,width=80, font=("Ariel", 15))
        entryText.pack(padx=50, pady=30)
        entryText.bind('<Button-3>',self.popup) # Bind a func to right click
        entryText.bind('<Return>', self.enterHitted)

        global menu
        menu = tk.Menu(root,tearoff=0) # Create a menu
        menu.add_command(label='Copy',command=self.copy) # Create labels and commands
        menu.add_command(label='Paste',command=self.paste)

        # Button user to Order a new QR
        global buttonQRgener
        buttonQRgener = ttk.Button(root, text="Generate QR Code", style="Accent.TButton", width=20, command=self.generateQR)
        buttonQRgener.pack(padx=10, pady=10)

        # Label to show img
        global labelImg 
        labelImg = tk.Label(root, bg="#e6e6e6")
        labelImg.pack()
        labelImg.pack_forget()

        global buttonSaveImgQR
        buttonSaveImgQR = ttk.Button(root,text="Save QR",style="Accent.TButton", width=20, command=self.saveQR)
        buttonSaveImgQR.pack()
        buttonSaveImgQR.pack_forget()


    def popup(self, event):
        try:
            menu.tk_popup(event.x_root,event.y_root)
        finally:
            menu.grab_release()

    def enterHitted(self, event):
        root.update_idletasks()
        buttonQRgener.invoke()
        time.sleep(0.1)

    def paste(self):
        try:
            clipboard = root.clipboard_get()
            user_input = clipboard
            entryText.delete(0,"end")
            entryText.insert('end',clipboard)
        except:
            pass

    def copy(self):
        inp = entryText.get()
        root.clipboard_clear()
        root.clipboard_append(inp)
                
    def generateQR(self):
        qrListSize = len(user_input.get())
        if qrListSize != 0:
            global qr, img
            qr = pyqrcode.create(user_input.get())
            labelImg.pack(padx=10, pady=30)
            img = tk.BitmapImage(data=qr.xbm(scale=10))
            bitmap = BitmapImage(data=qr.xbm(scale=10))
            # print(qr.terminal())
        else:
            messagebox.showwarning("Warning", "No data")
        try:
            self.showQR()
            buttonSaveImgQR.pack()
        except:
            pass

    def showQR(self):
        labelImg.config(image=img)
        pass

    def saveQR(self):
        root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file", defaultextension=".png", filetypes = (("Png files","*.png"),("all files","*.*")))
        qr.png(root.filename,scale=10)
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()