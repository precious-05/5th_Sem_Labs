using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Calculator
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private double GetNumber(TextBox txt)
        {
            // method to safely convert input text to number
            try
            {
                return Convert.ToDouble(txt.Text);
            }
            catch
            {
                throw new Exception("Invalid Number: " + txt.Name);
            }
        }


        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            //Enter 1st number text box
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            // Enter 2nd number text box
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {
            //display result text box
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // ADD
            try
            {
                double a = GetNumber(textBox1);
                double b = GetNumber(textBox2);

                double result = a + b;
                textBox3.Text = result.ToString();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            // SUBTRACT
            try
            {
                double a = GetNumber(textBox1);
                double b = GetNumber(textBox2);

                double result = a - b;
                textBox3.Text = result.ToString();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            // MULTIPLY
            try
            {
                double a = GetNumber(textBox1);
                double b = GetNumber(textBox2);

                double result = a * b;
                textBox3.Text = result.ToString();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            // DIVIDE
            try
            {
                double a = GetNumber(textBox1);
                double b = GetNumber(textBox2);

                if (b == 0)
                    throw new Exception("Cannot divide by ZERO!");

                double result = a / b;
                textBox3.Text = result.ToString();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}
