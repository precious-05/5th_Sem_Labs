using System;



delegate void GreetDelegate(string name);

class Publisher
{

    public event GreetDelegate OnGreet;
    public void RaiseEvent(string name)
    {
        Console.WriteLine("Event Raised");
        OnGreet?.Invoke(name);
    }
}


class Subscriber
{
  public void HandleGreeting(string name)
      {
        Console.WriteLine($"Subscriber: Hello! {name} Welcome to delegates");
     }

}

class Program
{
     static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();

        publisher.OnGreet += subscriber.HandleGreeting;
        publisher.RaiseEvent("Precious");
    }
}