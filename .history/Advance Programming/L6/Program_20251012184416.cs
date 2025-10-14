using System;

class RestaurantMenu
{
    static void Main()
    {
        Console.WriteLine("🍽️ Welcome to Precious Café!");
        Console.WriteLine("Please select your order:");
        Console.WriteLine("1. Zinger Burger - Rs. 450");
        Console.WriteLine("2. Pizza Slice - Rs. 300");
        Console.WriteLine("3. Cold Drink - Rs. 100");

        Console.Write("\nEnter your choice (1–3): ");
        int choice = Convert.ToInt32(Console.ReadLine());

        switch (choice)
        {
            case 1:
                Console.WriteLine("\nYou ordered a Zinger Burger ");
                Console.WriteLine("Total Bill: Rs. 450");
                break;

            case 2:
                Console.WriteLine("\nYou ordered a Pizza Slice ");
                Console.WriteLine("Total Bill: Rs. 300");
                break;

            case 3:
                Console.WriteLine("\nYou ordered a Cold Drink ");
                Console.WriteLine("Total Bill: Rs. 100");
                break;

            default:
                Console.WriteLine("\nInvalid choice! Please select 1-3");
                break;
        }

        Console.WriteLine("\nThank you for visiting Precious Cafe ");
    }
}
