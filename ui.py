from tkinter import *
from tkinter import ttk

def create_input_frame(container):
    frame = Frame(container, bg='blue')

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)

    Label(frame, text='Enter a path:').grid(column=0, row=0, sticky=W)
    Label(frame, text='Select host if known').grid(column=0, row=1, sticky=W)
    keyword = Entry(frame, width=30)
    keyword.focus()
    keyword.grid(column=1, row=0, sticky=W)
    combobox = ttk.Combobox(frame, values=["test1", "test2"])
    combobox.grid(column=1, row=1)
    button = Button(frame, text="Find Path").grid(column=1, row=3)
    return frame


def new_window():
    global top
    top = Toplevel(root)
    top.geometry('500x500')
    top.title('Add Server')
    top.resizable(0, 0)
    lbl = Label(top, text="test")
    lbl.pack()
    my_menu.entryconfig("File", state="disabled")
    top.protocol("WM_DELETE_WINDOW", close_top)

    
def close_top():
    my_menu.entryconfig("File", state="normal")
    top.destroy()

def create_menu(container):
    global my_menu
    my_menu = Menu(container)
    container.config(menu=my_menu)
    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(label="add server", command=new_window)
    
    return my_menu

def create_main_window():
    global root 
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