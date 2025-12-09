using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace paint4
{
    public partial class Form1 : Form
    {

        Graphics g;
        Pen pen;



        int x = -1, y = -1;


        bool moving = false;

        public Form1()
        {
            InitializeComponent();
            g = panel1.CreateGraphics();
            pen = new Pen(Color.Black, 5);
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            pen.StartCap = pen.EndCap = System.Drawing.Drawing2D.LineCap.Round;

        }





        private void ColorBox_Click(object sender, EventArgs e)
        {

        }
        private void pictureBox1_Click(object sender, EventArgs e)
        {
            // Casting the sender to PictureBox to read its background color
            PictureBox p = (PictureBox)sender;

            // Change the drawing pen color based on the clicked PictureBox color.
            pen.Color = p.BackColor;
            
        }

        private void pictureBox4_Click(object sender, EventArgs e)
        {
            // Casting the sender to PictureBox to read its background color
            // PictureBox p = (PictureBox)sender;
            pen.Color = panel1.BackColor;
            pen.Width = 50;

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

        

        private void panel1_MouseUp(object sender, MouseEventArgs e)
        {
            // User has released the mouse button; stop drawing.
            moving = false;

            // Reset coordinates so no unwanted lines are drawn.
            x = -1;
            y = -1;
        }
    }
}
