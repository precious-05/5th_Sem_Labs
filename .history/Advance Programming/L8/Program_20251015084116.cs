using System;

class CandyCounter
{
    static void Main()
    {
        int candies = 5;

        Console.WriteLine("You have 5 candies. Let's share them with friends!\n");

        while (candies > 0)
        {
            Console.WriteLine("Gave one candy to a friend!");
            // candies--;  // decreases by 1 each time
            Console.WriteLine("Candies left: " + candies);
            Console.WriteLine("-------------------");
        }

        Console.WriteLine("All candies are finished!");
    }
}
