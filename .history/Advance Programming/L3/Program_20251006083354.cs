using System;
// using Caclulations;

namespace Caclulations
{
    class Even_Checker
    {

        void is_even(int n)
        {
            if (n % 2 == 0)
            {
                Console.WriteLine("The Number is Even");
            }
            else
            {
                Console.WriteLine("The Number is even");
            }
        }
    }
}

class checker
{
    static void Main()
    {
        Even1 Even_Checker = new Even_Checker();
        Even1.is_even(2);
    }
}