// Fixed version of your event example
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
        // ❌ Wrong: Console.Writeline
        // ✅ Fixed: Console.WriteLine
        Console.WriteLine("Doing Something Important");

        // Trigger the event safely (null check with ?.)
        OnNotify?.Invoke("Task is Done");
    }
}

class Subscriber
{
    public void OnNotified(string message)
    {
        // ❌ Wrong: Console.Writeline("text", message);
        // ✅ Fixed: Concatenate string
        Console.WriteLine("Subscriber received a message: " + message);
    }
}

class Program
{
    static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();

        // ❌ Wrong: Called function instead of subscribing
        // publisher.OnNotify += subscriber.OnNotified("Hello");
        // ✅ Fixed: Subscribe method directly
        publisher.OnNotify += subscriber.OnNotified;

        // ❌ Wrong: Console.writeline with two args
        // ✅ Fixed: Concatenate properly
        publisher.OnNotify += (msg) => Console.WriteLine("Logger: " + msg);

        // ❌ Wrong: publisher.DoSomething;
        // ✅ Fixed: Add parentheses
        publisher.DoSomething();
    }
}
