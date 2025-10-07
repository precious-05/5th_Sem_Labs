// Import basic System library for Console class
// allows you to use built-in classes from the System namespace (like Console), Without this line, Console.WriteLine would give an error.
// (C# 10 se, .NET 6+):
// Jab aap dotnet new console likh kar project banate ho, .NET automatically kuch namespaces har file me "global using" ke taur par include kar deta hai.
// Isme System namespace bhi included hota hai.
// Is wja se by default program.cs mn using system; na hne k bawjood bhi wo run ho jta ha 


using System;

/*Namespace ka matlab

Namespace ka matlab hota hai "a box / container jisme classes, methods, aur objects organize kiye jate hain".
Ye ek tarah ka folder hota hai jisme aapka code rakha jata hai taa keh dusre code se name clash (conflict) na ho.
Example:
System ek namespace hai jisme Console, Math, String, etc. classes rakhi hui hain.
Aap using System; likh kar us namespace ke andar ki classes directly use kar sakte ho*/

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
