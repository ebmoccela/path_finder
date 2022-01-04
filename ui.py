from tkinter import *
from tkinter import ttk

def create_input_frame(container):
    frame = Frame(container)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)

    Label(frame, text='Enter a path:').grid(column=0, row=0, sticky=W)
    Label(frame, text='Select host if known').grid(column=0, row=1, sticky=W)
    keyword = Entry(frame, width=30)
    keyword.focus()
    keyword.grid(column=1, row=0, sticky=W)
    combobox = ttk.Combobox(frame, values=["test1", "test2"])
    combobox.grid(column=1, row=1)


    return frame

def test():
    pass

def create_menu(container):
    my_menu = Menu(container)
    container.config(menu=my_menu)
    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="add server", command=test)
    return my_menu

def create_main_window():
    root = Tk()
    root.title("Path Finder")
    root.geometry('500x500')
    root.resizable(0,0)
    
    create_menu(root)

    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)

    input_frame = create_input_frame(root)
    input_frame.grid(column=0, row=0)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()