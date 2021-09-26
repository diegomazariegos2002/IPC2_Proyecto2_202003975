
from tkinter import ttk
from tkinter import *

root = Tk()
root.geometry('500x500')

my_tree = ttk.Treeview(root)

#Define our columns
my_tree['columns'] = ("Name", "ID", "Favorite Pizza")


#Formate our columns
my_tree.column('#0', width=120, minwidth=25)
my_tree.column("Name", anchor=W, width=120)
my_tree.column("ID", anchor = CENTER, width=80)
my_tree.column("Favorite Pizza", anchor=W, width=120)

# Create Headings
my_tree.heading("#0", text="Label", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Favorite Pizza", text="Favorite Pizza", anchor=W)

#Add Data
data = ["John", 1, "Pepperoni"]


my_tree.insert(parent = '', index='end', iid=0, text = "1", values=("John", 1, "Peperroni"))


#Pack to the screen
my_tree.pack(pady=20)


root.mainloop()