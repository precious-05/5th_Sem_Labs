#include<iostream>
#include<conio.h>
class FCFS
{
    int b_time[10];
    int w_time[10];
    int n_jobs;
    float avg;


    public:
    FCFS()
    {
        n_jobs=0;
        avg=0;

    }
    void Job_Entry(int n)
    {
        n_jobs=n;
        cout<<"\n Enter the Burst Time of each job: ";
        cout<<"\n";
        for(int i=0; i<n_jobs; i++)
        {
            cout<<"\nJob"<<i+1<<":";
            cin>>b_time[i];
        }
    }
}