using System;



delegate void GreetDelegate(string name);

class Publisher
{

    public event GreetDelegate OnGreet;
    public void RaiseEvent()
}


class Subscriber
{


}

class Program
{
    
}