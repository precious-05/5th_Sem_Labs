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
        int n = Console.ReadLine();
        evenObj.is_even(2);
    }
}
