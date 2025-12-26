using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace Tabs
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
        private double GetNumber(MaskedTextBox textBox1)
        {
            // method to safely convert input text to number
            try
            {
                return Convert.ToDouble(textBox1.Text);
            }
            catch
            {
                throw new Exception("Invalid Number: " + textBox1.Name);
            }
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



        private void button5_Click(object sender, EventArgs e)
        {

            if (textBox4.Text == "" || textBox5.Text == "" || comboBox1.Text == "")
                MessageBox.Show("Can't Leave input box empty");

            else

                label9.Text = "Email: " + textBox4.Text + "\n" + "Name:" + textBox5.Text + "\n" + "Gender: " + comboBox1.Text;




        }

        private void label9_Click(object sender, EventArgs e)
        {
           
        }

        
    }
}
