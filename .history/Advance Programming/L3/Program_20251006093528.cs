using System;
using Caclulations;

namespace Caclulations
{
    class Even_Checker
    {
        public void is_even(int n)
        {
            if (n % 2 == 0)
            {
                Console.WriteLine("The Number is Even");
            }
            else
            {
                Console.WriteLine("The Number is Odd");
            }
        }
    }
}

class Checker
{
    static void Main()
    {
        Even_Checker evenObj = new Even_Checker();
        Console.WriteLine("Enter any number to check if it is even or odd");
        // int n = int.Parse(Console.ReadLine());
        int n = Convert.ToInt32(Console.ReadLine());
        evenObj.is_even(n);

        Console.WriteLine("Enter your height");
        double height = Convert.ToDouble(Console.ReadLine());
        Console.WriteLine("Your Height is: " + height);
    }
}
