using System;
using Caclulations;

namespace Caclulations
{
    class Even_Checker
    {
        public void is_even(int n)
        {
            if (n % 2 == 0)
            {
                Console.WriteLine("The Number is Even");
            }
            else
            {
                Console.WriteLine("The Number is Odd");
            }
        }
    }
}

class Checker
{
    static void Main()
    {
        Even_Checker evenObj = new Even_Checker();
        Console.WriteLine("Enter any number to check if it is even or odd");
        // int n = int.Parse(Console.ReadLine());
        int n = Convert.ToInt32(Console.ReadLine());
        evenObj.is_even(n);

        Console.WriteLine("Enter your height");
        double height = Convert.ToDouble(Console.ReadLine());
        Console.WriteLine("Your Height is: " + height);


        // Enter Array Size
        Console.WriteLine("Enter The Array Size");
        int size = Convert.ToInt32(Console.ReadLine());
        int[] array= new int[size];
        for (int i = 0; i < array.Length; i++)
        {
            Console.WriteLine("Enter the array element at index {i}: ");
            array[i] = Convert.ToInt32(Console.ReadLine());
             
        }

        Console.WriteLine("The array elements are: ");
        for (int i = 0; i < array.Length; i++)
        {
            Console.WriteLine("The array element at index {i} ");
            Console.WriteLine(array[i]);
            
        }

    }
}
