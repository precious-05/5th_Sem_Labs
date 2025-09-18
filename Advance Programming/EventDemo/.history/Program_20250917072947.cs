using System;

class Publisher
{
    // Step 1: Define the event delegate
    public delegate void NotifyHandler(string message);

    // Step 2: Declare the event
    // Previous issue: compiler warning because event was non-nullable.
    // Fixed: added "?" (nullable) so warning goes away.
    public event NotifyHandler? OnNotify;

    // Step 3: Method to trigger event
    public void DoSomething()
    {
        //  Previous issue: "Console.Writeline" (wrong case).
        //  Fixed: correct "Console.WriteLine"
        Console.WriteLine("Doing Something Important");

        //  Previous issue: direct invoke could cause NullReference.
        //  Fixed: safe call using "?."
        OnNotify?.Invoke("Task is Done");
    }
}

class Subscriber
{
    public void OnNotified(string message)
    {
        //  Previous issue: "Console.Writeline" + wrong syntax for printing two args.
        //  Fixed: "Console.WriteLine" + string concatenation.
        Console.WriteLine("Subscriber received a message: " + message);
    }
}

class Program
{
    static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();

        //  Previous issue: "publisher.OnNotify += subscriber.OnNotified("Hello");"
        // That was a METHOD CALL, not an EVENT SUBSCRIPTION (returned void -> error).
        // Fixed: Subscribe to method, no () call.
        publisher.OnNotify += subscriber.OnNotified;

        // Previous issue: "Console.writeline" (wrong case).
        //  Fixed: correct "Console.WriteLine"
        publisher.OnNotify += (msg) => Console.WriteLine("Logger: " + msg);

        // Previous issue: "publisher.DoSomething;" (missing ()).
        // Fixed: correctly call method.
        publisher.DoSomething();
    }
}
