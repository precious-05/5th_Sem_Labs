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
    static void Main(string[] args)
    {
        try
        {
            using (StreamReader file = new StreamReader("data.txt"))

            // StreamReader is a class within the System.IO namespace designed for reading characters from byte  streams in a specified encoding
            {
                string content = file.ReadToEnd();
                // ReadToEnd(): Reads all characters from the current position to the end of the stream and returns them  as a single string
                Console.WriteLine(content);
            }
        }
        catch (FileNotFoundException ex)
        {
            Console.WriteLine("The file 'data.txt' not found" + ex.Message);

        }
        finally
        {
            Console.WriteLine("The Program Completed");
        }
    }
}












/*In C#,  It simplifies the process of reading text data from sources like files,
 providing methods and properties to handle character decoding and text processing. 
Here's a breakdown of its key aspects:
Purpose: StreamReader is primarily used for reading text-based data, such as text files, line by line or in 
its entirety. It abstracts away the complexities of dealing with raw bytes and character encodings.
Encoding Handling: It automatically handles character encoding, converting bytes from the underlying
 stream into characters based on a specified encoding (e.g., UTF-8, ASCII). If no encoding is specified, 
 it defaults to UTF-8.
Common Use Cases:
Reading text files line by line.
Reading the entire content of a text file into a single string.
Processing specific portions of a file.
Key Methods:
ReadLine(): Reads a line of characters from the current stream and returns the data as a string.

Read(): Reads the next character from the input stream.
Peek(): Returns the next available character but does not consume it.*/