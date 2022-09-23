
from tkinter import *


class About():

    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.geometry("500x300")
        self.window.config(bg='#1B1F3B')
        self.window.title("Acerca del programador")
        self.initUI()

    def initUI(self):
        buttonFont = ("Helvetica", 10, "bold")
        messagesFont = ("Helvetica", 20)

        Label(self.window, text="Damián Ignacio Peña Afre",
              font=messagesFont, bg='#1B1F3B',
              fg='white').pack(fill="x")
        Label(self.window, text="202110568", font=messagesFont, bg='#1B1F3B',
              fg='white').pack(fill="x")
        Label(self.window, text="Lenguajes formales y de programación",
              font=messagesFont, bg='#1B1F3B',
              fg='white').pack(fill="x")
        Label(self.window, text="Proyecto 1", font=messagesFont, bg='#1B1F3B',
              fg='white').pack(fill="x")

        Button(self.window,
               text="Salir",
               pady=5,
               padx=10,
               bg="#DC3545",
               fg="white",
               font=buttonFont,
               command=self.window.destroy).pack(fill="x")
