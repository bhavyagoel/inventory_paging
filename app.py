import streamlit as st
from PIL import Image
from queue import Queue
import pandas as pd
from collections import deque
from operator import itemgetter


def welcome():
    return "Welcome All"

def print_graph(output, pages,capacity, page_faults):
    st.write("This is the simulated graph using FIFO page replacement algorithm:")
    st.write(output)
    st.write("\nNumber of page fault: " + str(page_faults))
    st.write("\nPage Fault Rate: "+ str(int(page_faults)/len(pages)*100) +"%")

def FIFO():
    st.write("Enter the demand details of the outlets or of your chain of shops.")
    pages_input = st.text_input(
        "Please input the reference unique item id in order of demand.",value="7,0,1,2,0,3,0,4,2,3,0,3,0,3,2,1,2,0,1,7,0,1"
    )
    pages = pages_input.split(",")
    pages = [int(i) for i in pages]
    n = len(pages)
    capacity = st.number_input("Enter number of retailers", step=1,min_value=1)
    frame = ["N/A"]*capacity

    indexes = Queue()
    time = 0
    output = pd.DataFrame(index=range(0, capacity))
    page_faults = 0
    
    for i in range(n):
        if frame.count("N/A") > 0:
            if pages[i] not in frame:
                frame[frame.index("N/A")] = pages[i]
                page_faults += 1
                indexes.put(pages[i])
                output[time] = frame
        else: 
            if (pages[i] not in frame): 
                val = indexes.queue[0]  
                indexes.get()  
                frame[frame.index(val)] = pages[i]
                indexes.put(pages[i])  
                page_faults += 1
                output[time] = frame
            else:
                temp = ["N/A"]*capacity
                temp[frame.index(pages[i])] = "hit"
                output[time] = temp
        time += 1
    print_graph(output, pages,capacity, page_faults)
    return 0


def LRU():
    st.write("Enter the demand details of the outlets or of your chain of shops.")
    pages_input = st.text_input(
        "Please input the reference unique item id in order of demand.",value="7,0,1,2,0,3,0,4,2,3,0,3,0,3,2,1,2,0,1,7,0,1"
    )
    pages = pages_input.split(",")
    pages = [int(i) for i in pages]
    n = len(pages)
    capacity = st.number_input("Enter number of retailers", step=1,min_value=1)
    frame = ["N/A"]*capacity 
    time_used = [0]*capacity
    time = 0
    output = pd.DataFrame(index=range(0,capacity))
    page_faults = 0
    
    for i in range(n):
        if (frame.count("N/A") > 0):
            if (pages[i] not in frame): 
                frame[frame.index("N/A")] = pages[i]
                page_faults += 1
                output[time] = frame

        else: 
            if (pages[i] not in frame): 
                
                index = max(enumerate(time_used), key=itemgetter(1))[0]
                frame[index] = pages[i]
                time_used[index] = 0
                page_faults += 1
                output[time] = frame
            else:
                time_used[frame.index(pages[i])] = 0
                temp = ["N/A"]*capacity
                temp[frame.index(pages[i])] = "hit"
                output[time] = temp
        time_used = [t+170 for t in time_used]
        time += 1

    print_graph(output, pages,capacity, page_faults)
    return 0


def Optimal():
    st.write("Enter the demand details of the outlets or of your chain of shops.")
    pages_input = st.text_input(
        "Please input the reference unique item id in order of demand.",value="7,0,1,2,0,3,0,4,2,3,0,3,0,3,2,1,2,0,1,7,0,1"
    )
    pages = pages_input.split(",")
    pages = [int(i) for i in pages]
    n = len(pages)
    capacity = st.number_input("Enter number of retailers", step=1,min_value=1)
    frame = ["N/A"]*capacity 
    pages_queue = deque()

    for page in pages:
        pages_queue.append(page)
    time = 0
    output = pd.DataFrame(index=range(0,capacity))
    page_faults = 0
    
    for i in range(n):
        if (frame.count("N/A") > 0):
            if (pages[i] not in frame): 
                frame[frame.index("N/A")] = pages[i]
                page_faults += 1
                output[time] = frame
        else: 
            if (pages[i] not in frame): 
                time_to_use = [999]*capacity
                for j in range(0,len(frame)):
                    if frame[j] in pages_queue:
                        time_to_use[j] = pages_queue.index(frame[j])
                
                index = max(enumerate(time_to_use), key=itemgetter(1))[0]
                frame[index] = pages[i]

                page_faults += 1
                output[time] = frame
            else:
                temp = ["N/A"]*capacity
                temp[frame.index(pages[i])] = "hit"
                output[time] = temp
        time += 1
        pages_queue.popleft()
    print_graph(output, pages,capacity, page_faults)

def main():
    image = Image.open("inventory.png")
    logo = Image.open("logo1.png")
    st.set_page_config(page_title="ManPages", page_icon=logo)
    st.image(image)
    st.title("@ManPages")
    st.markdown(
        """<div style="background-color:#e1f0fa;padding:10px">
                    <h1 style='text-align: center; color: #304189;font-family:Helvetica'><strong>
                    Paging your Inventories</strong></h1></div><br>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='text-align: center;font-family:Helvetica;'>
                   There have been many techniques to
                   market products for sale, but not very often, do we
                   find products specifically built for the outlets to
                   optimize their sales, by making available the
                   products, which have the most consistent demand.
                   When we came across the concept of Page
                   Replacement, we wanted to try it out on this very
                   problem to build a solution for years old problem
                   of inventory for the businesses and local
                   shopkeepers of the next generation.
                   So, we applied the Page Replacement and, came
                   up with a method to determine the effective
                   number of “hits” and “misses”, to correctly
                   correlate which Replacement (Page Replacement)
                   method is the best suited to optimize the economic
                   outcome of the outlets</p>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<h3 style='text-align: center; color: black; font-family:'Lato';font-family:Helvetica;'>
                   The dashboard will help a shopkeeper to get to know more about the paging techniques and it's output.
                   </h3>""",
        unsafe_allow_html=True,
    )

    st.sidebar.title("Select Paging Algorithms")
    st.sidebar.markdown("Select the algorithms accordingly:")
    algo = st.sidebar.selectbox(
        "Select the Opetion", options=["FIFO", "Optimal", "LRU"]
    )

    if algo == "FIFO":
        FIFO()
    elif algo == "Optimal":
        Optimal()
    elif algo == "LRU":
        LRU()


if __name__ == "__main__":
    main()
