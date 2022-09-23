from tkinter import *

from views.FileEditor import FileEditor
from views.HelpMenu import HelpMenu


class MainMenu():

    masterWindow = Tk()

    def __init__(self):
        self.masterWindow.geometry("400x300")
        self.masterWindow.title("Menú de inicio")
        self.masterWindow.config(bg='#1B1F3B')
        self.initUI()
        self.masterWindow.mainloop()

    def goToFileEditor(self):
        newWindow = FileEditor(self.masterWindow)
        newWindow.window.grab_set()

    def goToHelpMenu(self):
        newWindow = HelpMenu(self.masterWindow)
        newWindow.window.grab_set()

    def initUI(self):

        titleFont = ("Helvetica", 12, "bold")
        buttonFont = ("Helvetica", 10, "bold")

        # Información
        Label(self.masterWindow,
              text="Laboratorio Lenguajes Formales y de Programación",
              pady=5,
              font=titleFont,
              bg='#1B1F3B',
              fg='white').pack()
        Label(self.masterWindow,
              text="Proyecto 1",
              pady=5,
              font=titleFont,
              bg='#1B1F3B',
              fg='white').pack()
        Label(self.masterWindow,
              text="Nombre: Damián Ignacio Peña Afre",
              pady=5,
              bg='#1B1F3B',
              fg='white').pack()
        Label(self.masterWindow,
              text="Carné: 202110568",
              pady=5,
              bg='#1B1F3B',
              fg='white').pack()

        # Separador
        Label(self.masterWindow,
              text="Opciones:",
              pady=5,
              font=titleFont,
              bg='#1B1F3B',
              fg='white').pack()

        # Botones
        Button(self.masterWindow,
               text="Archivo",
               pady=5,
               padx=10,
               bg="#108054",
               fg="white",
               font=buttonFont,
               command=self.goToFileEditor).pack(fill="x")

        Button(self.masterWindow,
               text="Ayuda",
               pady=5,
               padx=10,
               bg="#0D6EFD",
               fg="white",
               font=buttonFont,
               command=self.goToHelpMenu).pack(fill="x")

        Button(self.masterWindow,
               text="Salir",
               pady=5,
               padx=10,
               bg="#DC3545",
               fg="white",
               font=buttonFont,
               command=self.masterWindow.destroy).pack(fill="x")
