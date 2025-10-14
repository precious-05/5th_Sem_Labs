# ------------------------------------------------------------
# 🧠 FCFS (First Come, First Serve) Scheduling Algorithm
# ------------------------------------------------------------
# 🔹 Basic Idea:
#   The process that arrives first gets the CPU first.
#   There is no preemption — once a process starts, it runs till it finishes.

# 🔹 Working:
#   1. Sort processes by their arrival time.
#   2. CPU executes them in that order.
#   3. Waiting Time (WT) = Start Time - Arrival Time
#   4. Turnaround Time (TAT) = Completion Time - Arrival Time
#   5. Average WT and TAT are calculated for performance.
#
# 🔹 Characteristics:
#   - Non-preemptive algorithm
#   - Simple and fair in small systems
#   - Problem: Causes “Convoy Effect” (short jobs wait for long ones)
# ------------------------------------------------------------

# Let's implement step-by-step 

# Step 1: Take process details (for simplicity, we hardcode values)
processes = ['P1', 'P2', 'P3']  # Process names
arrival_time = [0, 1, 2]        # Time when each process arrives
burst_time = [5, 3, 8]          # CPU time each process needs

# Step 2: Number of processes
n = len(processes)

# Step 3: Create lists to store results
waiting_time = [0] * n
turnaround_time = [0] * n
completion_time = [0] * n

# Step 4: Sort by arrival time (just in case they aren’t already sorted)
# zip() combines lists; sorted() sorts by arrival time
data = list(zip(processes, arrival_time, burst_time))
data.sort(key=lambda x: x[1])  # sort by arrival time

# After sorting, unpack data again
processes, arrival_time, burst_time = zip(*data)

# Step 5: Calculate Completion, Waiting, and Turnaround Times
# CPU starts at time = 0
current_time = 0

for i in range(n):
    # If CPU is idle before next process arrives
    if current_time < arrival_time[i]:
        current_time = arrival_time[i]
    
    # Process starts when CPU is available
    start_time = current_time
    completion_time[i] = start_time + burst_time[i]
    current_time = completion_time[i]
    
    # Calculate Turnaround and Waiting times
    turnaround_time[i] = completion_time[i] - arrival_time[i]
    waiting_time[i] = turnaround_time[i] - burst_time[i]

# Step 6: Calculate Averages
avg_waiting = sum(waiting_time) / n
avg_turnaround = sum(turnaround_time) / n

# Step 7: Display the results neatly
print("------------------------------------------------------------")
print(" FCFS Scheduling Results")
print("------------------------------------------------------------")
print("Process | Arrival | Burst | Completion | Waiting | Turnaround")
print("------------------------------------------------------------")

for i in range(n):
    print(f"{processes[i]:>7} | {arrival_time[i]:>7} | {burst_time[i]:>5} | "
          f"{completion_time[i]:>10} | {waiting_time[i]:>7} | {turnaround_time[i]:>10}")

print("------------------------------------------------------------")
print(f"Average Waiting Time   = {avg_waiting:.2f}")
print(f"Average Turnaround Time = {avg_turnaround:.2f}")
print("------------------------------------------------------------")

# ------------------------------------------------------------
#  Example Output (with above input):
#
# Process | Arrival | Burst | Completion | Waiting | Turnaround
# ------------------------------------------------------------
#     P1  |       0 |     5 |          5 |       0 |          5
#     P2  |       1 |     3 |          8 |       4 |          7
#     P3  |       2 |     8 |         16 |       6 |         14
# ------------------------------------------------------------
# Average Waiting Time   = 3.33
# Average Turnaround Time = 8.67
#
#  Gantt Chart (Time Line):
#     0 |---P1---| 5 |--P2--| 8 |-------P3-------| 16
#
# ------------------------------------------------------------
