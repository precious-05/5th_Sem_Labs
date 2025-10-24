using System;

class w_Loop
{
    static void Main()
    {
        while (true)
        {
            Console.WriteLine("Enter Your Name");
            string name = Console.ReadLine();
        }

        Console.ReadLine("Helo! Your name is: " + name);
    }
}