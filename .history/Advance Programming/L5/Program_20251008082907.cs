using System;

namespace days
{
    class week_days
    {
        static void Main()
        {
            Console.WriteLine("Enter the number of week day to show your favourite day: ");
            int day = Convert.ToInt32(Console.ReadLine());

            
            if (day == 1)
            {
                Console.WriteLine("Your Favorite Day is Monday");
            }
            else if (day == 2)
            {
                Console.WriteLine("Your Favorite Day is Tuesday");
            }

            else if (day == 3)
            {
                Console.WriteLine("Your Favorite Day is Wednesday");
            }

            else if (day == 4)
            {
                Console.WriteLine("Your Favorite Day is Thursday");
            }

            else if (day == 5)
            {
                Console.WriteLine("Your Favorite Day is Friday");
            }

            else if (day == 6)
            {
                Console.WriteLine("Your Favorite Day is Saturday");
            }

            else if (day == 7)
            {
                Console.WriteLine("Your Favorite Day is Sunday");
            }

            else
            {
                Console.WriteLine("Invalid Choice");
            }

            
            

       }
    }
}








































































/*using System;

public class SwitchStatementExample
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Enter a day number (1-7):");
        int dayNumber = Convert.ToInt32(Console.ReadLine());

        string dayName;

        switch (dayNumber)
        {
            case 1:
                dayName = "Monday";
                break;
            case 2:
                dayName = "Tuesday";
                break;
            case 3:
                dayName = "Wednesday";
                break;
            case 4:
                dayName = "Thursday";
                break;
            case 5:
                dayName = "Friday";
                break;
            case 6:
                dayName = "Saturday";
                break;
            case 7:
                dayName = "Sunday";
                break;
            default:
                dayName = "Invalid Day";
                break;
        }

        Console.WriteLine($"The day is: {dayName}");
    }
}*/