using System;
using System.Windows.Forms;

namespace HealthMate
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            
            // Agar Form1 dusre namespace mein hai to fully qualified name use karo
            Application.Run(new DiabetesCareManager.Form1());
        }
    }
}