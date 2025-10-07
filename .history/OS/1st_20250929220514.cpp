#include <iostream>
using namespace std;

class FCFS {
    int b_time[10];
    int w_time[10];
    int n_jobs;
    float avg;

public:
    FCFS() {
        n_jobs = 0;
        avg = 0;
    }

    void Job_Entry(int n) {
        n_jobs = n;
        cout << "\n Enter the Burst Time of each job: \n";
        for (int i = 0; i < n_jobs; i++) {
            cout << "Job " << i + 1 << ": ";
            cin >> b_time[i];
        }
    }

    void wait_time() {
        w_time[0] = 0; // first job has zero waiting time
        for (int i = 1; i < n_jobs; i++) {
            w_time[i] = w_time[i - 1] + b_time[i - 1];
        }

        avg = 0;
        for (int i = 0; i < n_jobs; i++) {
            avg += w_time[i];
        }
        avg /= n_jobs;

        // Printing output
        cout << "\n\t\t\tGantt Chart\n";
        cout << "Burst Time\t\t";
        for (int i = 0; i < n_jobs; i++) {
            cout << b_time[i] << " | ";
        }
        cout << "\nWaiting Time\t\t";
        for (int i = 0; i < n_jobs; i++) {
            cout << w_time[i] << " ";
        }
        cout << "\n\nThe Average Waiting Time is: " << avg << " ms\n";
    }
};

int main() {
    FCFS F;
    int n;
    cout << "\n\n\t\t\tFirst Come First Served (FCFS)";
    cout << "\n\nHow many jobs coming to be entered: ";
    cin >> n;
    F.Job_Entry(n);
    F.wait_time();
    return 0;
}
