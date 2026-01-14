using System;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Diagnostics.Contracts;
using System.Net.NetworkInformation;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;

delegate void GreetDelegate(string name);
// ye delegate ha yaani function ka reference/pointer/signature
// event issi pr build hoga

class publisher
{
    public event GreetDelegate OnGreet;  // allow a class to notify other classe/objects about anything happened
    
    public void RaiseEvent(StringBuilder name)
    {
        ConsoleTraceListener.WriteLine("Event Raised");
        OnGreet?.Invoke(name);
    }


}

class subscriber
{
    public void HandleGreeting(StringBuilder name)
    {
        Console.WriteLine($"Subscriber: Hello {name}");
    }

}


class program
{
    static void Main()
    {
        
    }
}