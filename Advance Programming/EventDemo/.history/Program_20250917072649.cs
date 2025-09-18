using System;

class Publisher
{
    // Step 1: Define the event delegate
    public delegate void NotifyHandler(string message);

    // Step 2: Declare the event
    public event NotifyHandler? OnNotify; // ❗ nullable lagaya to warning remove ho jaye

    // Step 3: Method to trigger event
    public void DoSomething()
    {
        // Fixed: WriteLine (not Writeline)
        Console.WriteLine("Doing Something Important");

        // Trigger the event safely (null check with ?.)
        OnNotify?.Invoke("Task is Done");
    }
}

class Subscriber
{
    public void OnNotified(string message)
    {
        // Fixed: use + for concatenation
        Console.WriteLine("Subscriber received a message: " + message);
    }
}

class Program
{
    static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();

        // Fixed: Subscribe method (not call it)
        publisher.OnNotify += subscriber.OnNotified;

        // Fixed: use WriteLine properly
        publisher.OnNotify += (msg) => Console.WriteLine("Logger: " + msg);

        // Fixed: Call method with ()
        publisher.DoSomething();
    }
}
