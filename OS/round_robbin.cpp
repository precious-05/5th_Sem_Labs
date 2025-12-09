#include <iostream>
#include <queue>
#include <vector>
#include <string>
#include <iomanip>
using namespace std;

class Process {
public:
    string name;
    int burstTime;
    int remainingTime;
    int waitingTime = 0;
    int turnaroundTime = 0;

    Process(string n, int bt) {
        name = n;
        burstTime = bt;
        remainingTime = bt;
    }
};

class RoundRobinScheduler {
private:
    int timeQuantum;
    queue<int> readyQueue;
    vector<Process> processes;

    struct GanttEntry {
        string name;
        int start;
        int end;
    };
    
    vector<GanttEntry> gantt;

public:
    RoundRobinScheduler(int tq) {
        timeQuantum = tq;
    }

    void addProcess(string name, int burst) {
        processes.emplace_back(name, burst);
        readyQueue.push(processes.size() - 1);
    }

    void runScheduler() {
        int currentTime = 0;

        while (!readyQueue.empty()) {
            int index = readyQueue.front();
            readyQueue.pop();

            Process &p = processes[index];

            int start = currentTime;

            if (p.remainingTime > timeQuantum) {
                p.remainingTime -= timeQuantum;
                currentTime += timeQuantum;
                readyQueue.push(index);
            } else {
                currentTime += p.remainingTime;
                p.waitingTime = currentTime - p.burstTime;
                p.remainingTime = 0;
            }

            // Save Gantt Chart Entry
            gantt.push_back({p.name, start, currentTime});
        }

        // Turnaround Times
        for (auto &p : processes)
            p.turnaroundTime = p.waitingTime + p.burstTime;
    }

    void printGanttChart() {
        cout << "\n=== GANTT CHART (TABLE FORMAT) ===\n\n";

        cout << left << setw(15) << "Process"
             << setw(10) << "Start"
             << setw(10) << "End" << "\n";

        cout << string(35, '-') << "\n";

        for (auto &g : gantt) {
            cout << left << setw(15) << g.name
                 << setw(10) << g.start
                 << setw(10) << g.end
                 << "\n";
        }

        cout << "\n";
    }

    void printProcessTable() {
        cout << "=== PROCESS TABLE ===\n\n";

        cout << left << setw(15) << "Process"
             << setw(10) << "Burst"
             << setw(10) << "Waiting"
             << setw(12) << "Turnaround" << "\n";

        cout << string(50, '-') << "\n";

        for (auto &p : processes) {
            cout << left << setw(15) << p.name
                 << setw(10) << p.burstTime
                 << setw(10) << p.waitingTime
                 << setw(12) << p.turnaroundTime
                 << "\n";
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

    cout << "\n------ ROUND ROBIN CPU SCHEDULER (TQ = 2) ------\n";

    scheduler.runScheduler();
    scheduler.printGanttChart();
    scheduler.printProcessTable();

    return 0;
}
