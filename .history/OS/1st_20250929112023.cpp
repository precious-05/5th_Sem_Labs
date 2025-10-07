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

    void wait_time(void)
    {
        for(int i=0; i<n; i++)
        {
            w_time[i]=0;
            for(int j=0; j<i; j++)
            {
                w_time[i]=0;
                for(int i=0; i<n_jobs; i++)
                {
                    w_time[i]=w_time[i]+b_time[j];

                }
                avg=avg+w_time[i];
            }
            avg=avg/n_jobs;


            /*Printing output in console*/
            cout<<"\n\t\t\t\tGantt chart\n"
            cout<<"\nBurst Time  \t\t";
            for(int i=0; i<n_jobs; i++)
            {
                cout<<" "<<b_time[i]<<" |";
            }
            cout<<"\n Waiting Time \t\t";
            for(int i=0; i<n_jobs; i++)
            {
                cout<<w_time[i]<<" ";
            }
            cout<<"\n\nThe Average Waiting Time is: "<<avg<<" ms ";
        }

    }
    
}