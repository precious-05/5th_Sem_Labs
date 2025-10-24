using System;

class w_Loop
{
    static void Main()
    {

        Console.WriteLine("Enter Your Name");
        string name = Console.ReadLine();

        while (name== "")
        {
            Console.WriteLine("Please! Enter Your Name");
            name = Console.ReadLine();
        }

        Console.WriteLine("Helo! Your name is: " + name);
    }
}