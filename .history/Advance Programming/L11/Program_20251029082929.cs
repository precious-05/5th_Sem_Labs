// write a C# program that tries to open a file named data.txt 
// Requirements:
// Use a Try-Catch-finally to handle Errors 
// Catch the FileNotFound Exceptio and show clear mesage
// Use finally block to print "Program Completed"
// (Don't forget to use System.Io)

using System;
using System.IO;

class FileOpener
{
    try
    {
        using(StreamReader file = new StreamReader("data.txt"))
        {
            string content = File.ReadToEnd();
            Console.WriteLine(content);
        }
    }
    catch (FileNotFoundException)
    {
        Console.WriteLine("The file 'data.txt' not found");

}
    finally
    {
        Console.WriteLine("The Program Completed");
}
}