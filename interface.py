import tkinter
from tkinter import ttk
from tkinter import StringVar
from main import analitics

window = tkinter.Tk()
window.title("QoE Help")
window.geometry('366x768')

text_node = tkinter.Label(text= "Nodo(s)", width=10)
box_node = tkinter.Entry(window, width=25)

text_days = tkinter.Label(text= "Dias", width=10)
box_days = tkinter.Entry(window, width=25)

def get_parameters():

    node_wrote = str(box_node.get()).upper()
    days_wrote = box_days.get()

    result = analitics(node_wrote, days_wrote)
    
    if isinstance(result, list):
        print(result)
        pass
        
        # table = ttk.Treeview(window, columns=int(days_wrote)+1)
        # table.grid(row=4, column=0, columnspan=int(days_wrote)+1)
        # table.heading("#0", text= "Nodo")

        # for n in range(int(days_wrote)):
        #     print(n)
        #     table.heading("#"+str(int(days_wrote)+1), text= "Fecha")
    else: 
        my_result = StringVar()
        message = tkinter.Label(window, textvariable=my_result, width=20)
        my_result.set(result)
        message.grid(row=2, column=1)


button_help = tkinter.Button(window, text="Analizar", command= get_parameters, width=8)



text_node.grid(row=0, column=0)
box_node.grid(row=0, column=1)
text_days.grid(row=1, column=0)
box_days.grid(row=1, column=1)
button_help.grid(row=2, column=0)

window.mainloop()