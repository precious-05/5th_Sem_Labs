using System;

delegate void GreetDelegate(string name);
// ye delegate ha yaani function ka reference/pointer/signature
// event issi pr build hoga

class publisher
{
    public event GreetDelegate OnGreet;  // allow a class to notify other classe/objects about anything happened
    
    public void RaiseEvent(string name)
    {
        ConsoleTraceListener.WriteLine("Event Raised");
        OnGreet?.Invoke(name);
    }


}

class subscriber
{
    public void HandleGreeting(string name)
    {
        Console.WriteLine($"Subscriber: Hello {name}");
    }

}


class program
{
    static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();
        publisher.OnGreet += subscriber.HandleGreeting;
        publisher.RaiseEvent("Alina");
    }
}