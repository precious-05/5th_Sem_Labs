using System;

class IfElseExample
{
    static void Main()
    {
        Console.WriteLine("Enter your marks (0–100):");
        int marks = Convert.ToInt32(Console.ReadLine());

        if (marks >= 90)
        {
            Console.WriteLine("Grade: A+");
        }
        else if (marks >= 80)
        {
            Console.WriteLine("Grade: A");
        }
        else if (marks >= 70)
        {
            Console.WriteLine("Grade: B");
        }
        else if (marks >= 60)
        {
            Console.WriteLine("Grade: C");
        }
        else
        {
            Console.WriteLine("Grade: Fail ");
        }
    }
}
