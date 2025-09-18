// See https://aka.ms/new-console-template for more information
using System;
class Publisher
{
    // Step 1: Define the event delegate
    public delegate void NotifyHandler(string message);

    // Step 2: Declare the event
    public event NotifyHandler OnNotify

    // Step 3: Method to trigger event

    public void DoSomething()
    {
        console.writeline("Doing Something Important");
        OnNotify?.Invoke("Task is Done")
    }
}
