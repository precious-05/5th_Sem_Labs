// See https://aka.ms/new-console-template for more information
using System;

namespace library
{
    class User_Input
    {
        static void Main()
        {
            Console.WriteLine("Enter your name");
            string name = Console.ReadLine();
            Console.WriteLine("Hello " + name);
            Console.ReadKey();
        }
    }

}
