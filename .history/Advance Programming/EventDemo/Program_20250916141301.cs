// See https://aka.ms/new-console-template for more information
using System;
class Publisher
{
    // Step 1: Define the event delegate
    public delegate void NotifyHandler(string message);

    // Step 2: Declare the event
    public event NotifyHandler OnNotify;

    // Step 3: Method to trigger event

    public void DoSomething()
    {
        Console.Writeline("Doing Something Important");
        OnNotify?.Invoke("Task is Done");
    }
}


class Subscriber
{
    public void OnNotified(string message)
    {
        Console.Writeline("Subscriber received a mesage", +message);
    }
}


class Program
{
    static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();
        // Subscribe to event
        publisher.OnNotify += subscriber.OnNotified;

        // publisher.OnNotify += (msg) => Console.writeline("Logger:",+msg)
        //Trigger Event 
        publisher.DoSomething;
    }
}