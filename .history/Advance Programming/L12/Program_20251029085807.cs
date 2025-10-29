using System;

class Multiply
{
    static void Main(string [] args)
    {

        try
        {
            Console.WriteLine("Enter 1st number");
            int n1 = Convert.ToInt32(Console.ReadLine());
            Console.WriteLine("Enter 2nd number");
            int n2 = Convert.ToInt32(Console.ReadLine());
            Int32 n3;

            n3 = n1 / n2;
            Console.WriteLine(n3);
        }

        catch(DivideByZeroException ex)
        {
            Console.WriteLine("Cannot divide by Zero")
        }

    }
}
