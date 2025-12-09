using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

namespace HealthTracker
{
    public partial class Form1 : Form
    {
        private MySqlConnection connection;
        private string connectionString = "Server=localhost;Database=healthtracker;Uid=root;Pwd=PRO_CODER#1;";
        private int currentUserId = 0;
        private string currentUsername = "";

        // New Gradient Color Scheme
        private Color primaryColor = Color.FromArgb(74, 107, 255);     // Royal Blue
        private Color secondaryColor = Color.FromArgb(106, 27, 154);   // Purple
        private Color successColor = Color.FromArgb(56, 203, 137);     // Emerald Green
        private Color dangerColor = Color.FromArgb(255, 87, 87);       // Coral Red
        private Color warningColor = Color.FromArgb(255, 193, 7);      // Amber
        private Color backgroundColor = Color.FromArgb(248, 250, 252); // Light Blue Gray
        private Color darkBlue = Color.FromArgb(32, 40, 68);           // Dark Blue
        private Color lightPurple = Color.FromArgb(147, 112, 219);     // Medium Purple

        public Form1()
        {
            InitializeComponent();
            InitializeDatabase();
            ShowWelcomeScreen();
        }

        private void InitializeDatabase()
        {
            try
            {
                // Create database if not exists
                string createDbConnection = "Server=localhost;Uid=root;Pwd=PRO_CODER#1;";
                using (MySqlConnection conn = new MySqlConnection(createDbConnection))
                {
                    conn.Open();
                    string createDbQuery = @"CREATE DATABASE IF NOT EXISTS healthtracker;";
                    MySqlCommand cmd = new MySqlCommand(createDbQuery, conn);
                    cmd.ExecuteNonQuery();
                }

                // Connect to healthtracker database
                connection = new MySqlConnection(connectionString);
                connection.Open();

                // Create tables if not exists
                string[] createTables = {
                    @"CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(100) NOT NULL,
                        full_name VARCHAR(100),
                        email VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )",

                    @"CREATE TABLE IF NOT EXISTS health_metrics (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        weight DECIMAL(5,2),
                        systolic INT,
                        diastolic INT,
                        sleep_hours DECIMAL(4,2),
                        record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS medications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        name VARCHAR(100) NOT NULL,
                        dosage VARCHAR(100),
                        schedule_time TIME,
                        is_active BOOLEAN DEFAULT TRUE,
                        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS reminders (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        title VARCHAR(100) NOT NULL,
                        description TEXT,
                        reminder_time DATETIME,
                        is_completed BOOLEAN DEFAULT FALSE,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )"
                };

                foreach (string query in createTables)
                {
                    MySqlCommand cmd = new MySqlCommand(query, connection);
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Database Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private DataTable ExecuteQuery(string query, params MySqlParameter[] parameters)
        {
            DataTable dataTable = new DataTable();
            try
            {
                using (MySqlCommand cmd = new MySqlCommand(query, connection))
                {
                    cmd.Parameters.AddRange(parameters);
                    using (MySqlDataAdapter adapter = new MySqlDataAdapter(cmd))
                    {
                        adapter.Fill(dataTable);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Query Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            return dataTable;
        }

        private int ExecuteNonQuery(string query, params MySqlParameter[] parameters)
        {
            try
            {
                using (MySqlCommand cmd = new MySqlCommand(query, connection))
                {
                    cmd.Parameters.AddRange(parameters);
                    return cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Command Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return -1;
            }
        }

        // Method to create gradient backgrounds
        private void DrawGradientBackground(object sender, PaintEventArgs e, Color color1, Color color2)
        {
            Rectangle rect = new Rectangle(0, 0, ((Control)sender).Width, ((Control)sender).Height);
            using (LinearGradientBrush brush = new LinearGradientBrush(rect, color1, color2, 45f))
            {
                e.Graphics.FillRectangle(brush, rect);
            }
        }

        private void DrawCardGradient(object sender, PaintEventArgs e, Color color1, Color color2)
        {
            Control control = (Control)sender;
            Rectangle rect = new Rectangle(0, 0, control.Width, control.Height);

            // Create rounded rectangle path
            GraphicsPath path = new GraphicsPath();
            int cornerRadius = 15;
            path.AddArc(rect.X, rect.Y, cornerRadius, cornerRadius, 180, 90);
            path.AddArc(rect.X + rect.Width - cornerRadius, rect.Y, cornerRadius, cornerRadius, 270, 90);
            path.AddArc(rect.X + rect.Width - cornerRadius, rect.Y + rect.Height - cornerRadius, cornerRadius, cornerRadius, 0, 90);
            path.AddArc(rect.X, rect.Y + rect.Height - cornerRadius, cornerRadius, cornerRadius, 90, 90);
            path.CloseFigure();

            using (LinearGradientBrush brush = new LinearGradientBrush(rect, color1, color2, 45f))
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                e.Graphics.FillPath(brush, path);
            }
        }

        private void ShowWelcomeScreen()
        {
            this.Controls.Clear();
            this.Text = "Health Mate - Welcome";
            this.Size = new Size(1400, 780);
            this.StartPosition = FormStartPosition.CenterScreen;

            // Set gradient background
            this.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(74, 107, 255), Color.FromArgb(106, 27, 154));

            // Header Panel with gradient
            Panel headerPanel = new Panel
            {
                Size = new Size(this.Width, 180),
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };
            headerPanel.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(32, 40, 68), Color.FromArgb(74, 107, 255));

            // Title with modern font and shadow effect
            Label titleLabel = new Label
            {
                Text = "HEALTH MATE",
                Font = new Font("Segoe UI", 42, FontStyle.Bold),
                ForeColor = Color.White,
                AutoSize = true,
                Location = new Point((this.Width - 450) / 2, 40),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            Label subtitleLabel = new Label
            {
                Text = "Your Personal Health Companion",
                Font = new Font("Segoe UI", 18, FontStyle.Regular),
                ForeColor = Color.White,
                AutoSize = true,
                Location = new Point((this.Width - 350) / 2, 110),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Main Content Panel
            Panel contentPanel = new Panel
            {
                Size = new Size(800, 400),
                Location = new Point((this.Width - 800) / 2, 220),
                BackColor = Color.Transparent
            };

            // Welcome Card
            Panel welcomeCard = new Panel
            {
                Size = new Size(600, 150),
                Location = new Point(100, 20),
                BackColor = Color.Transparent
            };
            welcomeCard.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(240, 245, 255));

            Label welcomeLabel = new Label
            {
                Text = "Welcome to Health Mate",
                Font = new Font("Segoe UI", 28, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(50, 30),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            Label descriptionLabel = new Label
            {
                Text = "Track your health metrics, medications, and reminders in one place",
                Font = new Font("Segoe UI", 14),
                ForeColor = darkBlue,
                AutoSize = true,
                Location = new Point(12, 85),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Buttons with modern gradient styling
            int buttonWidth = 300;
            int buttonHeight = 55;
            int buttonX = (contentPanel.Width - buttonWidth) / 2;

            Button registerBtn = CreateGradientButton("CREATE ACCOUNT",
                Color.FromArgb(106, 27, 154), Color.FromArgb(147, 112, 219),
                new Point(buttonX, 200),
                new Size(buttonWidth, buttonHeight));

            Button loginBtn = CreateGradientButton("SIGN IN",
                Color.FromArgb(74, 107, 255), Color.FromArgb(110, 150, 255),
                new Point(buttonX, 270),
                new Size(buttonWidth, buttonHeight));

            // Add events
            loginBtn.Click += (s, e) => CreateLoginForm();
            registerBtn.Click += (s, e) => CreateRegistrationForm();

            // Build hierarchy
            welcomeCard.Controls.Add(welcomeLabel);
            welcomeCard.Controls.Add(descriptionLabel);

            contentPanel.Controls.Add(welcomeCard);
            contentPanel.Controls.Add(registerBtn);
            contentPanel.Controls.Add(loginBtn);

            headerPanel.Controls.Add(titleLabel);
            headerPanel.Controls.Add(subtitleLabel);

            this.Controls.Add(headerPanel);
            this.Controls.Add(contentPanel);
        }

        private Button CreateGradientButton(string text, Color color1, Color color2, Point location, Size size)
        {
            Button btn = new Button
            {
                Text = text,
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                Size = size,
                Location = location,
                Cursor = Cursors.Hand,
                FlatStyle = FlatStyle.Flat
            };

            btn.FlatAppearance.BorderSize = 0;
            btn.Paint += (sender, e) =>
            {
                Button button = (Button)sender;
                DrawCardGradient(button, e, color1, color2);

                StringFormat sf = new StringFormat();
                sf.Alignment = StringAlignment.Center;
                sf.LineAlignment = StringAlignment.Center;

                e.Graphics.DrawString(button.Text, button.Font, new SolidBrush(button.ForeColor),
                    new RectangleF(0, 0, button.Width, button.Height), sf);
            };

            // Hover effects
            btn.MouseEnter += (sender, e) => { btn.Cursor = Cursors.Hand; };
            btn.MouseLeave += (sender, e) => { btn.Cursor = Cursors.Default; };

            return btn;
        }

        // ------------ CREATE LOGIN FORM ----------------
        private void CreateLoginForm()
        {
            this.Controls.Clear();
            this.Text = "Health Mate - Login";
            this.Size = new Size(1400, 780);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.AutoScroll = false;

            // Set gradient background
            this.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(74, 107, 255), Color.FromArgb(106, 27, 154));

            // Header Panel
            Panel headerPanel = new Panel
            {
                Size = new Size(this.Width, 120),
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };
            headerPanel.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(32, 40, 68), Color.FromArgb(74, 107, 255));

            Label titleLabel = new Label
            {
                Text = "WELCOME BACK",
                Font = new Font("Segoe UI", 32, FontStyle.Bold),
                ForeColor = Color.White,
                AutoSize = true,
                Location = new Point((this.Width - 300) / 2, 30),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Main Login Card
            Panel loginCard = new Panel
            {
                Size = new Size(500, 450),
                Location = new Point((this.Width - 500) / 2, 150),
                BackColor = Color.Transparent
            };
            loginCard.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            Label loginTitle = new Label
            {
                Text = "Sign In to Your Account",
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(80, 30),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Form fields
            int fieldWidth = 350;
            int fieldX = (loginCard.Width - fieldWidth) / 2;

            Label userLabel = new Label
            {
                Text = "Username",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = darkBlue,
                AutoSize = true,
                Location = new Point(fieldX, 100),
                BackColor = Color.Transparent
            };

            TextBox userTextBox = new TextBox
            {
                Location = new Point(fieldX, 125),
                Size = new Size(fieldWidth, 40),
                Font = new Font("Segoe UI", 12),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label passLabel = new Label
            {
                Text = "Password",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = darkBlue,
                AutoSize = true,
                Location = new Point(fieldX, 185),
                BackColor = Color.Transparent
            };

            TextBox passTextBox = new TextBox
            {
                Location = new Point(fieldX, 210),
                Size = new Size(fieldWidth, 40),
                Font = new Font("Segoe UI", 12),
                PasswordChar = '•',
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            // Buttons
            Button loginBtn = CreateGradientButton("SIGN IN",
                Color.FromArgb(74, 107, 255), Color.FromArgb(110, 150, 255),
                new Point(fieldX, 280),
                new Size(fieldWidth, 45));

            Button backBtn = CreateGradientButton("BACK TO HOME",
                Color.FromArgb(108, 117, 125), Color.FromArgb(134, 142, 150),
                new Point(fieldX, 340),
                new Size(fieldWidth, 45));

            // Events
            loginBtn.Click += (s, e) => LoginUser(userTextBox.Text.Trim(), passTextBox.Text);
            backBtn.Click += (s, e) => ShowWelcomeScreen();

            // Build hierarchy
            loginCard.Controls.Add(loginTitle);
            loginCard.Controls.Add(userLabel);
            loginCard.Controls.Add(userTextBox);
            loginCard.Controls.Add(passLabel);
            loginCard.Controls.Add(passTextBox);
            loginCard.Controls.Add(loginBtn);
            loginCard.Controls.Add(backBtn);

            headerPanel.Controls.Add(titleLabel);

            this.Controls.Add(headerPanel);
            this.Controls.Add(loginCard);
        }

        // ------------ CREATE REGISTRATION FORM ---------
        private void CreateRegistrationForm()
        {
            this.Controls.Clear();
            this.Text = "Health Mate - Register";
            this.Size = new Size(1400, 780);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.AutoScroll = true;

            // Set gradient background
            this.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(106, 27, 154), Color.FromArgb(74, 107, 255));

            // Header Panel
            Panel headerPanel = new Panel
            {
                Size = new Size(this.Width, 120),
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };
            headerPanel.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(32, 40, 68), Color.FromArgb(106, 27, 154));

            Label titleLabel = new Label
            {
                Text = "CREATE ACCOUNT",
                Font = new Font("Segoe UI", 32, FontStyle.Bold),
                ForeColor = Color.White,
                AutoSize = true,
                Location = new Point((this.Width - 350) / 2, 30),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Registration Card
            Panel registerCard = new Panel
            {
                Size = new Size(600, 540),
                Location = new Point((this.Width - 600) / 2, 135),
                BackColor = Color.Transparent
            };
            registerCard.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            Label registerTitle = new Label
            {
                Text = "Join Health Mate Today",
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(150, 30),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Form fields
            int fieldWidth = 400;
            int fieldX = (registerCard.Width - fieldWidth) / 2;

            string[] labels = { "Full Name:", "Username:", "Email:", "Password:", "Confirm Password:" };
            TextBox[] textBoxes = new TextBox[5];

            for (int i = 0; i < labels.Length; i++)
            {
                Label label = new Label
                {
                    Text = labels[i],
                    Font = new Font("Segoe UI", 12, FontStyle.Bold),
                    ForeColor = darkBlue,
                    AutoSize = true,
                    Location = new Point(fieldX, 80 + (i * 75)),
                    BackColor = Color.Transparent
                };

                TextBox textBox = new TextBox
                {
                    Location = new Point(fieldX, 105 + (i * 75)),
                    Size = new Size(fieldWidth, 35),
                    Font = new Font("Segoe UI", 12),
                    BackColor = Color.FromArgb(248, 250, 252),
                    BorderStyle = BorderStyle.FixedSingle
                };

                if (i >= 3) textBox.PasswordChar = '•';
                textBoxes[i] = textBox;
                registerCard.Controls.Add(label);
                registerCard.Controls.Add(textBox);
            }

            // Buttons
            Button registerBtn = CreateGradientButton("REGISTER",
                successColor, Color.FromArgb(120, 224, 175),
                new Point(fieldX, 445),
                new Size(fieldWidth, 42));

            Button backBtn = CreateGradientButton("BACK TO HOME",
                Color.FromArgb(108, 117, 125), Color.FromArgb(134, 142, 150),
                new Point(fieldX, 490),
                new Size(fieldWidth, 42));

            // Add events
            registerBtn.Click += (s, e) => RegisterUser(textBoxes[0].Text, textBoxes[1].Text, textBoxes[2].Text, textBoxes[3].Text, textBoxes[4].Text);
            backBtn.Click += (s, e) => ShowWelcomeScreen();

            // Add controls
            registerCard.Controls.Add(registerTitle);
            registerCard.Controls.Add(registerBtn);
            registerCard.Controls.Add(backBtn);

            headerPanel.Controls.Add(titleLabel);

            this.Controls.Add(headerPanel);
            this.Controls.Add(registerCard);
        }

        private void LoginUser(string username, string password)
        {
            if (string.IsNullOrWhiteSpace(username) || string.IsNullOrWhiteSpace(password))
            {
                MessageBox.Show("Please enter username and password!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                string query = "SELECT id, username FROM users WHERE username=@username AND password=@password";
                DataTable result = ExecuteQuery(query,
                    new MySqlParameter("@username", username),
                    new MySqlParameter("@password", password));

                if (result.Rows.Count > 0)
                {
                    currentUserId = Convert.ToInt32(result.Rows[0]["id"]);
                    currentUsername = result.Rows[0]["username"].ToString();
                    MessageBox.Show($"Welcome {currentUsername}!", "Login Successful", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    CreateMainDashboard();
                }
                else
                {
                    MessageBox.Show("Invalid username or password!", "Login Failed", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Login Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // SINGLE RegisterUser METHOD - No Duplicates
        private void RegisterUser(string fullName, string username, string email, string password, string confirmPassword)
        {
            if (string.IsNullOrWhiteSpace(fullName) || string.IsNullOrWhiteSpace(username) || string.IsNullOrWhiteSpace(password))
            {
                MessageBox.Show("Please fill all required fields!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (password != confirmPassword)
            {
                MessageBox.Show("Passwords do not match!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                string checkQuery = "SELECT COUNT(*) as user_count FROM users WHERE username=@username";
                DataTable checkResult = ExecuteQuery(checkQuery, new MySqlParameter("@username", username));

                long exists = 0;
                if (checkResult.Rows.Count > 0 && checkResult.Rows[0]["user_count"] != DBNull.Value)
                {
                    exists = Convert.ToInt64(checkResult.Rows[0]["user_count"]);
                }

                if (exists > 0)
                {
                    MessageBox.Show("Username already exists!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                string insertQuery = @"INSERT INTO users (username, password, full_name, email) VALUES (@username, @password, @fullName, @email)";
                int rowsAffected = ExecuteNonQuery(insertQuery,
                    new MySqlParameter("@username", username),
                    new MySqlParameter("@password", password),
                    new MySqlParameter("@fullName", fullName),
                    new MySqlParameter("@email", email));

                if (rowsAffected > 0)
                {
                    MessageBox.Show("Registration successful! Please login.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    ShowWelcomeScreen();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Registration Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void CreateMainDashboard()
        {
            this.Controls.Clear();
            this.Text = $"Health Mate - Welcome {currentUsername}";
            this.Size = new Size(1400, 780);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = backgroundColor;
            this.AutoScroll = false;

            // Header with gradient
            Panel headerPanel = new Panel
            {
                Size = new Size(this.Width, 80),
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };
            headerPanel.Paint += (sender, e) => DrawGradientBackground(sender, e, Color.FromArgb(32, 40, 68), Color.FromArgb(74, 107, 255));

            Label welcomeLabel = new Label
            {
                Text = $"Welcome, {currentUsername}",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = Color.White,
                AutoSize = true,
                Location = new Point(30, 20),
                BackColor = Color.Transparent
            };

            Button logoutBtn = CreateGradientButton("Logout",
                dangerColor, Color.FromArgb(255, 138, 138),
                new Point(1200, 15),
                new Size(150, 45));

            logoutBtn.Click += (s, e) => { currentUserId = 0; currentUsername = ""; ShowWelcomeScreen(); };

            // Main content area
            Panel mainContent = new Panel
            {
                Size = new Size(this.Width, this.Height - 80),
                Location = new Point(0, 80),
                BackColor = backgroundColor
            };

            // Tab control with gradient styling
            TabControl mainTabControl = new TabControl
            {
                Location = new Point(20, 20),
                Size = new Size(1360, 630),
                Font = new Font("Segoe UI", 14),
                ItemSize = new Size(300, 70)
            };

            // Style the tab control
            mainTabControl.DrawMode = TabDrawMode.OwnerDrawFixed;
            mainTabControl.DrawItem += (sender, e) =>
            {
                if (e.Index >= 0 && e.Index < mainTabControl.TabPages.Count)
                {
                    TabPage page = mainTabControl.TabPages[e.Index];
                    using (Brush brush = new LinearGradientBrush(e.Bounds, primaryColor, secondaryColor, LinearGradientMode.Vertical))
                    {
                        e.Graphics.FillRectangle(brush, e.Bounds);
                    }

                    Rectangle paddedBounds = e.Bounds;
                    paddedBounds.Inflate(-2, -2);

                    using (Brush textBrush = new SolidBrush(Color.White))
                    {
                        StringFormat sf = new StringFormat();
                        sf.Alignment = StringAlignment.Center;
                        e.Graphics.DrawString(page.Text, e.Font, textBrush, paddedBounds, sf);
                    }
                }
            };

            CreateDashboardTab(mainTabControl);
            CreateHealthMetricsTab(mainTabControl);
            CreateMedicationsTab(mainTabControl);
            CreateRemindersTab(mainTabControl);

            mainContent.Controls.Add(mainTabControl);

            headerPanel.Controls.Add(welcomeLabel);
            headerPanel.Controls.Add(logoutBtn);

            this.Controls.Add(headerPanel);
            this.Controls.Add(mainContent);
        }

        private void CreateDashboardTab(TabControl tabControl)
        {
            TabPage tab = new TabPage("Dashboard");
            tab.BackColor = backgroundColor;
            tab.AutoScroll = true;

            // Summary Cards with gradients - FIXED: Safer approach
            string[] cardTitles = { "Health Records", "Active Medications", "Pending Reminders", "Avg Sleep (7 days)" };
            string[] cardValues = new string[4];

            // FIXED: Use list of color pairs instead of separate arrays
            var cardColorPairs = new List<Tuple<Color, Color>>
    {
        new Tuple<Color, Color>(Color.FromArgb(74, 107, 255), Color.FromArgb(110, 150, 255)),
        new Tuple<Color, Color>(Color.FromArgb(56, 203, 137), Color.FromArgb(120, 224, 175)),
        new Tuple<Color, Color>(Color.FromArgb(255, 193, 7), Color.FromArgb(255, 213, 79)),
        new Tuple<Color, Color>(Color.FromArgb(147, 112, 219), Color.FromArgb(179, 157, 219))
    };

            // Load data for cards
            try
            {
                string healthQuery = "SELECT COUNT(*) as record_count FROM health_metrics WHERE user_id=@userId";
                DataTable healthResult = ExecuteQuery(healthQuery, new MySqlParameter("@userId", currentUserId));
                cardValues[0] = (healthResult.Rows.Count > 0) ? healthResult.Rows[0]["record_count"].ToString() : "0";

                string medsQuery = "SELECT COUNT(*) as med_count FROM medications WHERE user_id=@userId AND is_active=TRUE";
                DataTable medsResult = ExecuteQuery(medsQuery, new MySqlParameter("@userId", currentUserId));
                cardValues[1] = (medsResult.Rows.Count > 0) ? medsResult.Rows[0]["med_count"].ToString() : "0";

                string remQuery = "SELECT COUNT(*) as rem_count FROM reminders WHERE user_id=@userId AND is_completed=FALSE";
                DataTable remResult = ExecuteQuery(remQuery, new MySqlParameter("@userId", currentUserId));
                cardValues[2] = (remResult.Rows.Count > 0) ? remResult.Rows[0]["rem_count"].ToString() : "0";

                string sleepQuery = "SELECT AVG(sleep_hours) as avg_sleep FROM health_metrics WHERE user_id=@userId AND record_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)";
                DataTable sleepResult = ExecuteQuery(sleepQuery, new MySqlParameter("@userId", currentUserId));
                if (sleepResult.Rows.Count > 0 && sleepResult.Rows[0]["avg_sleep"] != DBNull.Value)
                {
                    cardValues[3] = $"{Math.Round(Convert.ToDouble(sleepResult.Rows[0]["avg_sleep"]), 1)} hrs";
                }
                else
                {
                    cardValues[3] = "N/A";
                }
            }
            catch (Exception ex)
            {
                for (int i = 0; i < 4; i++) cardValues[i] = "0";
                Console.WriteLine(ex);
            }

            // FIXED: Safer card creation with local variables
            for (int i = 0; i < cardTitles.Length; i++)
            {
                // Ensure we don't exceed color pairs
                if (i < cardColorPairs.Count)
                {
                    // Store colors in local variables to avoid closure issues
                    Color color1 = cardColorPairs[i].Item1;
                    Color color2 = cardColorPairs[i].Item2;
                    string title = cardTitles[i];
                    string value = cardValues[i];

                    Panel cardPanel = new Panel
                    {
                        Size = new Size(300, 140),
                        Location = new Point(50 + (i * 320), 30),
                        BackColor = Color.Transparent
                    };

                    // FIXED: Use local variables in paint event to avoid index issues
                    cardPanel.Paint += (sender, e) =>
                    {
                        DrawCardGradient(sender, e, color1, color2);
                    };

                    Label titleLabel = new Label
                    {
                        Text = title,
                        Font = new Font("Segoe UI", 14, FontStyle.Bold),
                        ForeColor = Color.White,
                        Location = new Point(20, 25),
                        AutoSize = true,
                        BackColor = Color.Transparent
                    };

                    Label valueLabel = new Label
                    {
                        Text = value,
                        Font = new Font("Segoe UI", 28, FontStyle.Bold),
                        ForeColor = Color.White,
                        Location = new Point(20, 60),
                        AutoSize = true,
                        BackColor = Color.Transparent
                    };

                    cardPanel.Controls.Add(titleLabel);
                    cardPanel.Controls.Add(valueLabel);
                    tab.Controls.Add(cardPanel);
                }
            }

            // Recent Health Data Group
            Panel recentGroupPanel = new Panel
            {
                Size = new Size(1320, 300),
                Location = new Point(20, 200),
                BackColor = Color.Transparent
            };
            recentGroupPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            Label recentGroupLabel = new Label
            {
                Text = "Recent Health Records",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(20, 15),
                BackColor = Color.Transparent
            };

            DataGridView recentGrid = new DataGridView
            {
                Location = new Point(20, 50),
                Size = new Size(1280, 230),
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                ReadOnly = true,
                RowHeadersVisible = false,
                BackgroundColor = Color.White,
                Font = new Font("Segoe UI", 11),
                BorderStyle = BorderStyle.None
            };

            // Style the DataGridView
            recentGrid.ColumnHeadersDefaultCellStyle.BackColor = primaryColor;
            recentGrid.ColumnHeadersDefaultCellStyle.ForeColor = Color.White;
            recentGrid.ColumnHeadersDefaultCellStyle.Font = new Font("Segoe UI", 11, FontStyle.Bold);
            recentGrid.EnableHeadersVisualStyles = false;

            recentGrid.Columns.Add("Date", "Date");
            recentGrid.Columns.Add("Weight", "Weight (kg)");
            recentGrid.Columns.Add("BloodPressure", "Blood Pressure");
            recentGrid.Columns.Add("SleepHours", "Sleep Hours");

            LoadRecentHealthData(recentGrid);

            recentGroupPanel.Controls.Add(recentGroupLabel);
            recentGroupPanel.Controls.Add(recentGrid);
            tab.Controls.Add(recentGroupPanel);

            tabControl.TabPages.Add(tab);
        }

        private void LoadRecentHealthData(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT record_date, weight, systolic, diastolic, sleep_hours 
                       FROM health_metrics WHERE user_id=@userId 
                       ORDER BY record_date DESC LIMIT 5";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    string weight = row["weight"] != DBNull.Value ? Convert.ToDouble(row["weight"]).ToString("0.0") : "N/A";
                    string systolic = row["systolic"] != DBNull.Value ? row["systolic"].ToString() : "N/A";
                    string diastolic = row["diastolic"] != DBNull.Value ? row["diastolic"].ToString() : "N/A";
                    string sleep = row["sleep_hours"] != DBNull.Value ? Convert.ToDouble(row["sleep_hours"]).ToString("0.0") : "N/A";

                    string bp = (systolic != "N/A" && diastolic != "N/A") ? $"{systolic}/{diastolic}" : "N/A";

                    grid.Rows.Add(
                        Convert.ToDateTime(row["record_date"]).ToString("MM/dd/yyyy"),
                        weight,
                        bp,
                        sleep
                    );
                }

                if (data.Rows.Count == 0)
                {
                    grid.Rows.Add("No data available", "", "", "");
                }
            }
            catch (Exception ex)
            {
                grid.Rows.Add("Error loading data", "", "", "");
            }
        }

        // ------- CREATE HEALTH METRICS TAB ----------
        private void CreateHealthMetricsTab(TabControl tabControl)
        {
            TabPage tab = new TabPage("Health Metrics");
            tab.BackColor = backgroundColor;
            tab.AutoScroll = true;

            // Input Group with gradient
            Panel inputGroupPanel = new Panel
            {
                Size = new Size(1100, 150),
                Location = new Point(20, 20),
                BackColor = Color.Transparent
            };
            inputGroupPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            Label inputGroupLabel = new Label
            {
                Text = "Add New Health Record",
                Font = new Font("Segoe UI", 16, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(20, 15),
                BackColor = Color.Transparent
            };

            // Form controls
            Label weightLabel = new Label { Text = "Weight (kg):", Location = new Point(30, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox weightTextBox = new TextBox
            {
                Location = new Point(120, 55),
                Size = new Size(100, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label bpLabel = new Label { Text = "BP (sys/dia):", Location = new Point(240, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox systolicTextBox = new TextBox
            {
                Location = new Point(330, 55),
                Size = new Size(50, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };
            Label slashLabel = new Label { Text = "/", Location = new Point(385, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox diastolicTextBox = new TextBox
            {
                Location = new Point(395, 55),
                Size = new Size(50, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label sleepLabel = new Label { Text = "Sleep Hours:", Location = new Point(465, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox sleepTextBox = new TextBox
            {
                Location = new Point(550, 55),
                Size = new Size(100, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Button addMetricBtn = CreateGradientButton("Add Record",
                successColor, Color.FromArgb(120, 224, 175),
                new Point(900, 50),
                new Size(160, 40));

            // Data Grid View Panel
            Panel gridPanel = new Panel
            {
                Location = new Point(20, 190),
                Size = new Size(1100, 450),
                BackColor = Color.Transparent
            };
            gridPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            DataGridView metricsGrid = new DataGridView
            {
                Location = new Point(20, 20),
                Size = new Size(1060, 410),
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                ReadOnly = true,
                RowHeadersVisible = false,
                BackgroundColor = Color.White,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None
            };

            // Style the DataGridView
            metricsGrid.ColumnHeadersDefaultCellStyle.BackColor = primaryColor;
            metricsGrid.ColumnHeadersDefaultCellStyle.ForeColor = Color.White;
            metricsGrid.ColumnHeadersDefaultCellStyle.Font = new Font("Segoe UI", 11, FontStyle.Bold);
            metricsGrid.EnableHeadersVisualStyles = false;

            metricsGrid.Columns.Add("ID", "ID");
            metricsGrid.Columns["ID"].Visible = false; // Hide ID column but keep it for deletion
            metricsGrid.Columns.Add("Date", "Date");
            metricsGrid.Columns.Add("Weight", "Weight (kg)");
            metricsGrid.Columns.Add("BloodPressure", "Blood Pressure");
            metricsGrid.Columns.Add("SleepHours", "Sleep Hours");
            metricsGrid.Columns.Add("Actions", "Actions");

            // Add Button Click Event
            addMetricBtn.Click += (s, e) =>
            {
                if (ValidateHealthInput(weightTextBox.Text, systolicTextBox.Text, diastolicTextBox.Text, sleepTextBox.Text))
                {
                    AddHealthMetric(double.Parse(weightTextBox.Text), int.Parse(systolicTextBox.Text),
                        int.Parse(diastolicTextBox.Text), double.Parse(sleepTextBox.Text));
                    UpdateMetricsGrid(metricsGrid);

                    weightTextBox.Clear();
                    systolicTextBox.Clear();
                    diastolicTextBox.Clear();
                    sleepTextBox.Clear();

                    MessageBox.Show("Health record added successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            };

            // FIXED: Delete health record event - using ID instead of date
            metricsGrid.CellClick += (s, e) =>
            {
                if (e.ColumnIndex == 5 && e.RowIndex >= 0)
                {
                    string recordId = metricsGrid.Rows[e.RowIndex].Cells[0].Value.ToString();
                    var result = MessageBox.Show("Delete this health record?", "Confirm", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                    if (result == DialogResult.Yes)
                    {
                        DeleteHealthRecordById(recordId);
                        UpdateMetricsGrid(metricsGrid);
                    }
                }
            };

            // Add controls
            inputGroupPanel.Controls.Add(inputGroupLabel);
            inputGroupPanel.Controls.AddRange(new Control[] { weightLabel, weightTextBox, bpLabel,
        systolicTextBox, slashLabel, diastolicTextBox, sleepLabel, sleepTextBox, addMetricBtn });

            gridPanel.Controls.Add(metricsGrid);

            tab.Controls.Add(inputGroupPanel);
            tab.Controls.Add(gridPanel);
            tabControl.TabPages.Add(tab);

            UpdateMetricsGrid(metricsGrid);
        }

        private void AddHealthMetric(double weight, int systolic, int diastolic, double sleepHours)
        {
            ExecuteNonQuery(
                @"INSERT INTO health_metrics (user_id, weight, systolic, diastolic, sleep_hours) 
        VALUES (@userId, @weight, @systolic, @diastolic, @sleepHours)",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@weight", weight),
                new MySqlParameter("@systolic", systolic),
                new MySqlParameter("@diastolic", diastolic),
                new MySqlParameter("@sleepHours", sleepHours)
            );
        }

        // FIXED: Delete by ID instead of date for better accuracy
        private void DeleteHealthRecordById(string recordId)
        {
            ExecuteNonQuery(
                "DELETE FROM health_metrics WHERE user_id=@userId AND id=@recordId",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@recordId", recordId)
            );
        }

        private void UpdateMetricsGrid(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT id, record_date, weight, systolic, diastolic, sleep_hours 
                       FROM health_metrics WHERE user_id=@userId ORDER BY record_date DESC";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    string id = row["id"].ToString();
                    string weight = row["weight"] != DBNull.Value ? Convert.ToDouble(row["weight"]).ToString("0.0") : "N/A";
                    string systolic = row["systolic"] != DBNull.Value ? row["systolic"].ToString() : "N/A";
                    string diastolic = row["diastolic"] != DBNull.Value ? row["diastolic"].ToString() : "N/A";
                    string sleep = row["sleep_hours"] != DBNull.Value ? Convert.ToDouble(row["sleep_hours"]).ToString("0.0") : "N/A";

                    string bp = (systolic != "N/A" && diastolic != "N/A") ? $"{systolic}/{diastolic}" : "N/A";

                    grid.Rows.Add(
                        id,
                        Convert.ToDateTime(row["record_date"]).ToString("yyyy-MM-dd HH:mm"),
                        weight,
                        bp,
                        sleep,
                        "Delete"
                    );
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading health data: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private bool ValidateHealthInput(string weight, string systolic, string diastolic, string sleep)
        {
            if (string.IsNullOrWhiteSpace(weight) || string.IsNullOrWhiteSpace(systolic) ||
                string.IsNullOrWhiteSpace(diastolic) || string.IsNullOrWhiteSpace(sleep))
            {
                MessageBox.Show("Please fill all fields!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }

            if (!double.TryParse(weight, out double w) || w <= 0)
            {
                MessageBox.Show("Please enter valid weight!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }

            if (!int.TryParse(systolic, out int sys) || sys <= 0 || !int.TryParse(diastolic, out int dia) || dia <= 0)
            {
                MessageBox.Show("Please enter valid blood pressure!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }

            if (!double.TryParse(sleep, out double slp) || slp <= 0)
            {
                MessageBox.Show("Please enter valid sleep hours!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }

            return true;
        }

        private void CreateMedicationsTab(TabControl tabControl)
        {
            TabPage tab = new TabPage("Medications");
            tab.BackColor = backgroundColor;
            tab.AutoScroll = true;

            // Input Group with gradient
            Panel inputGroupPanel = new Panel
            {
                Size = new Size(1100, 150),
                Location = new Point(20, 20),
                BackColor = Color.Transparent
            };
            inputGroupPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            Label inputGroupLabel = new Label
            {
                Text = "Add New Medication",
                Font = new Font("Segoe UI", 16, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(20, 15),
                BackColor = Color.Transparent
            };

            // Form controls
            Label nameLabel = new Label { Text = "Medication Name:", Location = new Point(30, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox nameTextBox = new TextBox
            {
                Location = new Point(160, 55),
                Size = new Size(200, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label dosageLabel = new Label { Text = "Dosage:", Location = new Point(380, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox dosageTextBox = new TextBox
            {
                Location = new Point(440, 55),
                Size = new Size(200, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label timeLabel = new Label { Text = "Schedule Time:", Location = new Point(660, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            DateTimePicker timePicker = new DateTimePicker
            {
                Location = new Point(760, 55),
                Size = new Size(120, 30),
                Format = DateTimePickerFormat.Time,
                ShowUpDown = true,
                Font = new Font("Segoe UI", 10)
            };

            Button addMedBtn = CreateGradientButton("Add Medication",
                successColor, Color.FromArgb(120, 224, 175),
                new Point(920, 50),
                new Size(150, 40));

            // Medications List Panel
            Panel gridPanel = new Panel
            {
                Location = new Point(20, 190),
                Size = new Size(1100, 450),
                BackColor = Color.Transparent
            };
            gridPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            DataGridView medsGrid = new DataGridView
            {
                Location = new Point(20, 20),
                Size = new Size(1060, 410),
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                ReadOnly = true,
                RowHeadersVisible = false,
                BackgroundColor = Color.White,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None
            };

            // Style the DataGridView
            medsGrid.ColumnHeadersDefaultCellStyle.BackColor = primaryColor;
            medsGrid.ColumnHeadersDefaultCellStyle.ForeColor = Color.White;
            medsGrid.ColumnHeadersDefaultCellStyle.Font = new Font("Segoe UI", 11, FontStyle.Bold);
            medsGrid.EnableHeadersVisualStyles = false;

            medsGrid.Columns.Add("ID", "ID");
            medsGrid.Columns["ID"].Visible = false; // Hide ID column
            medsGrid.Columns.Add("Name", "Medication Name");
            medsGrid.Columns.Add("Dosage", "Dosage");
            medsGrid.Columns.Add("Schedule", "Schedule Time");
            medsGrid.Columns.Add("Added", "Added Date");
            medsGrid.Columns.Add("Status", "Status");
            medsGrid.Columns.Add("Actions", "Actions");

            // Add controls
            inputGroupPanel.Controls.Add(inputGroupLabel);
            inputGroupPanel.Controls.AddRange(new Control[] { nameLabel, nameTextBox, dosageLabel, dosageTextBox, timeLabel, timePicker, addMedBtn });

            // Events
            addMedBtn.Click += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(nameTextBox.Text))
                {
                    MessageBox.Show("Please enter medication name!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                AddMedication(nameTextBox.Text, dosageTextBox.Text, timePicker.Value);
                UpdateMedsGrid(medsGrid);

                nameTextBox.Clear();
                dosageTextBox.Clear();
                nameTextBox.Focus();

                MessageBox.Show("Medication added successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            };

            // FIXED: Delete medication by ID
            medsGrid.CellClick += (s, e) =>
            {
                if (e.ColumnIndex == 6 && e.RowIndex >= 0)
                {
                    string medId = medsGrid.Rows[e.RowIndex].Cells[0].Value.ToString();
                    string medName = medsGrid.Rows[e.RowIndex].Cells[1].Value.ToString();
                    var result = MessageBox.Show($"Delete medication '{medName}'?", "Confirm", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                    if (result == DialogResult.Yes)
                    {
                        DeleteMedicationById(medId);
                        UpdateMedsGrid(medsGrid);
                    }
                }
            };

            gridPanel.Controls.Add(medsGrid);

            tab.Controls.Add(inputGroupPanel);
            tab.Controls.Add(gridPanel);
            tabControl.TabPages.Add(tab);
            UpdateMedsGrid(medsGrid);
        }

        private void AddMedication(string name, string dosage, DateTime scheduleTime)
        {
            ExecuteNonQuery(
                @"INSERT INTO medications (user_id, name, dosage, schedule_time) 
        VALUES (@userId, @name, @dosage, @scheduleTime)",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@name", name),
                new MySqlParameter("@dosage", dosage),
                new MySqlParameter("@scheduleTime", scheduleTime.ToString("HH:mm:ss"))
            );
        }

        // FIXED: Delete by ID instead of name
        private void DeleteMedicationById(string medId)
        {
            ExecuteNonQuery(
                "DELETE FROM medications WHERE user_id=@userId AND id=@medId",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@medId", medId)
            );
        }

        private void UpdateMedsGrid(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT id, name, dosage, schedule_time, added_date, is_active 
                       FROM medications WHERE user_id=@userId ORDER BY added_date DESC";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    string id = row["id"].ToString();
                    string status = (row["is_active"] != DBNull.Value && Convert.ToBoolean(row["is_active"])) ? "Active" : "Inactive";
                    string schedule = row["schedule_time"] != DBNull.Value ?
                        TimeSpan.Parse(row["schedule_time"].ToString()).ToString(@"hh\:mm") : "N/A";
                    string addedDate = row["added_date"] != DBNull.Value ?
                        Convert.ToDateTime(row["added_date"]).ToString("yyyy-MM-dd") : "N/A";

                    grid.Rows.Add(
                        id,
                        row["name"].ToString(),
                        row["dosage"] != DBNull.Value ? row["dosage"].ToString() : "",
                        schedule,
                        addedDate,
                        status,
                        "❌ Delete"
                    );
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading medications: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void CreateRemindersTab(TabControl tabControl)
        {
            TabPage tab = new TabPage("Reminders");
            tab.BackColor = backgroundColor;
            tab.AutoScroll = true;

            // Input Group with gradient
            Panel inputGroupPanel = new Panel
            {
                Size = new Size(1100, 170),
                Location = new Point(20, 20),
                BackColor = Color.Transparent
            };
            inputGroupPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            Label inputGroupLabel = new Label
            {
                Text = "Add New Reminder",
                Font = new Font("Segoe UI", 16, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(20, 15),
                BackColor = Color.Transparent
            };

            // Form controls
            Label titleLabel = new Label { Text = "Reminder Title:", Location = new Point(30, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox titleTextBox = new TextBox
            {
                Location = new Point(140, 55),
                Size = new Size(300, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label descLabel = new Label { Text = "Description:", Location = new Point(30, 105), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            TextBox descTextBox = new TextBox
            {
                Location = new Point(140, 100),
                Size = new Size(300, 30),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.FromArgb(248, 250, 252),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label timeLabel = new Label { Text = "Reminder Time:", Location = new Point(460, 60), AutoSize = true, Font = new Font("Segoe UI", 10), BackColor = Color.Transparent };
            DateTimePicker reminderPicker = new DateTimePicker
            {
                Location = new Point(570, 55),
                Size = new Size(200, 30),
                Format = DateTimePickerFormat.Custom,
                CustomFormat = "MM/dd/yyyy hh:mm tt",
                Font = new Font("Segoe UI", 10)
            };

            Button addReminderBtn = CreateGradientButton("Add Reminder",
                successColor, Color.FromArgb(120, 224, 175),
                new Point(900, 55),
                new Size(160, 40));

            // Reminders List Panel
            Panel gridPanel = new Panel
            {
                Location = new Point(20, 210),
                Size = new Size(1100, 430),
                BackColor = Color.Transparent
            };
            gridPanel.Paint += (sender, e) => DrawCardGradient(sender, e, Color.White, Color.FromArgb(245, 247, 255));

            DataGridView remindersGrid = new DataGridView
            {
                Location = new Point(20, 20),
                Size = new Size(1060, 390),
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                ReadOnly = true,
                RowHeadersVisible = false,
                BackgroundColor = Color.White,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None
            };

            // Style the DataGridView
            remindersGrid.ColumnHeadersDefaultCellStyle.BackColor = primaryColor;
            remindersGrid.ColumnHeadersDefaultCellStyle.ForeColor = Color.White;
            remindersGrid.ColumnHeadersDefaultCellStyle.Font = new Font("Segoe UI", 11, FontStyle.Bold);
            remindersGrid.EnableHeadersVisualStyles = false;

            remindersGrid.Columns.Add("ID", "ID");
            remindersGrid.Columns["ID"].Visible = false; // Hide ID column
            remindersGrid.Columns.Add("Title", "Reminder Title");
            remindersGrid.Columns.Add("Description", "Description");
            remindersGrid.Columns.Add("Time", "Reminder Time");
            remindersGrid.Columns.Add("Status", "Status");
            remindersGrid.Columns.Add("Actions", "Actions");

            // Add controls
            inputGroupPanel.Controls.Add(inputGroupLabel);
            inputGroupPanel.Controls.AddRange(new Control[] { titleLabel, titleTextBox, descLabel, descTextBox, timeLabel, reminderPicker, addReminderBtn });

            // Events
            addReminderBtn.Click += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(titleTextBox.Text))
                {
                    MessageBox.Show("Please enter reminder title!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                AddReminder(titleTextBox.Text, descTextBox.Text, reminderPicker.Value);
                UpdateRemindersGrid(remindersGrid);

                titleTextBox.Clear();
                descTextBox.Clear();
                titleTextBox.Focus();

                MessageBox.Show("Reminder added successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            };

            // FIXED: Reminders actions - both complete and delete
            remindersGrid.CellClick += (s, e) =>
            {
                if (e.RowIndex >= 0)
                {
                    string reminderId = remindersGrid.Rows[e.RowIndex].Cells[0].Value.ToString();
                    string reminderTitle = remindersGrid.Rows[e.RowIndex].Cells[1].Value.ToString();
                    string currentStatus = remindersGrid.Rows[e.RowIndex].Cells[4].Value.ToString();

                    if (e.ColumnIndex == 5) // Actions column
                    {
                        if (currentStatus == "Pending")
                        {
                            var result = MessageBox.Show($"Mark reminder '{reminderTitle}' as completed?", "Confirm", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                            if (result == DialogResult.Yes)
                            {
                                CompleteReminderById(reminderId);
                                UpdateRemindersGrid(remindersGrid);
                            }
                        }
                        else
                        {
                            var result = MessageBox.Show($"Delete reminder '{reminderTitle}'?", "Confirm", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                            if (result == DialogResult.Yes)
                            {
                                DeleteReminderById(reminderId);
                                UpdateRemindersGrid(remindersGrid);
                            }
                        }
                    }
                }
            };

            gridPanel.Controls.Add(remindersGrid);

            tab.Controls.Add(inputGroupPanel);
            tab.Controls.Add(gridPanel);
            tabControl.TabPages.Add(tab);
            UpdateRemindersGrid(remindersGrid);
        }

        private void AddReminder(string title, string description, DateTime reminderTime)
        {
            ExecuteNonQuery(
                @"INSERT INTO reminders (user_id, title, description, reminder_time) 
        VALUES (@userId, @title, @description, @reminderTime)",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@title", title),
                new MySqlParameter("@description", description),
                new MySqlParameter("@reminderTime", reminderTime)
            );
        }

        // FIXED: Complete reminder by ID
        private void CompleteReminderById(string reminderId)
        {
            ExecuteNonQuery(
                "UPDATE reminders SET is_completed=TRUE WHERE user_id=@userId AND id=@reminderId",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@reminderId", reminderId)
            );
        }

        // FIXED: Delete reminder by ID
        private void DeleteReminderById(string reminderId)
        {
            ExecuteNonQuery(
                "DELETE FROM reminders WHERE user_id=@userId AND id=@reminderId",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@reminderId", reminderId)
            );
        }

        private void UpdateRemindersGrid(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT id, title, description, reminder_time, is_completed 
                       FROM reminders WHERE user_id=@userId ORDER BY reminder_time DESC";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    string id = row["id"].ToString();
                    bool isCompleted = row["is_completed"] != DBNull.Value && Convert.ToBoolean(row["is_completed"]);
                    string status = isCompleted ? "Completed" : "Pending";
                    string actionText = isCompleted ? "Delete" : "Complete";
                    string reminderTime = row["reminder_time"] != DBNull.Value ?
                        Convert.ToDateTime(row["reminder_time"]).ToString("MM/dd/yyyy hh:mm tt") : "N/A";

                    grid.Rows.Add(
                        id,
                        row["title"].ToString(),
                        row["description"] != DBNull.Value ? row["description"].ToString() : "",
                        reminderTime,
                        status,
                        actionText
                    );
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading reminders: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Helper method to create gradient panels for cards
        private Panel CreateGradientCard(Point location, Size size, Color color1, Color color2)
        {
            Panel card = new Panel
            {
                Location = location,
                Size = size,
                BackColor = Color.Transparent
            };
            card.Paint += (sender, e) => DrawCardGradient(sender, e, color1, color2);
            return card;
        }
    }
}