using System.ComponentModel;
using System.Data.SqlTypes;
using System.Diagnostics.Tracing;
using System.Drawing;
using System.Security.Cryptography;

Graphics g;
Pen p;
int x=-1, y=-1;
Boolean moving = false;


Graphics g= panel1.CreateGraphics();
Pen p= new Pen(Color.Black,10);


private void pictureBox_1_Click(Object sender, EvenArgs e)
{
    Pen.color=p.BackColor;
}



private void panel1_MouseDown(object sender, CancelEventArgs e)
{
    moving = true;
    x= e.X;
    y=e.Y;
}


private void panel1_MouseMove(object sender, MouseEventArgs e)
{
    if (moving && x!=-1 & y!=-1)
    {
        g.DrawLine(pen,x,y,e.X,e.Y);
        x=e.X;
        y=e.Y;
    }
}