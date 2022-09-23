
import os
from tkinter import *

from views.About import About


class HelpMenu():

    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.geometry("400x300")
        self.window.config(bg='#1B1F3B')
        self.window.title("Menu de ayuda")
        self.initUI()

    def goToTechnicManual(self):
        filePath = os.path.join(os.getcwd(), 'manuals',
                                "ManualTecnicoProyecto1_202110568.pdf")
        os.startfile(filePath)

    def goToUserManual(self):
        filePath = os.path.join(os.getcwd(), 'manuals',
                                "ManualUsuarioProyecto1_202110568.pdf")
        os.startfile(filePath)

    def goToAbout(self):
        newWindow = About(self.window)
        newWindow.window.grab_set()

    def initUI(self):
        buttonFont = ("Helvetica", 10, "bold")
        messagesFont = ("Helvetica", 20)

        Label(self.window, text="Menú de ayuda",
              font=messagesFont, bg='#1B1F3B',
              fg='white').pack(fill="x")

        Button(self.window,
               text="Manual de usuario",
               pady=5,
               padx=10,
               bg="#0D6EFD",
               fg="white",
               font=buttonFont,
               command=self.goToUserManual).pack(fill="x")

        Button(self.window,
               text="Manual técnico",
               pady=5,
               padx=10,
               bg="#0D6EFD",
               fg="white",
               font=buttonFont,
               command=self.goToTechnicManual).pack(fill="x")

        Button(self.window,
               text="Temas de ayuda",
               pady=5,
               padx=10,
               bg="#0D6EFD",
               fg="white",
               font=buttonFont,
               command=self.goToAbout).pack(fill="x")

        Button(self.window,
               text="Salir",
               pady=5,
               padx=10,
               bg="#DC3545",
               fg="white",
               font=buttonFont,
               command=self.window.destroy).pack(fill="x")
