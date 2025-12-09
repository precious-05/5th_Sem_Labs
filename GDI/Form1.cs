using System;
using System.Drawing;
using System.Windows.Forms;

namespace GDI
{
    public partial class Form1 : Form
    {
        private bool isDrawing = false;
        private Point lastPoint;
        private Color selectedColor = Color.Black;
        private int brushSize = 5;

        public Form1()
        {
            InitializeComponent();
            DoubleBuffered = true;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Set default selected color
            selectedColor = Color.Black;
        }

        // ------------------ COLOR SELECTION ------------------
        private void pictureBoxColor_Click(object sender, EventArgs e)
        {
            PictureBox pb = sender as PictureBox;
            selectedColor = pb.BackColor;
        }

        // ------------------- DRAWING LOGIC -------------------
        private void panelCanvas_MouseDown(object sender, MouseEventArgs e)
        {
            isDrawing = true;
            lastPoint = e.Location;
        }

        private void panelCanvas_MouseMove(object sender, MouseEventArgs e)
        {
            if (isDrawing)
            {
                using (Graphics g = panelCanvas.CreateGraphics())
                {
                    Pen pen = new Pen(selectedColor, brushSize)
                    {
                        StartCap = System.Drawing.Drawing2D.LineCap.Round,
                        EndCap = System.Drawing.Drawing2D.LineCap.Round
                    };

                    g.DrawLine(pen, lastPoint, e.Location);
                }

                lastPoint = e.Location;
            }
        }

        private void panelCanvas_MouseUp(object sender, MouseEventArgs e)
        {
            isDrawing = false;
        }
    }

    internal class panelCanvas
    {
    }
}
