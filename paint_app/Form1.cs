using System;
using System.Drawing;
using System.Windows.Forms;

namespace paint_app
{
    public partial class Form1 : Form
    {
        
        Graphics g;
        Pen pen = new Pen(Color.Black, 10);

 
        int x = -1, y = -1;

        
        bool moving = false;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {
            
            pen.Color = Color.Blue;
        }

        private void panel2_Paint(object sender, PaintEventArgs e)
        {
            pen.Color = Color.Gray;
        }


        private void panel3_Paint(object sender, PaintEventArgs e)
        {
            pen.Color = Color.Black;
           
        }


        

        private void panel1_MouseDown(object sender, MouseEventArgs e)
        {
            // Graphics object is created here to avoid null reference issues...
            g = panel1.CreateGraphics();

            // Enable drawing.
            moving = true;

            // Store the starting mouse position.
            x = e.X;
            y = e.Y;
        }

        private void panel1_MouseUp(object sender, MouseEventArgs e)
        {
            // User has released the mouse button; stop drawing.
            moving = false;

            // Reset coordinates so no unwanted lines are drawn.
            x = -1;
            y = -1;
        }

        private void panel1_MouseMove(object sender, MouseEventArgs e)
        {
            // If the mouse is pressed and previous coordinates are valid, draw a line.
            if (moving && x != -1 && y != -1)
            {
                // Draw a line from the previous point to the current mouse position.
                g.DrawLine(pen, x, y, e.X, e.Y);

                // Update the previous coordinates to the current ones for smooth drawing.
                x = e.X;
                y = e.Y;
            }
        }
    }
}
