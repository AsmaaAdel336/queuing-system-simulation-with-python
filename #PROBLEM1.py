# PROBLEM1
from matplotlib import pyplot as plt
import numpy as np
import random as rd
import tkinter as tk
from tkinter import *
import threading
import matplotlib
matplotlib.use('TkAgg')
text = None


def UI():
    global text
    root = Tk()
    root.title("Bank Multi-Channel Queue] Simulation")
    root.geometry("850x600")
    root.minsize(850, 600)
    title = Label(root, text="Bank Multi-Channel Queue] Simulation")
    title.config(font=("Calibri", 30))
    title.pack()
    text = Text(root, height=50, width=100, font=("Calibri", 22))
    text.pack()
    root.mainloop()


# Start a different thread for GUI
threading.Thread(target=UI).start()

customers_n = 500   # Number of clients
n = 30    # Number of simulations
Customer_Type_list = []  # Types of customers

O_Interarrival_time_list = [0, 0]  # Interarrival time of ordinary customers
# Interarrival time of distingushed customers
D_Interarrival_time_list = [0, 0]

O_arrival_time_list = [0, 0]  # arrival time of ordinary customers
D_arrival_time_list = [0, 0]  # arrival time of distingushed customers

service_time_list = []    # Total Service Time
start_service_time_list = []    # start Service Time
service_time_end_list = []    # Service Time ends

O_waiting_time_list = [0, 0]    # Total Waiting Time of ordinary customers
# Total Waiting Time of distingushed customers
D_waiting_time_list = [0, 0]

O_Customer_waiting_list = [0, 0]  # ordinary waiting customers
D_Customer_waiting_list = [0, 0]  # distingushed waiting customers

completion_time_list = []  # the completion time for each customer

time_in_system_list = []  # time in system for each customer

IDLE_time_list = []  # idle time for each customer

ST_GRAPH = []    # Array of total Service Time for constructing graph
WT_GRAPH = []    # Array of total Waiting Time for constructing graph
O_IAT_GRAPH = []    # Array of total ordinary Inter-arrival Time for constructing graph
D_IAT_GRAPH = []    # Array of total distingushed Inter-arrival Time for constructing graph


'''

0  customer type                     ,
1  O Interarrival time 
2  D Interarrival time 
3  O Arrival Time     
4  D Arrival Time 
5  Start Service Time,
6  Service Time,
7  Time Service ends,  
8  O Waiting Time  
9  D Waiting Time
10  Completion Time,
11  Time in System, 
12  idle time of server 

'''
data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # data of each customer


def get_IAT_OF_ORDINARY():
    rand = rd.randint(0, 100)
    if 1 <= rand <= 9:
        return 0
    elif 10 <= rand <= 26:
        return 1
    elif 27 <= rand <= 53:
        return 2
    elif 54 <= rand <= 73:
        return 3
    elif 74 <= rand <= 88:
        return 4
    else:
        return 5


def get_IAT_OF_DISTUNGUSHED():
    rand = rd.randint(0, 10)
    if rand == 1:
        return 1
    elif 2 <= rand <= 3:
        return 2
    elif 4 <= rand <= 6:
        return 3
    else:
        return 4


def get_ST_OF_ORDINARY():
    rand = rd.randint(1, 10)
    if 1 <= rand <= 20:
        return 1
    elif 21 <= rand <= 60:
        return 2
    elif 61 <= rand <= 88:
        return 3
    else:
        return 4


def get_ST_OF_DISTUNGUSHED():
    rand = rd.randint(1, 100)
    if 1 <= rand <= 10:
        return 1
    elif 11 <= rand <= 40:
        return 2
    elif 41 <= rand <= 78:
        return 3
    else:
        return 4


def get_CUSTOMER_TYPE():
    type = bool(rd.getrandbits(1))
    if type == 1:
        return "Ordinary       "
    else:
        return "Distingushed"


def get_the_previous_customer_data():
    data[0] = Customer_Type_list[-1]
    if (type == "Ordinary       "):
        data[1] = O_Interarrival_time_list[-1]
        data[2] = D_Interarrival_time_list[-2]
        data[3] = O_arrival_time_list[-1]
        data[4] = D_arrival_time_list[-2]
        data[8] = O_waiting_time_list[-1]
        data[9] = D_waiting_time_list[-2]
    else:
        data[1] = O_Interarrival_time_list[-2]
        data[2] = D_Interarrival_time_list[-1]
        data[3] = O_arrival_time_list[-2]
        data[4] = D_arrival_time_list[-1]
        data[8] = O_waiting_time_list[-2]
        data[9] = D_waiting_time_list[-1]

    data[5] = start_service_time_list[-1]
    data[6] = service_time_list[-1]
    data[7] = service_time_end_list[-1]
    data[10] = completion_time_list[-1]
    data[11] = time_in_system_list[-1]
    data[12] = IDLE_time_list[-1]
    return data


def choose_customer(customer1, customer2):
    if(customer1.AT == customer2.AT):
        if(customer1.type == "Distingushed"):
            return customer1
        else:
            return customer2


customer_number = 0  # the customer number

IAT_ORDINARY_Customer = 0  # Time when the ordinary customer arrives
IAT_DISTINGUSHED_Customer = 0  # Time when the distingushed customer arrives

for i in range(n):
    for j in range(customers_n):
        type = get_CUSTOMER_TYPE()  # check type of the customer
        Customer_Type_list.append(type)
        if(type == "Ordinary       "):
            O_IAT = get_IAT_OF_ORDINARY()  # Inter-arrival Time of ordinary customer
            ST = get_ST_OF_ORDINARY()  # Service Time of ordinary customer
            if(j != 0):
                # Arrival Time of ordinary customer
                AT = sum(filter(lambda i: isinstance(i, int),
                         O_Interarrival_time_list)) + O_IAT  # sum all IAT for all previos ordinary customers and add to IAT of customer
        else:
            D_IAT = get_IAT_OF_DISTUNGUSHED()  # Inter-arrival Time of distingushed customer
            ST = get_ST_OF_DISTUNGUSHED()  # Service Time of distingushed customer
            # Arrival Time of distingushed customer
            if(j != 0):
                AT = sum(filter(lambda i: isinstance(i, int),
                         D_Interarrival_time_list)) + D_IAT  # sum all IAT for all previos distingushed customers and add to IAT of customer
        WT = None   # Waiting Time
        SST = None  # Service Start Time
        CT = None  # Completion Time
        TS = None   # Time in System
        TSE = None  # time service ends
        IDLE = None  # idle service time

        if j == 0:  # If the first customer arrived,so there is no previous data
            O_Interarrival_time_list.append(IAT_ORDINARY_Customer)
            D_Interarrival_time_list.append(IAT_DISTINGUSHED_Customer)
            # Arrival Time of distingushed customer
            WT = 0  # waiting time of the first customer is zero
            if(type == "Ordinary       "):
                # add the waiting time of the ordinary customer
                O_waiting_time_list.append(WT)
                # add the waiting time of the distingushed customer
                D_waiting_time_list.append("-")
                IAT_ORDINARY_Customer = O_IAT
                AT = 0
                O_arrival_time_list.append(AT)
                D_arrival_time_list.append("-")
                O_IAT_GRAPH.append(O_IAT)

            else:
                D_waiting_time_list.append(WT)
                O_waiting_time_list.append("-")
                IAT_DISTINGUSHED_Customer = D_IAT
                D_IAT_GRAPH.append(D_IAT)
                AT = 0
                D_arrival_time_list.append(AT)
                O_arrival_time_list.append("-")
            SST = AT  # the start service time of the first customer is equal to his "arrival time"
            start_service_time_list.append(SST)
            CT = SST + ST  # completion time equals to "start service time"  plus   "service time"
            completion_time_list.append(CT)
            TS = CT - AT  # time in system equals "completion time"   plus  "arrival time"
            time_in_system_list.append(TS)
            TSE = SST + ST  # time service ends equals to "start service time"  plus  "service "time"
            service_time_end_list.append(TSE)
            IDLE = 0  # the idle time is zero
            IDLE_time_list.append(IDLE)
            service_time_list.append(ST)

        else:  # if the customer is not the first one
            PC = get_the_previous_customer_data()                 # Previous Customer
            # store the time when the previos customer ends
            PC_service_time_ends = PC[7]
            if AT >= PC_service_time_ends:  # If the customer arrived when the teller is available
                if(type == "Distingushed"):
                    WT = 0
                    SST = AT + WT
                    CT = SST + ST
                    TS = CT - AT
                    TSE = SST + ST
                    IDLE = AT-PC_service_time_ends
                    D_Interarrival_time_list.append(D_IAT)
                    O_Interarrival_time_list.append("-")
                    start_service_time_list.append(SST)
                    completion_time_list.append(CT)
                    time_in_system_list.append(TS)
                    service_time_end_list.append(TSE)
                    IDLE_time_list.append(IDLE)
                    service_time_list.append(ST)
                    # add the waiting time of the ordinary customer
                    D_waiting_time_list.append(WT)
                    # add the waiting time of the distingushed customer
                    O_waiting_time_list.append("-")
                    D_arrival_time_list.append(AT)
                    O_arrival_time_list.append("-")
                    D_IAT_GRAPH.append(D_IAT)
                else:
                    WT = PC_service_time_ends - AT
                    SST = AT + WT
                    CT = SST + ST
                    TS = CT - AT
                    TSE = SST + ST
                    IDLE = 0
                    O_Interarrival_time_list.append(O_IAT)
                    D_Interarrival_time_list.append("-")
                    start_service_time_list.append(SST)
                    completion_time_list.append(CT)
                    time_in_system_list.append(TS)
                    service_time_end_list.append(TSE)
                    IDLE_time_list.append(IDLE)
                    service_time_list.append(ST)
                    # add the waiting time of the ordinary customer
                    O_waiting_time_list.append(WT)
                    # add the waiting time of the distingushed customer
                    D_waiting_time_list.append("-")
                    O_arrival_time_list.append(AT)
                    D_arrival_time_list.append("-")
                    O_IAT_GRAPH.append(O_IAT)

            elif AT < PC_service_time_ends:  # If the teller is not available when the customer arrives
                WT = PC_service_time_ends - AT
                SST = AT + WT
                CT = SST + ST
                TS = CT - AT
                TSE = SST + ST
                IDLE = 0
                start_service_time_list.append(SST)
                completion_time_list.append(CT)
                time_in_system_list.append(TS)
                service_time_end_list.append(TSE)
                IDLE_time_list.append(IDLE)
                service_time_list.append(ST)
                if(type == "Ordinary       "):
                    # add the waiting time of the ordinary customer
                    O_waiting_time_list.append(WT)
                    # add the waiting time of the distingushed customer
                    D_waiting_time_list.append("-")
                    O_arrival_time_list.append(AT)
                    D_arrival_time_list.append("-")
                    O_Interarrival_time_list.append(O_IAT)
                    D_Interarrival_time_list.append("-")
                    O_IAT_GRAPH.append(O_IAT)

                else:
                    D_waiting_time_list.append(WT)
                    O_waiting_time_list.append("-")
                    D_arrival_time_list.append(AT)
                    O_arrival_time_list.append("-")
                    D_Interarrival_time_list.append(D_IAT)
                    O_Interarrival_time_list.append("-")
                    D_IAT_GRAPH.append(D_IAT)

        # Append data to graph arrays
        WT_GRAPH.append(WT)
        ST_GRAPH.append(ST)


# The average service time of the teller
AVG_ST = sum(service_time_list)/len(service_time_list)
# The average waiting time in the ordinary customers queue and the distinguished customers queue.
AVG_O_WT = sum(filter(lambda i: isinstance(i, int), O_waiting_time_list)) / \
    len(list(i for i in O_waiting_time_list if isinstance(i, int)))
AVG_D_WT = sum(filter(lambda i: isinstance(i, int), D_waiting_time_list)) / \
    len(list(i for i in D_waiting_time_list if isinstance(i, int)))
# The maximum ordinary customers queue length and the distinguished customers queue length.
MAX_O_QUEUE = len(list(i for i in O_arrival_time_list if isinstance(i, int)))
MAX_D_QUEUE = len(list(i for i in D_arrival_time_list if isinstance(i, int)))
# The probability that an ordinary customer wait in the queue,
#  and the probability that a distinguished customer wait in the queue
PR_O_WT = sum(filter(lambda i: isinstance(i, int),
                     O_waiting_time_list))/len(O_waiting_time_list)/100
PR_D_WT = sum(filter(lambda i: isinstance(i, int),
                     D_waiting_time_list))/len(D_waiting_time_list)/100
# The portion of idle time of the teller.
POR_IDLE = sum(IDLE_time_list)/completion_time_list[-1]


print("Type           O_IAT   D_IAT  O_AT  D_AT   O_WT  D_WT  SST   ST    CT  TS  IDLE")

for i in range(13):
    print(Customer_Type_list[i], '   ',
          O_Interarrival_time_list[i+2], '       ',
          D_Interarrival_time_list[i+2], '     ',
          O_arrival_time_list[i+2], '       ',
          D_arrival_time_list[i+2], '      ',
          start_service_time_list[i], '      ',
          service_time_list[i], '      ',
          O_waiting_time_list[i+2], '      ',
          D_waiting_time_list[i+2], '       ',
          completion_time_list[i], '       ',
          time_in_system_list[i], '       ',
          IDLE_time_list[i])


text.insert(tk.END, "Calender Table for the first 10 Customers: \n")
text.insert(tk.END, "Type               O_IAT  D_IAT  O_AT  D_AT   O_WT    D_WT    SST     ST      CT    TS    IDLE\n")
for i in range(13):
    text.insert(tk.END, Customer_Type_list[i])
    text.insert(tk.END, '         ')
    text.insert(tk.END, O_Interarrival_time_list[i+2])
    text.insert(tk.END, '         ')
    text.insert(tk.END, D_Interarrival_time_list[i+2])
    text.insert(tk.END, '         ')
    text.insert(tk.END, O_arrival_time_list[i+2])
    text.insert(tk.END, '         ')
    text.insert(tk.END, D_arrival_time_list[i+2])
    text.insert(tk.END, '         ')
    text.insert(tk.END, start_service_time_list[i])
    text.insert(tk.END, '         ')
    text.insert(tk.END, service_time_list[i])
    text.insert(tk.END, '          ')
    text.insert(tk.END, O_waiting_time_list[i+2])
    text.insert(tk.END, '          ')
    text.insert(tk.END, D_waiting_time_list[i+2])
    text.insert(tk.END, '          ')
    text.insert(tk.END, completion_time_list[i])
    text.insert(tk.END, '          ')
    text.insert(tk.END, time_in_system_list[i])
    text.insert(tk.END, '         ')
    text.insert(tk.END, IDLE_time_list[i])
    text.insert(tk.END, "\n")

text.insert(tk.END, 'The average service time of the teller: ')
text.insert(tk.END, AVG_ST,)
text.insert(tk.END, "\n")
text.insert(tk.END, 'The average waiting time in the ordinary customers queue: ')
text.insert(tk.END, AVG_O_WT)
text.insert(tk.END, "\n")
text.insert(
    tk.END, 'The average waiting time in the distingushed customers queue: ')

text.insert(tk.END, AVG_D_WT)
text.insert(tk.END, "\n")
text.insert(tk.END, 'The maximum ordinary customers queue length: ')
text.insert(tk.END, MAX_O_QUEUE)
text.insert(tk.END, "\n")
text.insert(tk.END, 'The maximum distingushed customers queue length: ')
text.insert(tk.END, MAX_D_QUEUE)
text.insert(tk.END, "\n")
text.insert(
    tk.END, 'The probability that an ordinary customer wait in the queue: ')
text.insert(tk.END, PR_O_WT)
text.insert(tk.END, "\n")
text.insert(
    tk.END, 'The probability that an distingushed customer wait in the queue: ')
text.insert(tk.END, PR_D_WT)
text.insert(tk.END, "\n")
text.insert(tk.END, 'The portion of idle time of the teller: ')
text.insert(tk.END, POR_IDLE)
text.insert(tk.END, "\n")


text.insert(tk.END, "\n\n")
# Construct Graphs
plt.hist(x=WT_GRAPH)
plt.title("Waiting Time Histogram")
plt.xlabel("Waiting Time")
plt.ylabel("Number of customers")
plt.savefig("WT")
plt.show()
plt.hist(x=ST_GRAPH)
plt.title("Service Time Histogram")
plt.xlabel("Service Time")
plt.ylabel("Number of customers")
plt.savefig("ST")
plt.show()
plt.hist(x=O_IAT_GRAPH)
plt.title("ordinary Inter-arrival Time Histogram")
plt.xlabel("Inter-arrival Time")
plt.ylabel("Number of ordinary customers")
plt.savefig("O_IAT")
plt.show()
plt.hist(x=D_IAT_GRAPH)
plt.title("distingushed Inter-arrival Time Histogram")
plt.xlabel("distingushed Inter-arrival Time")
plt.ylabel("Number of distingushed customers")
plt.savefig("D_IAT")
plt.show()
