using System;
namespace switchess
{

    class S
    {
        static void Main()
        {
            Console.WriteLine("Enter the number of week day to show your favourite day: ");
            int day = Convert.ToInt32(Console.ReadLine());

            switch (day)
            {
                case 1:
                    Console.WriteLine("-- Your Favorite Day is Monday");
                    break;


                case 2:
                Console.WriteLine("-- Your Favorite Day is Tuesday");
                    break;


                case 3:
                Console.WriteLine("-- Your Favorite Day is Wednesday");
                    break;

                case 4:
                Console.WriteLine("-- Your Favorite Day is Thursday");
                    break;

                case 5:
                Console.WriteLine("-- Your Favorite Day is Friday");
                    break;
                case 6:
                Console.WriteLine("-- Your Favorite Day is Saturday");
                    break;
                case 7:
                Console.WriteLine("-- Your Favorite Day is Sunday");
                    break;
                default:
                Console.WriteLine("Sorry!Invalid Day");

                    break;                             
            }



        }
    }
}