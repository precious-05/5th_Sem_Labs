using System;

class WeatherSuggestion
{
    static void Main()
    {
        Console.WriteLine("\n Welcome to Precious Weather Advisor!");
        Console.Write("Enter today's temperature (C): ");
        int temp = Convert.ToInt32(Console.ReadLine());

        if (temp >= 35)
        {
            Console.WriteLine("It's too hot! Stay indoors and drink plenty of water");
        }
        else if (temp >= 25)
        {
            Console.WriteLine("Nice warm day perfect for outdoor activities!");
        }
        else if (temp >= 15)
        {
            Console.WriteLine("It's a bit cool  maybe grab a light jacket");
        }
        else if (temp >= 5)
        {
            Console.WriteLine("It's cold  wear warm clothes!");
        }
        else
        {
            Console.WriteLine("Freezing temperature!  Better stay home and keep warm");
        }
    }
}
