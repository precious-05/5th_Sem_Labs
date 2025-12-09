using System;
using System.Drawing;
using System.Windows.Forms;

namespace paint_app
{
    public partial class Form1 : Form
    {
        // Graphics object used for drawing on the panel.
        // This will be created when the user starts drawing.
        Graphics g;

        // Pen used for drawing; default color is black and thickness is 10.
        Pen pen = new Pen(Color.Black, 10);

        // Variables used to store the last mouse position.
        int x = -1, y = -1;

        // Flag to check if the mouse is currently pressed and drawing is active.
        bool moving = false;



        public Form1()
        {
            InitializeComponent();
        }

        

        // This single event handles color selection for all PictureBoxes.
        private void ColorBox_Click(object sender, EventArgs e)
        {
            // Casting the sender to PictureBox to read its background color
            PictureBox p = (PictureBox)sender;

            // Change the drawing pen color based on the clicked PictureBox color.
            pen.Color = p.BackColor;
        }

        private void panel1_MouseUp(object sender, MouseEventArgs e)
        {
            // User has released the mouse button; stop drawing.
            moving = false;

            // Reset coordinates so no unwanted lines are drawn.
            x = -1;
            y = -1;

        }

        private void panel1_MouseDown(object sender, MouseEventArgs e)
        {


            // Enable drawing.
            moving = true;

            // Store the starting mouse position.
            x = e.X;
            y = e.Y;
        }

        private void panel1_MouseMove(object sender, MouseEventArgs e)
        {
            // Graphics object is created here to avoid null reference issues...
            g = panel1.CreateGraphics();
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
