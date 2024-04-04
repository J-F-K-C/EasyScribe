import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import sys

class Notepad:

    __root = Tk()

    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    
    __thisScrollBar = Scrollbar(__thisTextArea)    
    __file = None

    def __init__(self,**kwargs):

        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass


        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        self.__root.title("Unbenannt - EasyScribe")

        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
    
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        
        top = (screenHeight / 2) - (self.__thisHeight /2)
        
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                            self.__thisHeight,
                                            left, top))

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self.__thisTextArea.grid(sticky = N + E + S + W)
        
        self.__thisFileMenu.add_command(label="Neu",
                                        command=self.__newFile)
        
        self.__thisFileMenu.add_command(label="Öffnen",
                                        command=self.__openFile)
        
        self.__thisFileMenu.add_command(label="Speichern",
                                        command=self.__saveFile)

        self.__thisFileMenu.add_separator()                                       
        self.__thisFileMenu.add_command(label="Beenden",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="Datei",
                                    menu=self.__thisFileMenu)   
    
        self.__thisEditMenu.add_command(label="Ausschneiden",
                                        command=self.__cut)            
    
        self.__thisEditMenu.add_command(label="Kopieren",
                                        command=self.__copy)        
        
        self.__thisEditMenu.add_command(label="Einfügen",
                                        command=self.__paste)        
        
        self.__thisMenuBar.add_cascade(label="Editieren",
                                    menu=self.__thisEditMenu)   
    
        self.__thisHelpMenu.add_command(label="Über",
                                        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Hilfe",
                                    menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT,fill=Y)                
        
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)    
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
    
        
    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("EasyScribe")

    def __openFile(self):
        file_path = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"),
                                               ("Text Documents", "*.txt")])

        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.__file = file_path
                    self.__root.title(os.path.basename(self.__file) + " - EasyScribe")
                    self.__thisTextArea.delete(1.0, END)
                    self.__thisTextArea.insert(1.0, file.read())
            except Exception as e:
                showerror("Fehler beim Öffnen der Datei", str(e))

        
    def __newFile(self):
        self.__root.title("Unbenannt - EasyScribe")
        self.__file = None
        self.__thisTextArea.delete(1.0,END)

    def __saveFile(self):

        if self.__file == None:
            self.__file = asksaveasfilename(initialfile='Unbenannt.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.txt")])

            if self.__file == "":
                self.__file = None
            else:
                
                file = open(self.__file,"w")
                file.write(self.__thisTextArea.get(1.0,END))
                file.close()
                
                self.__root.title(os.path.basename(self.__file) + " - EasyScribe")
                
            
        else:
            file = open(self.__file,"w")
            file.write(self.__thisTextArea.get(1.0,END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):

        self.__root.mainloop()

    def load_file_from_command_line(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.__file = file_path
                self.__root.title(os.path.basename(self.__file) + " - EasyScribe")
                self.__thisTextArea.delete(1.0, END)
                self.__thisTextArea.insert(1.0, file.read())
        except Exception as e:
            showerror("Fehler beim Öffnen der Datei", str(e))

if len(sys.argv) > 1:
    file_to_open = sys.argv[1]
    notepad = Notepad(width=600, height=400)
    notepad.load_file_from_command_line(file_to_open)
    notepad.run()
else:
    notepad = Notepad(width=600,height=400)
    notepad.run()
