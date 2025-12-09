#include <iostream>
#include <queue>
#include <vector>    
#include <string>
using namespace std;

class Process {
public:
    string name;      
    int burstTime;
    int remainingTime;
    int waitingTime = 0;
    int turnaroundTime = 0;

    Process(string n, int bt) 
    {
        name = n;
        burstTime = bt;
        remainingTime = bt;
    }
};




class RoundRobinScheduler {
private:
    int timeQuantum;
    queue<int> readyQueue;         // queue<datatype> queue_name;

    vector<Process> processes;    //  Dynamic arrays that can grow or shrink in size
                                    // vector<datatype> vector_name;  
                                    // In this case Vector will store Process type Objects

    vector<string> gantt;         // String Vector

public:
    RoundRobinScheduler(int tq) 
    {
        timeQuantum = tq;
    }

    void addProcess(string name, int burst) {
        processes.emplace_back(name, burst);    //  vector<T>.emplace_back(arguments_for_constructor);
                                                // Creates a new process object and adds it at the end of vector
        readyQueue.push(processes.size() - 1);  

        // Assume vector has 3 processes at this time at 0,1,2 indexes
        // processes.size()  →  4  ,   processes.size() -1  →  3  (bcz index starts from 0)

        // Front → [0, 1, 2] → Back
        // Front → [chrome, VS Code, Terminal]

    }



    void runScheduler() {
        int currentTime = 0;

        while (!readyQueue.empty()) {
            int index = readyQueue.front();  // index = 0
            readyQueue.pop();    // queue becomes [1, 2]

            Process &p = processes[index];  // p is NOT a copy… p is the original process inside the vector
                                            // &p directly points to process object such as VS Code Process
                            // remainingTime, waitingTime changes reflect in original vector 

            int start = currentTime;   //  start = 0

            // Time Slice Execution
            if (p.remainingTime > timeQuantum)    // 5 > 2 → TRUE
            {
                p.remainingTime -= timeQuantum;  // remaining = 5 − 2 = 3   (remaining time means how much work is remaining for the process)
                currentTime += timeQuantum;  //  currentTime = 0 + 2 = 2
                // currentTime = total CPU time that has passed
                // Bcz CPU gives 2 time units to each process


                // remainingTime → process ke andar bacha hua kaam
                // currentTime → CPU ke clock par guzra hua waqt
                
                readyQueue.push(index);   // 
            } 
            else 
            {
                currentTime += p.remainingTime;
                p.waitingTime = currentTime - p.burstTime;
                p.remainingTime = 0;
            }

            // Saving the Gantt Chart Entry
            gantt.push_back(p.name + " (" + to_string(start) + "→" + to_string(currentTime) + ")");
        }


        // Calculate Turnaround Times
        for (auto &p : processes) {
            p.turnaroundTime = p.waitingTime + p.burstTime;
        }
    }

    void printGanttChart() {
        cout << "\n=== GANTT CHART ===\n";
        for (auto &entry : gantt) {
            cout << "| " << entry << " ";
        }
        cout << "|\n\n";
    }

    void printProcessTable() {
        cout << "Process\tBurst\tWaiting\tTurnaround\n";
        for (auto &p : processes) {
            cout << p.name << "\t"
                 << p.burstTime << "\t"
                 << p.waitingTime << "\t"
                 << p.turnaroundTime << "\n";
        }
    }
};

int main() {
    RoundRobinScheduler scheduler(2);

    
    scheduler.addProcess("Chrome", 5);
    scheduler.addProcess("VSCode", 3);
    scheduler.addProcess("Terminal", 8);
    scheduler.addProcess("Spotify", 6);
    scheduler.addProcess("Explorer", 4);

    cout << "\n=== ROUND ROBIN CPU SCHEDULER (TIME QUANTUM = 2) ===\n";

    scheduler.runScheduler();
    scheduler.printGanttChart();
    scheduler.printProcessTable();

    return 0;
}
