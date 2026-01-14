using System;
using System.Security.Cryptography.X509Certificates;

delegate void GreetDelegate(string name);
// ye delegate ha yaani function ka reference/pointer/signature
// event issi pr build hoga

class publisher
{
    public event GreetDelegate OnGreet;  // allow a class to notify other classe/objects about anything happened


}