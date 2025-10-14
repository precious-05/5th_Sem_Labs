using System;

namespace BasicMath
{
    class Program
    {
        static void Main()
        {
            // Declare two integer variables
            int a = 20;
            int b = 5;

            // Perform operations
            if (a < b)
            {
                int sum = a + b;
            }          // Addition
            int difference = a - b;   // Subtraction
            int product = a * b;      // Multiplication
            int quotient = a / b;     // Division

            // Display results
            Console.WriteLine("a = " + a + ", b = " + b);
            Console.WriteLine("Addition: " + sum);
            Console.WriteLine("Subtraction: " + difference);
            Console.WriteLine("Multiplication: " + product);
            Console.WriteLine("Division: " + quotient);

            // Keep console open
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
