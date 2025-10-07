// Import basic System library for Console class
// allows you to use built-in classes from the System namespace (like Console), Without this line, Console.WriteLine would give an error.
// (C# 10 se, .NET 6+):


using System;
namespace HelloWorld
{
    class Hello
    {
        static void Main()
        {
            // Create an array of 5 integers
            int[] numbers = { 2, 4, 6, 8, 10 };

            // Print all elements using a for loop
            Console.WriteLine("Array elements are:");
            for (int i = 0; i < numbers.Length; i++)
            {
                Console.WriteLine(numbers[i]);
            }

            // Calculate the sum of all numbers
            int sum = 0;
            for (int i = 0; i < numbers.Length; i++)
            {
                sum += numbers[i];  // add each element to sum
            }

            // Display the sum
            Console.WriteLine("Sum of all elements: " + sum);

            // Keep the console window open in debug mode
            Console.WriteLine("Press any key to exit");
            Console.ReadKey();
        }
    }
}
