using System;

class w_Loop
{
    static void Main()
    {
        while (true)
        {
            Console.WriteLine("Please Enter Your Name");
            string n = Console.ReadLine();
        }

        Console.ReadLine("Helo! Your name is: " + n);
    }
}