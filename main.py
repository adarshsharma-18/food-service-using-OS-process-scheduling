import tkinter as tk
from tkinter import simpledialog
from operator import attrgetter

class Process:
    def __init__(self, pid, atime, btime):
        self.pid = pid
        self.atime = atime
        self.btime = btime
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def create_input_window(title, labels, callback):
    input_window = tk.Toplevel()
    input_window.title(title)
    input_window.geometry("300x200")
    input_window.configure(bg="#ffcccb")

    for label_text in labels:
        label = tk.Label(input_window, text=label_text, bg="#ffcccb")
        label.pack()

    entry = tk.Entry(input_window)
    entry.pack()

    def on_button_click():
        value = entry.get()
        input_window.destroy()
        callback(value)

    button = tk.Button(input_window, text="Submit", command=on_button_click, bg="#ff6666")
    button.pack()

def create_output_window(title, output_text):
    output_window = tk.Toplevel()
    output_window.title(title)
    output_window.geometry("400x300")
    output_window.configure(bg="#ffcccb")

    output_label = tk.Label(output_window, text=output_text, bg="#ffcccb")
    output_label.pack()

def sjf():
    def start_sjf(n):
        processes = []
        for j in range(int(n)):
            arrival_time = simpledialog.askinteger("SJF - Arrival Time", f"Enter Arrival Time of Order {j + 1}: ")
            cooking_time = simpledialog.askinteger("SJF - Cooking Time", f"Enter Cooking Time of Order {j + 1} (in minutes): ")
            processes.append(Process(j + 1, arrival_time, cooking_time))

        processes.sort(key=attrgetter('atime', 'btime'))

        ttime = 0
        tArray = [0] * (int(n) + 1)

        for i in range(int(n)):
            j = i
            while j < int(n) and processes[j].atime <= ttime:
                j += 1

            processes[i:j] = sorted(processes[i:j], key=attrgetter('btime'))
            tArray[i] = ttime
            ttime += processes[i].btime

        tArray[-1] = ttime
        average_waiting_time = 0
        average_turnaround_time = 0

        result_text = "\n#Order ID   Arrival Time   Cooking Time   Completion Time   Turnaround Time   Waiting Time\n"
        index = 1
        while index <= int(n):
            for i in range(int(n)):
                if processes[i].pid == index:
                    turnaround = max(0, tArray[i] - processes[i].atime)
                    waiting = max(0, tArray[i] - processes[i].atime)
                    processes[i].completion_time = tArray[i + 1]
                    processes[i].turnaround_time = turnaround
                    processes[i].waiting_time = waiting
                    result_text += f"O[{processes[i].pid}]      {processes[i].atime}              {processes[i].btime}             {processes[i].completion_time}                 {processes[i].turnaround_time}                 {processes[i].waiting_time}\n"
                    average_turnaround_time += turnaround
                    average_waiting_time += waiting
            index += 1

        n_float = float(n)
        result_text += f"\nAverage Waiting Time = {average_waiting_time / n_float:.2f} (min)\n"
        result_text += f"Average Turnaround Time = {average_turnaround_time / n_float:.2f} (min)\n"

        create_output_window("SJF Results", result_text)

    create_input_window("SJF - Enter Order Details", ["Enter Total Number of Orders:"], start_sjf)



def srtf():
    def start_srtf(n):
        p = [Process(i + 1, 0, 0) for i in range(int(n))]
        avg_turnaround_time = 0
        avg_waiting_time = 0
        total_turnaround_time = 0
        total_waiting_time = 0
        total_idle_time = 0
        burst_remaining = [0] * int(n)
        is_completed = [0] * int(n)

        result_text = "\nEnter Arrival Time and Cooking Time\n"

        for i in range(int(n)):
            result_text += f"\nOrder {i + 1}\n"
            p[i].atime = simpledialog.askinteger("SRTF - Arrival Time", f"Arrival Time for Order {i + 1}:")
            p[i].btime = simpledialog.askinteger("SRTF - Cooking Time", f"Cooking Time for Order {i + 1} (in minutes):")
            burst_remaining[i] = p[i].btime

        current_time = 0
        completed = 0
        prev = 0

        while completed < int(n):
            idx = -1
            mn = 10000000

            for i in range(int(n)):
                if p[i].atime <= current_time and not is_completed[i]:
                    if burst_remaining[i] < mn:
                        mn = burst_remaining[i]
                        idx = i
                    if burst_remaining[i] == mn:
                        if p[i].atime < p[idx].atime:
                            mn = burst_remaining[i]
                            idx = i

            if idx != -1:
                if burst_remaining[idx] == p[idx].btime:
                    p[idx].start_time = current_time
                    total_idle_time += p[idx].start_time - prev

                burst_remaining[idx] -= 1
                current_time += 1
                prev = current_time

                if burst_remaining[idx] == 0:
                    p[idx].completion_time = current_time
                    p[idx].turnaround_time = p[idx].completion_time - p[idx].atime
                    p[idx].waiting_time = p[idx].turnaround_time - p[idx].btime
                    total_turnaround_time += p[idx].turnaround_time
                    total_waiting_time += p[idx].waiting_time
                    is_completed[idx] = 1
                    completed += 1
            else:
                current_time += 1

        min_arrival_time = min(p, key=attrgetter('atime')).atime
        max_completion_time = max(p, key=attrgetter('completion_time')).completion_time
        avg_turnaround_time = total_turnaround_time / int(n)
        avg_waiting_time = total_waiting_time / int(n)

        result_text += "\n#Order ID   Arrival Time   Cooking Time   Start Time   Completion Time   Turnaround Time   Waiting Time\n"
        for i in range(int(n)):
            result_text += f"O[{p[i].pid}]      {p[i].atime}              {p[i].btime}            {p[i].start_time}               {p[i].completion_time}                 {p[i].turnaround_time}                 {p[i].waiting_time}\n"

        result_text += f"\nAverage Waiting Time = {avg_waiting_time:.2f} (min)\n"
        result_text += f"Average Turnaround Time = {avg_turnaround_time:.2f} (min)\n"

        create_output_window("SRTF Results", result_text)

    create_input_window("SRTF - Enter Order Details", ["Enter Total Number of Orders:"], start_srtf)

def priority():
    def start_priority(n):
        bt = [0] * int(n)
        wt = [0] * int(n)
        tat = [0] * int(n)
        pr = [0] * int(n)
        p = [i + 1 for i in range(int(n))]
        total = 0

        result_text = ""

        for i in range(int(n)):
            result_text += f"\nOrder {i + 1}\n"
            bt[i] = simpledialog.askinteger("Priority - Cooking Time", f"Cooking Time for Order {i + 1} (in minutes):")
            pr[i] = simpledialog.askinteger("Priority - Priority", f"Priority for Order {i + 1}:")

        for i in range(int(n)):
            pos = i
            for j in range(i + 1, int(n)):
                if pr[j] < pr[pos]:
                    pos = j

            pr[i], pr[pos] = pr[pos], pr[i]
            bt[i], bt[pos] = bt[pos], bt[i]
            p[i], p[pos] = p[pos], p[i]

        wt[0] = 0

        for i in range(1, int(n)):
            wt[i] = 0
            for j in range(i):
                wt[i] += bt[j]

            total += wt[i]

        avg_wt = total / int(n)
        total = 0

        result_text += "\n#Order ID   Cooking Time   Waiting Time   Turnaround Time\n"
        for i in range(int(n)):
            tat[i] = bt[i] + wt[i]
            total += tat[i]
            result_text += f"O[{p[i]}]      {bt[i]}            {wt[i]}              {tat[i]}\n"

        avg_tat = total / int(n)
        result_text += f"\nAverage Waiting Time = {avg_wt:.2f} (min)\n"
        result_text += f"Average Turnaround Time = {avg_tat:.2f} (min)\n"

        create_output_window("Priority Results", result_text)

    create_input_window("Priority - Enter Order Details", ["Enter Total Number of Orders:"], start_priority)



def main_menu():

    root = tk.Tk()
    root.title("Automated Food Ordering System")
    root.geometry("400x350")
    root.configure(bg="#ffcccb")

    label = tk.Label(root, text="<<<<< WELCOME TO AUTOMATED FOOD ORDERING SYSTEM >>>>>>", font=("Helvetica", 14), bg="#ffcccb")
    label.pack(pady=20)

    label_purpose = tk.Label(root, text="System's Purposes:\n\n"
                                       "i. To minimize customer waiting time and turnaround time by using different algorithms of process scheduling.\n"
                                       "ii. To discover the best efficient algorithm among these three process scheduling algorithms.", justify="left", bg="#ffcccb")
    label_purpose.pack(pady=20)

    button_sjf = tk.Button(root, text="Shortest-Job First Scheduling", command=sjf, bg="#fff3e6", width=30, height=2)
    button_sjf.pack(pady=10)

    button_srtf = tk.Button(root, text="Shortest-Remaining Time First", command=srtf, bg="#ffdb4d", width=30, height=2)
    button_srtf.pack(pady=10)

    button_priority = tk.Button(root, text="Priority Scheduling", command=priority, bg="#ff6666", width=30, height=2)
    button_priority.pack(pady=10)

    button_exit = tk.Button(root, text="Exit", command=root.destroy, bg="#99ff99", width=30, height=2)
    button_exit.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_menu()
