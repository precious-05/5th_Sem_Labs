using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace DiabetesCareManager
{
    public partial class Form1 : Form
    {
        private MySqlConnection connection;
        private string connectionString = "Server=localhost;Database=diabetes_care;Uid=root;Pwd=PRO_CODER#1;";
        private int currentUserId = 0;
        private string currentUsername = "";
        private Timer notificationTimer;
        private NotifyIcon trayIcon;

        // Modern Purple Color Scheme
        private Color primaryColor = Color.FromArgb(103, 58, 183);      // Deep Purple
        private Color secondaryColor = Color.FromArgb(156, 39, 176);    // Purple
        private Color accentColor = Color.FromArgb(255, 64, 129);       // Pink Accent
        private Color safeColor = Color.FromArgb(76, 175, 80);          // Green
        private Color warningColor = Color.FromArgb(255, 193, 7);       // Amber
        private Color dangerColor = Color.FromArgb(244, 67, 54);        // Red
        private Color infoColor = Color.FromArgb(33, 150, 243);         // Blue
        private Color backgroundColor = Color.FromArgb(250, 245, 255);  // Light Purple
        private Color darkColor = Color.FromArgb(33, 33, 33);           // Dark Gray
        private Color lightPurple = Color.FromArgb(237, 231, 246);      // Very Light Purple
        private Color mediumPurple = Color.FromArgb(179, 157, 219);     // Medium Purple

        // Layout containers
        private Panel sidebar;
        private Panel mainContentContainer;
        private TableLayoutPanel dashboardCards;

        public Form1()
        {
            // Set form properties
            this.Text = "Diabetes Care Manager";
            this.Size = new Size(1200, 700);
            this.MinimumSize = new Size(1000, 600);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = backgroundColor;
            this.Font = new Font("Segoe UI", 9);

            InitializeDatabase();
            SetupTrayIcon();
            StartNotificationTimer();
            ShowWelcomeScreen();
        }

        private void SetupTrayIcon()
        {
            trayIcon = new NotifyIcon();
            trayIcon.Icon = SystemIcons.Information;
            trayIcon.Text = "Diabetes Care Manager";
            trayIcon.Visible = false;
        }

        private void StartNotificationTimer()
        {
            notificationTimer = new Timer();
            notificationTimer.Interval = 60000; // Check every minute
            notificationTimer.Enabled = true;
            notificationTimer.Tick += (s, e) => CheckNotifications();
        }

        private void InitializeDatabase()
        {
            try
            {
                string createDbConnection = "Server=localhost;Uid=root;Pwd=PRO_CODER#1;";
                using (MySqlConnection conn = new MySqlConnection(createDbConnection))
                {
                    conn.Open();
                    string createDbQuery = @"CREATE DATABASE IF NOT EXISTS diabetes_care;";
                    MySqlCommand cmd = new MySqlCommand(createDbQuery, conn);
                    cmd.ExecuteNonQuery();
                }

                connection = new MySqlConnection(connectionString);
                connection.Open();

                string[] createTables = {
                    @"CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(100) NOT NULL,
                        diabetes_type INT DEFAULT 1,
                        diagnosis_date DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )",

                    @"CREATE TABLE IF NOT EXISTS glucose_readings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        glucose_value DECIMAL(5,1) NOT NULL,
                        reading_type ENUM('Fasting', 'Before Meal', 'After Meal', 'Bedtime', 'Random') NOT NULL,
                        meal_context VARCHAR(100),
                        notes TEXT,
                        reading_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status ENUM('Normal', 'Low', 'High', 'Critical') DEFAULT 'Normal',
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS medications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        name VARCHAR(100) NOT NULL,
                        medication_type ENUM('Insulin', 'Oral', 'Other') NOT NULL,
                        dosage VARCHAR(100),
                        units INT,
                        schedule_time TIME,
                        frequency ENUM('Daily', 'Weekly', 'As Needed') DEFAULT 'Daily',
                        is_active BOOLEAN DEFAULT TRUE,
                        last_taken DATETIME,
                        next_due DATETIME,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS food_log (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        food_item VARCHAR(200) NOT NULL,
                        carbs DECIMAL(6,2),
                        calories INT,
                        meal_type ENUM('Breakfast', 'Lunch', 'Dinner', 'Snack') NOT NULL,
                        log_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        insulin_dose DECIMAL(5,2),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS a1c_records (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        a1c_value DECIMAL(4,1) NOT NULL,
                        test_date DATE NOT NULL,
                        lab_name VARCHAR(100),
                        notes TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS hypoglycemia_events (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        glucose_before DECIMAL(5,1),
                        symptoms TEXT,
                        treatment TEXT,
                        recovery_time_minutes INT,
                        event_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS alerts (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        alert_type ENUM('Glucose', 'Medication', 'Appointment', 'General'),
                        message TEXT NOT NULL,
                        alert_time DATETIME,
                        is_read BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS doctor_visits (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        doctor_name VARCHAR(100),
                        visit_date DATE,
                        notes TEXT,
                        next_appointment DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )",

                    @"CREATE TABLE IF NOT EXISTS food_items (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        carbs_per_serving DECIMAL(6,2),
                        serving_size VARCHAR(100),
                        category VARCHAR(50)
                    )"
                };

                foreach (string query in createTables)
                {
                    MySqlCommand cmd = new MySqlCommand(query, connection);
                    cmd.ExecuteNonQuery();
                }

                // Insert default food items
                InsertDefaultFoodItems();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Database Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void InsertDefaultFoodItems()
        {
            try
            {
                string checkQuery = "SELECT COUNT(*) as count FROM food_items";
                var cmd = new MySqlCommand(checkQuery, connection);
                var count = Convert.ToInt32(cmd.ExecuteScalar());

                if (count == 0)
                {
                    string[] foodItems = {
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('White Bread (1 slice)', 15, '1 slice')",
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('Brown Rice (1 cup)', 45, '1 cup cooked')",
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('Apple (medium)', 25, '1 medium')",
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('Banana (medium)', 27, '1 medium')",
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('Orange Juice (1 cup)', 26, '1 cup')",
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('Potato (medium)', 37, '1 medium baked')",
                        "INSERT INTO food_items (name, carbs_per_serving, serving_size) VALUES ('Pasta (1 cup)', 43, '1 cup cooked')"
                    };

                    foreach (string query in foodItems)
                    {
                        new MySqlCommand(query, connection).ExecuteNonQuery();
                    }
                }
            }
            catch { /* Table might already exist with data */ }
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
                Console.WriteLine($"Query Error: {ex.Message}");
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
                Console.WriteLine($"Command Error: {ex.Message}");
                return -1;
            }
        }

        private void CheckNotifications()
        {
            if (currentUserId == 0) return;

            try
            {
                // Check for missed medications
                string medQuery = @"SELECT name, schedule_time FROM medications 
                                  WHERE user_id=@userId AND is_active=TRUE 
                                  AND next_due < NOW()";
                DataTable missedMeds = ExecuteQuery(medQuery, new MySqlParameter("@userId", currentUserId));

                if (missedMeds.Rows.Count > 0)
                {
                    ShowNotification("Missed Medication",
                        $"You missed: {missedMeds.Rows[0]["name"]} at {missedMeds.Rows[0]["schedule_time"]}");
                }

                // Check for critical glucose readings (last 30 minutes)
                string glucoseQuery = @"SELECT glucose_value FROM glucose_readings 
                                      WHERE user_id=@userId AND reading_time > DATE_SUB(NOW(), INTERVAL 30 MINUTE)
                                      AND (glucose_value < 70 OR glucose_value > 300)";
                DataTable criticalReadings = ExecuteQuery(glucoseQuery, new MySqlParameter("@userId", currentUserId));

                if (criticalReadings.Rows.Count > 0)
                {
                    ShowNotification("Critical Glucose Alert",
                        "You have dangerous glucose readings in the last 30 minutes!");
                }
            }
            catch { }
        }

        private void ShowNotification(string title, string message)
        {
            if (trayIcon != null)
            {
                trayIcon.Icon = SystemIcons.Warning;
                trayIcon.Visible = true;
                trayIcon.BalloonTipTitle = title;
                trayIcon.BalloonTipText = message;
                trayIcon.BalloonTipIcon = ToolTipIcon.Warning;
                trayIcon.ShowBalloonTip(5000);
            }
        }

        private void ShowWelcomeScreen()
        {
            this.Controls.Clear();
            this.BackColor = backgroundColor;
            this.Padding = new Padding(0);

            // Main container using TableLayoutPanel for perfect centering
            TableLayoutPanel mainContainer = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2,
                BackColor = Color.Transparent,
                Padding = new Padding(0)
            };
            mainContainer.RowStyles.Add(new RowStyle(SizeType.Percent, 40)); // Header
            mainContainer.RowStyles.Add(new RowStyle(SizeType.Percent, 60)); // Content

            // =================== HEADER PANEL ===================
            Panel headerPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = primaryColor
            };

            // Center container for header content
            TableLayoutPanel headerContent = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 3,
                BackColor = Color.Transparent
            };
            headerContent.RowStyles.Add(new RowStyle(SizeType.Percent, 50)); // Logo space
            headerContent.RowStyles.Add(new RowStyle(SizeType.Absolute, 50)); // Title
            headerContent.RowStyles.Add(new RowStyle(SizeType.Absolute, 30)); // Subtitle

            // Logo Container
            Panel logoContainer = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent
            };

            Panel logoCircle = new Panel
            {
                Size = new Size(80, 80),
                BackColor = Color.White
            };
            logoCircle.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                e.Graphics.FillEllipse(new SolidBrush(Color.White), 0, 0, 80, 80);
                e.Graphics.DrawString("D", new Font("Segoe UI", 36, FontStyle.Bold),
                    new SolidBrush(primaryColor), new PointF(22, 15));
            };

            // Main Title
            Label titleLabel = new Label
            {
                Text = "DIABETES CARE MANAGER",
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                ForeColor = Color.White,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Subtitle
            Label subtitleLabel = new Label
            {
                Text = "Your Personal Health Companion",
                Font = new Font("Segoe UI", 14, FontStyle.Regular),
                ForeColor = Color.White,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.TopCenter,
                BackColor = Color.Transparent
            };

            // Center logo in its container
            logoContainer.Controls.Add(logoCircle);
            headerContent.Controls.Add(logoContainer, 0, 0);
            headerContent.Controls.Add(titleLabel, 0, 1);
            headerContent.Controls.Add(subtitleLabel, 0, 2);
            headerPanel.Controls.Add(headerContent);

            // =================== CONTENT PANEL ===================
            Panel contentPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = backgroundColor,
                Padding = new Padding(50, 30, 50, 30)
            };

            // Center container for content
            TableLayoutPanel contentLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 3,
                BackColor = Color.Transparent,
                Padding = new Padding(0)
            };
            contentLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 150)); // Welcome card
            contentLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 20));  // Spacer
            contentLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 120)); // Buttons
            contentLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));  // Extra space

            // Welcome Card - CENTERED
            Panel welcomeCard = new Panel
            {
                BackColor = Color.White,
                Size = new Size(600, 150),
                Padding = new Padding(40, 20, 40, 20)
            };

            // Add rounded corners to welcome card
            welcomeCard.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                Rectangle rect = new Rectangle(0, 0, welcomeCard.Width - 1, welcomeCard.Height - 1);
                int radius = 15;

                GraphicsPath path = new GraphicsPath();
                path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                path.CloseFigure();

                e.Graphics.FillPath(new SolidBrush(Color.White), path);
                e.Graphics.DrawPath(new Pen(Color.FromArgb(220, 220, 220), 1), path);
            };

            // Welcome Text Container - FIXED: Using TableLayoutPanel for proper text layout
            TableLayoutPanel textContainer = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2,
                BackColor = Color.Transparent,
                Padding = new Padding(0)
            };
            textContainer.RowStyles.Add(new RowStyle(SizeType.Absolute, 50));  // Welcome label
            textContainer.RowStyles.Add(new RowStyle(SizeType.Percent, 100));  // Description label

            Label welcomeLabel = new Label
            {
                Text = "Welcome to Diabetes Care Manager",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = primaryColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.BottomCenter,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 0, 0, 5)
            };

            // FIXED: Description label - No DockStyle.Fill issue
            Label descriptionLabel = new Label
            {
                Text = "Track your glucose levels, medications, food intake,\nand A1C trends all in one comprehensive platform",
                Font = new Font("Segoe UI", 12),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.TopCenter,
                BackColor = Color.Transparent,
                Padding = new Padding(10, 5, 10, 0)
            };

            textContainer.Controls.Add(welcomeLabel, 0, 0);
            textContainer.Controls.Add(descriptionLabel, 0, 1);
            welcomeCard.Controls.Add(textContainer);

            // Buttons Container - PERFECTLY CENTERED
            Panel buttonsContainer = new Panel
            {
                BackColor = Color.Transparent,
                Size = new Size(500, 120)
            };

            // Buttons Panel with TableLayout - FIXED: Proper button layout
            TableLayoutPanel buttonsLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 3,
                BackColor = Color.Transparent,
                Padding = new Padding(50, 10, 50, 10)
            };
            buttonsLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 50)); // Register button
            buttonsLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 15)); // Spacer
            buttonsLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 45)); // Login button

            // Register Button - MODERN STYLE
            Button registerBtn = new Button
            {
                Text = "GET STARTED →",
                Font = new Font("Segoe UI", 13, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Dock = DockStyle.Fill,
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            registerBtn.FlatAppearance.BorderSize = 0;
            registerBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 100, 150);

            // Add rounded corners to button
            registerBtn.Paint += (sender, e) =>
            {
                Button btn = (Button)sender;
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                Rectangle rect = new Rectangle(0, 0, btn.Width - 1, btn.Height - 1);
                int radius = 25;

                GraphicsPath path = new GraphicsPath();
                path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                path.CloseFigure();

                e.Graphics.FillPath(new SolidBrush(btn.BackColor), path);

                // Draw text
                StringFormat sf = new StringFormat();
                sf.Alignment = StringAlignment.Center;
                sf.LineAlignment = StringAlignment.Center;
                e.Graphics.DrawString(btn.Text, btn.Font, new SolidBrush(btn.ForeColor), rect, sf);
            };

            // Login Button - MODERN STYLE
            Button loginBtn = new Button
            {
                Text = "I ALREADY HAVE AN ACCOUNT",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = primaryColor,
                Dock = DockStyle.Fill,
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            loginBtn.FlatAppearance.BorderSize = 0;
            loginBtn.FlatAppearance.MouseOverBackColor = secondaryColor;

            // Add rounded corners to login button
            loginBtn.Paint += (sender, e) =>
            {
                Button btn = (Button)sender;
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                Rectangle rect = new Rectangle(0, 0, btn.Width - 1, btn.Height - 1);
                int radius = 22;

                GraphicsPath path = new GraphicsPath();
                path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                path.CloseFigure();

                e.Graphics.FillPath(new SolidBrush(btn.BackColor), path);

                // Draw text
                StringFormat sf = new StringFormat();
                sf.Alignment = StringAlignment.Center;
                sf.LineAlignment = StringAlignment.Center;
                e.Graphics.DrawString(btn.Text, btn.Font, new SolidBrush(btn.ForeColor), rect, sf);
            };

            // Add button events
            registerBtn.Click += (s, e) => CreateRegistrationForm();
            loginBtn.Click += (s, e) => CreateLoginForm();

            // Add buttons to layout
            buttonsLayout.Controls.Add(registerBtn, 0, 0);
            buttonsLayout.Controls.Add(new Panel { BackColor = Color.Transparent }, 0, 1); // Spacer
            buttonsLayout.Controls.Add(loginBtn, 0, 2);

            buttonsContainer.Controls.Add(buttonsLayout);

            // FIXED: Add a container to center the welcome card and buttons
            Panel centerContainer = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent
            };

            // Add welcome card and buttons to center container
            centerContainer.Controls.Add(welcomeCard);
            centerContainer.Controls.Add(buttonsContainer);

            // Center the elements vertically
            contentLayout.Controls.Add(centerContainer, 0, 0);
            contentLayout.SetRowSpan(centerContainer, 4); // Span all rows

            contentPanel.Controls.Add(contentLayout);

            // Add panels to main container
            mainContainer.Controls.Add(headerPanel, 0, 0);
            mainContainer.Controls.Add(contentPanel, 0, 1);

            // FIXED: Center everything after the layout is complete
            this.Layout += (s, e) =>
            {
                // Center logo in header
                if (logoCircle != null && logoContainer != null)
                {
                    logoCircle.Location = new Point(
                        (logoContainer.Width - logoCircle.Width) / 2,
                        (logoContainer.Height - logoCircle.Height) / 2
                    );
                }

                // Center welcome card
                if (welcomeCard != null && centerContainer != null)
                {
                    welcomeCard.Location = new Point(
                        (centerContainer.Width - welcomeCard.Width) / 2,
                        0
                    );
                }

                // Center buttons container below welcome card
                if (buttonsContainer != null && welcomeCard != null && centerContainer != null)
                {
                    buttonsContainer.Location = new Point(
                        (centerContainer.Width - buttonsContainer.Width) / 2,
                        welcomeCard.Bottom + 20
                    );
                }
            };

            this.Controls.Add(mainContainer);

            // Force layout to trigger centering
            this.PerformLayout();
        }

        private void CreateLoginForm()
        {
            this.Controls.Clear();
            this.BackColor = backgroundColor;

            // Main container
            TableLayoutPanel mainLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2,
                BackColor = backgroundColor
            };
            mainLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 120)); // Header
            mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));  // Content

            // ========== HEADER ==========
            Panel headerPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = primaryColor
            };

            Label loginTitle = new Label
            {
                Text = "Welcome Back",
                Font = new Font("Segoe UI", 28, FontStyle.Bold),
                ForeColor = Color.White,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };
            headerPanel.Controls.Add(loginTitle);

            // ========== CONTENT ==========
            Panel contentPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = backgroundColor,
                Padding = new Padding(0)
            };

            // Login Card with rounded corners
            Panel loginCard = new Panel
            {
                Size = new Size(420, 420),
                BackColor = Color.White,
                Padding = new Padding(40, 30, 40, 30)
            };

            // Draw rounded corners manually
            loginCard.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                // Draw white rounded rectangle
                Rectangle rect = new Rectangle(0, 0, loginCard.Width - 1, loginCard.Height - 1);
                int radius = 15;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(Color.White), path);
                    e.Graphics.DrawPath(new Pen(Color.FromArgb(230, 230, 230), 1), path);
                }
            };

            // Card Title
            Label cardTitle = new Label
            {
                Text = "SIGN IN",
                Font = new Font("Segoe UI", 22, FontStyle.Bold),
                ForeColor = primaryColor,
                Size = new Size(340, 40),
                Location = new Point(40, 10),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Username Field
            Panel usernamePanel = new Panel
            {
                Size = new Size(340, 70),
                Location = new Point(40, 70),
                BackColor = Color.Transparent
            };

            Label userLabel = new Label
            {
                Text = "Username",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Location = new Point(5, 0),
                AutoSize = true
            };

            Panel usernameInput = new Panel
            {
                Size = new Size(340, 40),
                Location = new Point(0, 25),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            TextBox userTextBox = new TextBox
            {
                Font = new Font("Segoe UI", 11),
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Size = new Size(330, 35),
                Location = new Point(5, 2)
            };

            // Add placeholder manually
            userTextBox.Enter += (s, e) =>
            {
                if (userTextBox.Text == "Enter username")
                {
                    userTextBox.Text = "";
                    userTextBox.ForeColor = Color.Black;
                }
            };

            userTextBox.Leave += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(userTextBox.Text))
                {
                    userTextBox.Text = "Enter username";
                    userTextBox.ForeColor = Color.Gray;
                }
            };

            if (string.IsNullOrWhiteSpace(userTextBox.Text))
            {
                userTextBox.Text = "Enter username";
                userTextBox.ForeColor = Color.Gray;
            }

            // Password Field
            Panel passwordPanel = new Panel
            {
                Size = new Size(340, 70),
                Location = new Point(40, 150),
                BackColor = Color.Transparent
            };

            Label passLabel = new Label
            {
                Text = "Password",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Location = new Point(5, 0),
                AutoSize = true
            };

            Panel passwordInput = new Panel
            {
                Size = new Size(340, 40),
                Location = new Point(0, 25),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            TextBox passTextBox = new TextBox
            {
                Font = new Font("Segoe UI", 11),
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Size = new Size(330, 35),
                Location = new Point(5, 2),
                PasswordChar = '•'
            };

            // Add placeholder for password
            passTextBox.Enter += (s, e) =>
            {
                if (passTextBox.Text == "Enter password")
                {
                    passTextBox.Text = "";
                    passTextBox.ForeColor = Color.Black;
                    passTextBox.PasswordChar = '•';
                }
            };

            passTextBox.Leave += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(passTextBox.Text))
                {
                    passTextBox.Text = "Enter password";
                    passTextBox.ForeColor = Color.Gray;
                    passTextBox.PasswordChar = '\0';
                }
            };

            if (string.IsNullOrWhiteSpace(passTextBox.Text))
            {
                passTextBox.Text = "Enter password";
                passTextBox.ForeColor = Color.Gray;
                passTextBox.PasswordChar = '\0';
            }

            // Login Button
            Button loginBtn = new Button
            {
                Text = "SIGN IN",
                Font = new Font("Segoe UI", 13, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(340, 45),
                Location = new Point(40, 240),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            loginBtn.FlatAppearance.BorderSize = 0;
            loginBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 85, 140);

            // Add rounded corners to button
            loginBtn.Paint += (sender, e) =>
            {
                Button btn = (Button)sender;
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                Rectangle rect = new Rectangle(0, 0, btn.Width - 1, btn.Height - 1);
                int radius = 22;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(btn.BackColor), path);

                    // Draw text
                    StringFormat sf = new StringFormat();
                    sf.Alignment = StringAlignment.Center;
                    sf.LineAlignment = StringAlignment.Center;
                    e.Graphics.DrawString(btn.Text, btn.Font, new SolidBrush(btn.ForeColor), rect, sf);
                }
            };

            // Back Button
            Button backBtn = new Button
            {
                Text = "← Back to Home",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = primaryColor,
                BackColor = Color.Transparent,
                Size = new Size(340, 35),
                Location = new Point(40, 300),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            backBtn.FlatAppearance.BorderSize = 0;
            backBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(240, 240, 240);

            // Add events
            loginBtn.Click += (s, e) => LoginUser(userTextBox.Text.Trim(), passTextBox.Text);
            backBtn.Click += (s, e) => ShowWelcomeScreen();

            // Add controls to panels
            usernamePanel.Controls.Add(userLabel);
            usernameInput.Controls.Add(userTextBox);
            usernamePanel.Controls.Add(usernameInput);

            passwordPanel.Controls.Add(passLabel);
            passwordInput.Controls.Add(passTextBox);
            passwordPanel.Controls.Add(passwordInput);

            loginCard.Controls.Add(cardTitle);
            loginCard.Controls.Add(usernamePanel);
            loginCard.Controls.Add(passwordPanel);
            loginCard.Controls.Add(loginBtn);
            loginCard.Controls.Add(backBtn);

            // Center the login card
            contentPanel.Controls.Add(loginCard);

            // Layout event to center the card
            contentPanel.Layout += (s, e) =>
            {
                loginCard.Location = new Point(
                    (contentPanel.Width - loginCard.Width) / 2,
                    (contentPanel.Height - loginCard.Height) / 2
                );
            };

            // Add to main layout
            mainLayout.Controls.Add(headerPanel, 0, 0);
            mainLayout.Controls.Add(contentPanel, 0, 1);

            this.Controls.Add(mainLayout);
        }

        private void CreateRegistrationForm()
        {
            this.Controls.Clear();
            this.BackColor = backgroundColor;

            // Main container
            TableLayoutPanel mainLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2,
                BackColor = backgroundColor
            };
            mainLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 100)); // Header
            mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));  // Content

            // ========== HEADER ==========
            Panel headerPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = primaryColor
            };

            Label registerTitle = new Label
            {
                Text = "Create Account",
                Font = new Font("Segoe UI", 26, FontStyle.Bold),
                ForeColor = Color.White,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };
            headerPanel.Controls.Add(registerTitle);

            // ========== CONTENT ==========
            Panel contentPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = backgroundColor,
                AutoScroll = true,
                Padding = new Padding(20)
            };

            // Registration Card
            Panel registerCard = new Panel
            {
                Size = new Size(480, 520),
                BackColor = Color.White,
                Padding = new Padding(40, 30, 40, 30)
            };

            // Draw rounded corners
            registerCard.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                // Draw white rounded rectangle
                Rectangle rect = new Rectangle(0, 0, registerCard.Width - 1, registerCard.Height - 1);
                int radius = 15;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(Color.White), path);
                    e.Graphics.DrawPath(new Pen(Color.FromArgb(230, 230, 230), 1), path);
                }
            };

            // Card Title
            Label cardTitle = new Label
            {
                Text = "CREATE YOUR ACCOUNT",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = primaryColor,
                Size = new Size(400, 40),
                Location = new Point(40, 10),
                TextAlign = ContentAlignment.MiddleCenter,
                BackColor = Color.Transparent
            };

            // Form Container
            Panel formContainer = new Panel
            {
                Size = new Size(400, 380),
                Location = new Point(40, 60),
                BackColor = Color.Transparent
            };

            int fieldWidth = 400;
            int currentY = 0;

            // Username Field
            Panel usernamePanel = new Panel
            {
                Size = new Size(fieldWidth, 70),
                Location = new Point(0, currentY),
                BackColor = Color.Transparent
            };

            Label usernameLabel = new Label
            {
                Text = "Username:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Location = new Point(5, 0),
                AutoSize = true
            };

            Panel usernameInput = new Panel
            {
                Size = new Size(fieldWidth, 40),
                Location = new Point(0, 25),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            TextBox usernameTextBox = new TextBox
            {
                Font = new Font("Segoe UI", 11),
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Size = new Size(fieldWidth - 10, 35),
                Location = new Point(5, 2)
            };

            // Add placeholder for username
            usernameTextBox.Enter += (s, e) =>
            {
                if (usernameTextBox.Text == "Enter username")
                {
                    usernameTextBox.Text = "";
                    usernameTextBox.ForeColor = Color.Black;
                }
            };

            usernameTextBox.Leave += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(usernameTextBox.Text))
                {
                    usernameTextBox.Text = "Enter username";
                    usernameTextBox.ForeColor = Color.Gray;
                }
            };

            if (string.IsNullOrWhiteSpace(usernameTextBox.Text))
            {
                usernameTextBox.Text = "Enter username";
                usernameTextBox.ForeColor = Color.Gray;
            }

            usernameInput.Controls.Add(usernameTextBox);
            usernamePanel.Controls.Add(usernameLabel);
            usernamePanel.Controls.Add(usernameInput);
            formContainer.Controls.Add(usernamePanel);

            currentY += 70;

            // Password Field
            Panel passwordPanel = new Panel
            {
                Size = new Size(fieldWidth, 70),
                Location = new Point(0, currentY),
                BackColor = Color.Transparent
            };

            Label passwordLabel = new Label
            {
                Text = "Password:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Location = new Point(5, 0),
                AutoSize = true
            };

            Panel passwordInput = new Panel
            {
                Size = new Size(fieldWidth, 40),
                Location = new Point(0, 25),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            TextBox passwordTextBox = new TextBox
            {
                Font = new Font("Segoe UI", 11),
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Size = new Size(fieldWidth - 10, 35),
                Location = new Point(5, 2),
                PasswordChar = '•'
            };

            // Add placeholder for password
            passwordTextBox.Enter += (s, e) =>
            {
                if (passwordTextBox.Text == "Enter password")
                {
                    passwordTextBox.Text = "";
                    passwordTextBox.ForeColor = Color.Black;
                    passwordTextBox.PasswordChar = '•';
                }
            };

            passwordTextBox.Leave += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(passwordTextBox.Text))
                {
                    passwordTextBox.Text = "Enter password";
                    passwordTextBox.ForeColor = Color.Gray;
                    passwordTextBox.PasswordChar = '\0';
                }
            };

            if (string.IsNullOrWhiteSpace(passwordTextBox.Text))
            {
                passwordTextBox.Text = "Enter password";
                passwordTextBox.ForeColor = Color.Gray;
                passwordTextBox.PasswordChar = '\0';
            }

            passwordInput.Controls.Add(passwordTextBox);
            passwordPanel.Controls.Add(passwordLabel);
            passwordPanel.Controls.Add(passwordInput);
            formContainer.Controls.Add(passwordPanel);

            currentY += 70;

            // Confirm Password Field
            Panel confirmPassPanel = new Panel
            {
                Size = new Size(fieldWidth, 70),
                Location = new Point(0, currentY),
                BackColor = Color.Transparent
            };

            Label confirmPassLabel = new Label
            {
                Text = "Confirm Password:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Location = new Point(5, 0),
                AutoSize = true
            };

            Panel confirmPassInput = new Panel
            {
                Size = new Size(fieldWidth, 40),
                Location = new Point(0, 25),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            TextBox confirmPassTextBox = new TextBox
            {
                Font = new Font("Segoe UI", 11),
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Size = new Size(fieldWidth - 10, 35),
                Location = new Point(5, 2),
                PasswordChar = '•'
            };

            // Add placeholder for confirm password
            confirmPassTextBox.Enter += (s, e) =>
            {
                if (confirmPassTextBox.Text == "Confirm password")
                {
                    confirmPassTextBox.Text = "";
                    confirmPassTextBox.ForeColor = Color.Black;
                    confirmPassTextBox.PasswordChar = '•';
                }
            };

            confirmPassTextBox.Leave += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(confirmPassTextBox.Text))
                {
                    confirmPassTextBox.Text = "Confirm password";
                    confirmPassTextBox.ForeColor = Color.Gray;
                    confirmPassTextBox.PasswordChar = '\0';
                }
            };

            if (string.IsNullOrWhiteSpace(confirmPassTextBox.Text))
            {
                confirmPassTextBox.Text = "Confirm password";
                confirmPassTextBox.ForeColor = Color.Gray;
                confirmPassTextBox.PasswordChar = '\0';
            }

            confirmPassInput.Controls.Add(confirmPassTextBox);
            confirmPassPanel.Controls.Add(confirmPassLabel);
            confirmPassPanel.Controls.Add(confirmPassInput);
            formContainer.Controls.Add(confirmPassPanel);

            currentY += 70;

            // Diabetes Type Field - FIXED: Removed BorderStyle from ComboBox
            Panel typePanel = new Panel
            {
                Size = new Size(fieldWidth, 70),
                Location = new Point(0, currentY),
                BackColor = Color.Transparent
            };

            Label typeLabel = new Label
            {
                Text = "Diabetes Type:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Location = new Point(5, 0),
                AutoSize = true
            };

            Panel typeInput = new Panel
            {
                Size = new Size(fieldWidth, 40),
                Location = new Point(0, 25),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            ComboBox typeCombo = new ComboBox
            {
                Font = new Font("Segoe UI", 11),
                BackColor = Color.White,
                // REMOVED: BorderStyle = BorderStyle.None, // ComboBox doesn't have BorderStyle property
                Size = new Size(fieldWidth - 10, 35),
                Location = new Point(5, 2),
                DropDownStyle = ComboBoxStyle.DropDownList,
                FlatStyle = FlatStyle.Flat // Added for better appearance
            };
            typeCombo.Items.AddRange(new string[] { "Type 1", "Type 2", "Gestational", "Pre-Diabetes", "Other" });
            typeCombo.SelectedIndex = 0;

            typeInput.Controls.Add(typeCombo);
            typePanel.Controls.Add(typeLabel);
            typePanel.Controls.Add(typeInput);
            formContainer.Controls.Add(typePanel);

            currentY += 80;

            // Register Button
            Button registerBtn = new Button
            {
                Text = "CREATE ACCOUNT",
                Font = new Font("Segoe UI", 13, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(fieldWidth, 45),
                Location = new Point(0, currentY),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            registerBtn.FlatAppearance.BorderSize = 0;
            registerBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 85, 140);

            // Add rounded corners to register button
            registerBtn.Paint += (sender, e) =>
            {
                Button btn = (Button)sender;
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                Rectangle rect = new Rectangle(0, 0, btn.Width - 1, btn.Height - 1);
                int radius = 22;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(btn.BackColor), path);

                    StringFormat sf = new StringFormat();
                    sf.Alignment = StringAlignment.Center;
                    sf.LineAlignment = StringAlignment.Center;
                    e.Graphics.DrawString(btn.Text, btn.Font, new SolidBrush(btn.ForeColor), rect, sf);
                }
            };

            formContainer.Controls.Add(registerBtn);

            currentY += 60;

            // Back Button
            Button backBtn = new Button
            {
                Text = "← Back to Home",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = primaryColor,
                BackColor = Color.Transparent,
                Size = new Size(fieldWidth, 35),
                Location = new Point(0, currentY),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            backBtn.FlatAppearance.BorderSize = 0;
            backBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(240, 240, 240);

            formContainer.Controls.Add(backBtn);

            // Events
            registerBtn.Click += (s, e) =>
            {
                // Get actual values (remove placeholder text)
                string username = usernameTextBox.Text.Trim();
                string password = passwordTextBox.Text;
                string confirmPassword = confirmPassTextBox.Text;

                if (username == "Enter username" || string.IsNullOrWhiteSpace(username))
                {
                    MessageBox.Show("Please enter a username!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                if (password == "Enter password" || string.IsNullOrWhiteSpace(password))
                {
                    MessageBox.Show("Please enter a password!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                if (password != confirmPassword)
                {
                    MessageBox.Show("Passwords do not match!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                string diabetesType = typeCombo.SelectedItem.ToString();

                int diabetesTypeId = 2; // Default to Type 2
                if (diabetesType.Contains("1")) diabetesTypeId = 1;
                else if (diabetesType.Contains("Gestational")) diabetesTypeId = 3;
                else if (diabetesType.Contains("Pre")) diabetesTypeId = 4;
                else if (diabetesType.Contains("Other")) diabetesTypeId = 5;

                RegisterUser(username, password, diabetesTypeId, DateTime.Now.AddYears(-1));
            };

            backBtn.Click += (s, e) => ShowWelcomeScreen();

            // Add to card
            registerCard.Controls.Add(cardTitle);
            registerCard.Controls.Add(formContainer);

            // Center the card
            contentPanel.Controls.Add(registerCard);

            // Layout event to center the card
            contentPanel.Layout += (s, e) =>
            {
                registerCard.Location = new Point(
                    (contentPanel.ClientSize.Width - registerCard.Width) / 2,
                    20
                );
            };

            // Add to main layout
            mainLayout.Controls.Add(headerPanel, 0, 0);
            mainLayout.Controls.Add(contentPanel, 0, 1);

            this.Controls.Add(mainLayout);
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

                    // Show tray icon
                    if (trayIcon != null)
                    {
                        trayIcon.Visible = true;
                        trayIcon.Text = $"Diabetes Care - {currentUsername}";
                    }

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

        private void RegisterUser(string username, string password, int diabetesType, DateTime diagnosisDate)
        {
            // Validation
            if (string.IsNullOrWhiteSpace(username) || string.IsNullOrWhiteSpace(password))
            {
                MessageBox.Show("Please fill all required fields!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                // Check if username exists
                string checkQuery = "SELECT COUNT(*) as user_count FROM users WHERE username=@username";
                DataTable checkResult = ExecuteQuery(checkQuery, new MySqlParameter("@username", username));

                if (checkResult.Rows.Count > 0 && Convert.ToInt64(checkResult.Rows[0]["user_count"]) > 0)
                {
                    MessageBox.Show("Username already exists!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Insert user
                string insertQuery = @"INSERT INTO users (username, password, diabetes_type, diagnosis_date) 
                                     VALUES (@username, @password, @diabetesType, @diagnosisDate)";

                int rowsAffected = ExecuteNonQuery(insertQuery,
                    new MySqlParameter("@username", username),
                    new MySqlParameter("@password", password),
                    new MySqlParameter("@diabetesType", diabetesType),
                    new MySqlParameter("@diagnosisDate", diagnosisDate));

                if (rowsAffected > 0)
                {
                    MessageBox.Show("Registration successful! Please login to manage your diabetes.",
                        "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
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
            this.BackColor = backgroundColor;

            // Main container with TableLayoutPanel
            TableLayoutPanel mainLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 1,
                Margin = new Padding(0)
            };
            mainLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 200)); // Sidebar
            mainLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));   // Main content

            // Sidebar - FIXED WIDTH, anchored properly
            sidebar = new Panel
            {
                BackColor = primaryColor,
                Dock = DockStyle.Fill,
                Padding = new Padding(0)
            };

            // Sidebar Logo
            Panel sidebarLogo = new Panel
            {
                Size = new Size(200, 100),
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };
            sidebarLogo.Paint += (sender, e) =>
            {
                e.Graphics.FillRectangle(new SolidBrush(primaryColor), 0, 0, 200, 100);
                e.Graphics.DrawString("D", new Font("Segoe UI", 36, FontStyle.Bold),
                    Brushes.White, new PointF(70, 20));
                e.Graphics.DrawString("CARE", new Font("Segoe UI", 14, FontStyle.Bold),
                    Brushes.White, new PointF(75, 65));
            };

            // Navigation Buttons Container
            Panel navContainer = new Panel
            {
                Location = new Point(0, 100),
                Size = new Size(200, 400),
                BackColor = Color.Transparent
            };

            string[] navItems = { "📊 Dashboard", "🩸 Glucose Log", "💊 Medications",
                                "🍎 Food Tracker", "📈 A1C Trends", "📅 Doctor Visits", "⚙️ Settings" };

            for (int i = 0; i < navItems.Length; i++)
            {
                Button navBtn = new Button
                {
                    Text = navItems[i],
                    Font = new Font("Segoe UI", 10),
                    ForeColor = Color.White,
                    BackColor = Color.Transparent,
                    Size = new Size(200, 45),
                    Location = new Point(0, i * 45),
                    FlatStyle = FlatStyle.Flat,
                    TextAlign = ContentAlignment.MiddleLeft,
                    Padding = new Padding(15, 0, 0, 0),
                    Cursor = Cursors.Hand,
                    Tag = i
                };

                navBtn.FlatAppearance.BorderSize = 0;
                navBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(100, 255, 255, 255);
                navBtn.FlatAppearance.MouseDownBackColor = accentColor;

                navBtn.Click += (s, e) =>
                {
                    if (s is Button btn && btn.Tag is int index)
                    {
                        ShowTabContent(index);
                    }
                };

                navContainer.Controls.Add(navBtn);
            }

            // Logout Button - anchored to bottom
            Button logoutBtn = new Button
            {
                Text = "🚪 Logout",
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.White,
                BackColor = Color.Transparent,
                Size = new Size(200, 45),
                Location = new Point(0, this.ClientSize.Height - 80),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleLeft,
                Padding = new Padding(15, 0, 0, 0),
                Cursor = Cursors.Hand,
                Anchor = AnchorStyles.Bottom | AnchorStyles.Left
            };
            logoutBtn.FlatAppearance.BorderSize = 0;
            logoutBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(100, 244, 67, 54);
            logoutBtn.Click += (s, e) =>
            {
                currentUserId = 0;
                if (trayIcon != null) trayIcon.Visible = false;
                ShowWelcomeScreen();
            };

            sidebar.Controls.Add(sidebarLogo);
            sidebar.Controls.Add(navContainer);
            sidebar.Controls.Add(logoutBtn);

            // Main Content Area - PROPERLY ANCHORED
            mainContentContainer = new Panel
            {
                BackColor = backgroundColor,
                Dock = DockStyle.Fill,
                AutoScroll = true,
                Padding = new Padding(20)
            };

            // Add to main layout
            mainLayout.Controls.Add(sidebar, 0, 0);
            mainLayout.Controls.Add(mainContentContainer, 1, 0);

            // Handle form resize to update logout button position
            this.Resize += (s, e) =>
            {
                if (logoutBtn != null && sidebar != null)
                {
                    logoutBtn.Location = new Point(0, sidebar.ClientSize.Height - 80);
                }
            };

            this.Controls.Add(mainLayout);

            // Initially show dashboard
            CreateDashboardContent();
        }

        private void ShowTabContent(int tabIndex)
        {
            if (mainContentContainer == null) return;

            mainContentContainer.SuspendLayout();
            mainContentContainer.Controls.Clear();

            switch (tabIndex)
            {
                case 0: CreateDashboardContent(); break;
                case 1: CreateGlucoseTab(); break;
                case 2: CreateMedicationsTab(); break;
                case 3: CreateFoodTrackerTab(); break;
                case 4: CreateA1CTab(); break;
                case 5: CreateDoctorVisitsTab(); break;
                case 6: CreateSettingsTab(); break;
            }

            mainContentContainer.ResumeLayout();
        }

        private void CreateDashboardContent()
        {
            mainContentContainer.SuspendLayout();
            mainContentContainer.Controls.Clear();

            // ========== HEADER SECTION ==========
            Panel headerSection = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 100),
                Location = new Point(20, 20),
                BackColor = Color.Transparent
            };

            Label welcomeLabel = new Label
            {
                Text = $"👋 Welcome back, {currentUsername}!",
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label dateLabel = new Label
            {
                Text = DateTime.Now.ToString("dddd, MMMM dd, yyyy"),
                Font = new Font("Segoe UI", 12, FontStyle.Regular),
                ForeColor = mediumPurple,
                Location = new Point(0, 45),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            headerSection.Controls.Add(welcomeLabel);
            headerSection.Controls.Add(dateLabel);

            // ========== STATISTICS CARDS ==========
            Panel statsContainer = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 180),
                Location = new Point(20, 140),
                BackColor = Color.Transparent
            };

            // Load data
            try
            {
                // Today's glucose average
                string glucoseQuery = @"SELECT 
                              AVG(glucose_value) as avg_today,
                              COUNT(*) as count_today 
                              FROM glucose_readings 
                              WHERE user_id=@userId AND DATE(reading_time) = CURDATE()";
                DataTable glucoseResult = ExecuteQuery(glucoseQuery, new MySqlParameter("@userId", currentUserId));
                if (glucoseResult.Rows.Count > 0)
                {
                    if (glucoseResult.Rows[0]["avg_today"] != DBNull.Value)
                    {
                        double avgGlucose = Math.Round(Convert.ToDouble(glucoseResult.Rows[0]["avg_today"]), 0);
                        string glucoseValue = $"{avgGlucose}";
                        string glucoseSubtext = "mg/dL";

                        // Determine status color
                        Color statusColor = avgGlucose < 70 ? dangerColor :
                                          avgGlucose < 180 ? safeColor :
                                          avgGlucose < 250 ? warningColor : dangerColor;

                        // Create glucose card
                        Panel glucoseCard = CreateStatCard("🩸 Today's Glucose", glucoseValue, glucoseSubtext,
                            statusColor, new Point(0, 0));
                        statsContainer.Controls.Add(glucoseCard);
                    }
                    else
                    {
                        Panel glucoseCard = CreateStatCard("🩸 Today's Glucose", "No Data", "No readings today",
                            mediumPurple, new Point(0, 0));
                        statsContainer.Controls.Add(glucoseCard);
                    }
                }
                else
                {
                    Panel glucoseCard = CreateStatCard("🩸 Today's Glucose", "No Data", "No readings today",
                        mediumPurple, new Point(0, 0));
                    statsContainer.Controls.Add(glucoseCard);
                }

                // Active medications count
                string medsQuery = @"SELECT COUNT(*) as med_count FROM medications 
                           WHERE user_id=@userId AND is_active=TRUE";
                DataTable medsResult = ExecuteQuery(medsQuery, new MySqlParameter("@userId", currentUserId));
                int medCount = 0;
                if (medsResult.Rows.Count > 0 && medsResult.Rows[0][0] != DBNull.Value)
                    medCount = Convert.ToInt32(medsResult.Rows[0][0]);

                Panel medsCard = CreateStatCard("💊 Active Medications", medCount.ToString(), "Medications",
                    primaryColor, new Point(220, 0));
                statsContainer.Controls.Add(medsCard);

                // Average carbs (last 7 days)
                string carbsQuery = @"SELECT AVG(carbs) as avg_carbs FROM food_log 
                            WHERE user_id=@userId AND DATE(log_time) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)";
                DataTable carbsResult = ExecuteQuery(carbsQuery, new MySqlParameter("@userId", currentUserId));
                string carbsText = "No Data";
                if (carbsResult.Rows.Count > 0 && carbsResult.Rows[0][0] != DBNull.Value)
                {
                    double avgCarbs = Math.Round(Convert.ToDouble(carbsResult.Rows[0][0]), 0);
                    carbsText = $"{avgCarbs}g";
                }

                Panel carbsCard = CreateStatCard("🍎 Avg Carbs/Day", carbsText, "Last 7 days",
                    accentColor, new Point(440, 0));
                statsContainer.Controls.Add(carbsCard);

                // Next A1C goal
                string a1cQuery = @"SELECT a1c_value FROM a1c_records 
                          WHERE user_id=@userId ORDER BY test_date DESC LIMIT 1";
                DataTable a1cResult = ExecuteQuery(a1cQuery, new MySqlParameter("@userId", currentUserId));
                string a1cText = "< 7.0%";
                string a1cSubtext = "Goal";

                if (a1cResult.Rows.Count > 0 && a1cResult.Rows[0][0] != DBNull.Value)
                {
                    double currentA1c = Convert.ToDouble(a1cResult.Rows[0][0]);
                    a1cText = $"{currentA1c}%";
                    a1cSubtext = currentA1c < 7.0 ? "✓ On Track" : "⚠️ Needs Work";
                }

                Panel a1cCard = CreateStatCard("📈 A1C Status", a1cText, a1cSubtext,
                    safeColor, new Point(660, 0));
                statsContainer.Controls.Add(a1cCard);
            }
            catch (Exception ex)
            {
                // If there's an error, show placeholder cards
                statsContainer.Controls.Add(CreateStatCard("🩸 Today's Glucose", "--", "Error loading",
                    mediumPurple, new Point(0, 0)));
                statsContainer.Controls.Add(CreateStatCard("💊 Active Medications", "--", "Error loading",
                    mediumPurple, new Point(220, 0)));
                statsContainer.Controls.Add(CreateStatCard("🍎 Avg Carbs/Day", "--", "Error loading",
                    mediumPurple, new Point(440, 0)));
                statsContainer.Controls.Add(CreateStatCard("📈 A1C Status", "--", "Error loading",
                    mediumPurple, new Point(660, 0)));
            }

            // ========== QUICK ACTIONS ==========
            Panel quickActionsPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 150),
                Location = new Point(20, 340),
                BackColor = Color.Transparent
            };

            Label quickActionsTitle = new Label
            {
                Text = "⚡ Quick Actions",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Panel actionsGrid = new Panel
            {
                Size = new Size(quickActionsPanel.Width, 100),
                Location = new Point(0, 45),
                BackColor = Color.Transparent
            };

            // Define action buttons with icons and labels
            var quickActions = new[]
            {
        new { Icon = "🩸", Text = "Log Glucose", Color = accentColor, Tag = 1 },
        new { Icon = "💊", Text = "Add Medication", Color = primaryColor, Tag = 2 },
        new { Icon = "🍎", Text = "Log Food", Color = safeColor, Tag = 3 },
        new { Icon = "📅", Text = "Add Visit", Color = infoColor, Tag = 5 }
    };

            int actionButtonWidth = (actionsGrid.Width - 50) / 4;

            for (int i = 0; i < 4; i++)
            {
                var action = quickActions[i];

                // Create main action button container
                Panel actionButtonContainer = new Panel
                {
                    Size = new Size(actionButtonWidth, 90),
                    Location = new Point(i * (actionButtonWidth + 15), 0),
                    BackColor = Color.Transparent
                };

                // Create the actual button with icon
                Button actionBtn = new Button
                {
                    Text = action.Icon,
                    Font = new Font("Segoe UI", 24, FontStyle.Bold),
                    ForeColor = Color.White,
                    BackColor = action.Color,
                    Size = new Size(70, 70),
                    Location = new Point((actionButtonWidth - 70) / 2, 0),
                    FlatStyle = FlatStyle.Flat,
                    TextAlign = ContentAlignment.MiddleCenter,
                    Cursor = Cursors.Hand,
                    Tag = action.Tag
                };
                actionBtn.FlatAppearance.BorderSize = 0;
                actionBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(
                    Math.Min(action.Color.R + 30, 255),
                    Math.Min(action.Color.G + 30, 255),
                    Math.Min(action.Color.B + 30, 255)
                );

                // Add rounded corners to button
                actionBtn.Paint += (sender, e) =>
                {
                    Button btn = (Button)sender;
                    e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                    Rectangle rect = new Rectangle(0, 0, btn.Width - 1, btn.Height - 1);
                    int radius = 35; // Fully rounded for circle effect

                    using (GraphicsPath path = new GraphicsPath())
                    {
                        path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                        path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                        path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                        path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                        path.CloseFigure();

                        e.Graphics.FillPath(new SolidBrush(btn.BackColor), path);
                    }
                };

                // Add label below the button
                Label actionLabel = new Label
                {
                    Text = action.Text,
                    Font = new Font("Segoe UI", 10, FontStyle.Bold),
                    ForeColor = darkColor,
                    Size = new Size(actionButtonWidth, 20),
                    Location = new Point(0, 72),
                    TextAlign = ContentAlignment.TopCenter,
                    BackColor = Color.Transparent
                };

                actionBtn.Click += (s, e) =>
                {
                    if (s is Button btn && btn.Tag is int index)
                    {
                        ShowTabContent(index);
                    }
                };

                actionButtonContainer.Controls.Add(actionBtn);
                actionButtonContainer.Controls.Add(actionLabel);
                actionsGrid.Controls.Add(actionButtonContainer);
            }

            quickActionsPanel.Controls.Add(quickActionsTitle);
            quickActionsPanel.Controls.Add(actionsGrid);

            // ========== RECENT GLUCOSE READINGS ==========
            Panel recentReadingsPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 350),
                Location = new Point(20, 510),
                BackColor = Color.White,
                Padding = new Padding(25)
            };

            // Add rounded corners
            recentReadingsPanel.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                Rectangle rect = new Rectangle(0, 0, recentReadingsPanel.Width - 1, recentReadingsPanel.Height - 1);
                int radius = 15;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(Color.White), path);
                    e.Graphics.DrawPath(new Pen(Color.FromArgb(230, 230, 230), 1), path);
                }
            };

            Label recentTitle = new Label
            {
                Text = "📊 Recent Glucose Readings",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 15),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Create refresh button
            Button refreshReadingsBtn = new Button
            {
                Text = "🔄 Refresh",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = primaryColor,
                BackColor = Color.Transparent,
                Size = new Size(100, 35),
                Location = new Point(recentReadingsPanel.Width - 120, 10),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            refreshReadingsBtn.FlatAppearance.BorderSize = 0;
            refreshReadingsBtn.FlatAppearance.MouseOverBackColor = lightPurple;

            refreshReadingsBtn.Click += (s, e) =>
            {
                ShowTabContent(0); // Refresh dashboard
            };

            // Create modern DataGridView
            DataGridView glucoseGrid = new DataGridView
            {
                Location = new Point(0, 70),
                Size = new Size(recentReadingsPanel.Width - 50, 240),
                BackgroundColor = Color.White,
                RowHeadersVisible = false,
                ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None,
                AllowUserToAddRows = false,
                AllowUserToResizeRows = false,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                GridColor = Color.FromArgb(240, 240, 240),
                DefaultCellStyle = new DataGridViewCellStyle
                {
                    Padding = new Padding(8),
                    SelectionBackColor = lightPurple,
                    SelectionForeColor = Color.Black
                },
                RowTemplate = { Height = 40 }
            };

            // Add columns with custom styling
            glucoseGrid.Columns.Add("Time", "Time");
            glucoseGrid.Columns.Add("Value", "Glucose (mg/dL)");
            glucoseGrid.Columns.Add("Type", "Reading Type");
            glucoseGrid.Columns.Add("Status", "Status");

            // Style columns
            foreach (DataGridViewColumn column in glucoseGrid.Columns)
            {
                column.HeaderCell.Style.Font = new Font("Segoe UI", 11, FontStyle.Bold);
                column.HeaderCell.Style.BackColor = backgroundColor;
                column.HeaderCell.Style.ForeColor = primaryColor;
                column.HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }

            // Set specific column widths
            glucoseGrid.Columns["Time"].Width = 120;
            glucoseGrid.Columns["Value"].Width = 120;
            glucoseGrid.Columns["Type"].Width = 120;
            glucoseGrid.Columns["Status"].Width = 100;

            // Color code status column
            glucoseGrid.CellFormatting += (sender, e) =>
            {
                if (e.ColumnIndex == glucoseGrid.Columns["Status"].Index && e.Value != null)
                {
                    string status = e.Value.ToString();
                    switch (status)
                    {
                        case "Normal":
                            e.CellStyle.ForeColor = safeColor;
                            break;
                        case "Low":
                            e.CellStyle.ForeColor = infoColor;
                            break;
                        case "High":
                            e.CellStyle.ForeColor = warningColor;
                            break;
                        case "Critical":
                            e.CellStyle.ForeColor = dangerColor;
                            break;
                        default:
                            e.CellStyle.ForeColor = Color.Black;
                            break;
                    }
                    e.CellStyle.Font = new Font(glucoseGrid.Font, FontStyle.Bold);
                }

                if (e.ColumnIndex == glucoseGrid.Columns["Value"].Index && e.Value != null)
                {
                    e.CellStyle.Font = new Font(glucoseGrid.Font, FontStyle.Bold);
                    e.CellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                }
            };

            // Alternating row colors
            glucoseGrid.AlternatingRowsDefaultCellStyle.BackColor = Color.FromArgb(250, 250, 250);

            // Load data
            LoadRecentGlucose(glucoseGrid);

            recentReadingsPanel.Controls.Add(recentTitle);
            recentReadingsPanel.Controls.Add(refreshReadingsBtn);
            recentReadingsPanel.Controls.Add(glucoseGrid);

            // ========== ADD ALL CONTROLS ==========
            mainContentContainer.Controls.Add(headerSection);
            mainContentContainer.Controls.Add(statsContainer);
            mainContentContainer.Controls.Add(quickActionsPanel);
            mainContentContainer.Controls.Add(recentReadingsPanel);

            // ========== HANDLE RESIZE ==========
            mainContentContainer.Resize += (s, e) =>
            {
                int containerWidth = mainContentContainer.ClientSize.Width - 40;

                // Update header section
                headerSection.Size = new Size(containerWidth, 100);

                // Update stats container
                statsContainer.Size = new Size(containerWidth, 180);
                statsContainer.Location = new Point(20, 140);

                // Update quick actions
                quickActionsPanel.Size = new Size(containerWidth, 150);
                quickActionsPanel.Location = new Point(20, 340);

                // Update recent readings panel
                recentReadingsPanel.Size = new Size(containerWidth, 350);
                recentReadingsPanel.Location = new Point(20, 510);

                // Update grid size
                glucoseGrid.Size = new Size(recentReadingsPanel.Width - 50, 240);

                // Update refresh button position
                refreshReadingsBtn.Location = new Point(recentReadingsPanel.Width - 120, 10);

                // Update quick action buttons
                int newActionButtonWidth = (containerWidth - 50) / 4;
                for (int i = 0; i < actionsGrid.Controls.Count; i++)
                {
                    if (actionsGrid.Controls[i] is Panel actionContainer)
                    {
                        actionContainer.Size = new Size(newActionButtonWidth, 90);
                        actionContainer.Location = new Point(i * (newActionButtonWidth + 15), 0);

                        // Center the button within the container
                        if (actionContainer.Controls.Count > 0 && actionContainer.Controls[0] is Button btn)
                        {
                            btn.Location = new Point((newActionButtonWidth - 70) / 2, 0);
                        }

                        // Update label width
                        if (actionContainer.Controls.Count > 1 && actionContainer.Controls[1] is Label lbl)
                        {
                            lbl.Size = new Size(newActionButtonWidth, 20);
                        }
                    }
                }
            };

            mainContentContainer.ResumeLayout();
        }

        // Helper method to create beautiful stat cards
        private Panel CreateStatCard(string title, string value, string subtext, Color cardColor, Point location)
        {
            Panel card = new Panel
            {
                Size = new Size(200, 170),
                Location = location,
                BackColor = cardColor,
                Padding = new Padding(20)
            };

            // Add rounded corners
            card.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                Rectangle rect = new Rectangle(0, 0, card.Width - 1, card.Height - 1);
                int radius = 15;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(cardColor), path);
                }
            };

            // Title
            Label titleLabel = new Label
            {
                Text = title,
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(0, 15),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Value
            Label valueLabel = new Label
            {
                Text = value,
                Font = new Font("Segoe UI", 32, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(0, 45),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Subtext
            Label subtextLabel = new Label
            {
                Text = subtext,
                Font = new Font("Segoe UI", 10, FontStyle.Regular),
                ForeColor = Color.FromArgb(240, 240, 240),
                Location = new Point(0, 105),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            card.Controls.Add(titleLabel);
            card.Controls.Add(valueLabel);
            card.Controls.Add(subtextLabel);

            return card;
        }

        private void LoadRecentGlucose(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT reading_time, glucose_value, reading_type, status 
                               FROM glucose_readings WHERE user_id=@userId 
                               ORDER BY reading_time DESC LIMIT 8";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    grid.Rows.Add(
                        Convert.ToDateTime(row["reading_time"]).ToString("MM/dd HH:mm"),
                        row["glucose_value"],
                        row["reading_type"],
                        row["status"]
                    );
                }
            }
            catch { }
        }

        private void CreateGlucoseTab()
        {
            mainContentContainer.SuspendLayout();
            mainContentContainer.Controls.Clear();

            // ========== HEADER ==========
            Label header = new Label
            {
                Text = "🩸 Blood Glucose Tracker",
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(20, 20),
                BackColor = Color.Transparent
            };

            // ========== TODAY'S SUMMARY CARD ==========
            Panel summaryCard = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 120),
                Location = new Point(20, 70),
                BackColor = Color.White,
                Padding = new Padding(25)
            };

            // Add rounded corners and shadow
            summaryCard.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                Rectangle rect = new Rectangle(0, 0, summaryCard.Width - 1, summaryCard.Height - 1);
                int radius = 12;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(Color.White), path);
                    e.Graphics.DrawPath(new Pen(Color.FromArgb(230, 230, 230), 1), path);
                }
            };

            // Load today's average glucose
            double todaysAvg = 0;
            int todaysReadings = 0;
            try
            {
                string query = @"SELECT 
                        AVG(glucose_value) as avg_glucose,
                        COUNT(*) as reading_count 
                        FROM glucose_readings 
                        WHERE user_id=@userId AND DATE(reading_time) = CURDATE()";
                DataTable result = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));
                if (result.Rows.Count > 0)
                {
                    if (result.Rows[0]["avg_glucose"] != DBNull.Value)
                        todaysAvg = Math.Round(Convert.ToDouble(result.Rows[0]["avg_glucose"]), 1);
                    todaysReadings = Convert.ToInt32(result.Rows[0]["reading_count"]);
                }
            }
            catch { }

            Label summaryTitle = new Label
            {
                Text = "📊 Today's Summary",
                Font = new Font("Segoe UI", 16, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 10),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label avgGlucoseLabel = new Label
            {
                Text = $"Average Glucose: {todaysAvg} mg/dL",
                Font = new Font("Segoe UI", 14, FontStyle.Regular),
                ForeColor = darkColor,
                Location = new Point(0, 45),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label readingCountLabel = new Label
            {
                Text = $"Readings Today: {todaysReadings}",
                Font = new Font("Segoe UI", 12, FontStyle.Regular),
                ForeColor = mediumPurple,
                Location = new Point(0, 75),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            summaryCard.Controls.Add(summaryTitle);
            summaryCard.Controls.Add(avgGlucoseLabel);
            summaryCard.Controls.Add(readingCountLabel);

            // ========== ADD READING CARD ==========
            Panel addReadingCard = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 280),
                Location = new Point(20, 210),
                BackColor = Color.White,
                Padding = new Padding(25)
            };

            // Add rounded corners
            addReadingCard.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                Rectangle rect = new Rectangle(0, 0, addReadingCard.Width - 1, addReadingCard.Height - 1);
                int radius = 12;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(Color.White), path);
                    e.Graphics.DrawPath(new Pen(Color.FromArgb(230, 230, 230), 1), path);
                }
            };

            Label addReadingTitle = new Label
            {
                Text = "➕ Add New Reading",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 10),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Form layout using TableLayoutPanel
            TableLayoutPanel formLayout = new TableLayoutPanel
            {
                Location = new Point(0, 60),
                Size = new Size(addReadingCard.Width - 50, 150),
                ColumnCount = 2,
                RowCount = 3,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 10, 0, 10)
            };
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 35));
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 65));

            // Glucose Value
            Label glucoseLabel = new Label
            {
                Text = "Glucose Value:",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 15, 0)
            };

            Panel glucoseInputPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(5)
            };

            TextBox glucoseTextBox = new TextBox
            {
                Font = new Font("Segoe UI", 12),
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Dock = DockStyle.Fill
            };

            // Manual placeholder implementation (since PlaceholderText doesn't exist in older .NET)
            glucoseTextBox.Enter += (s, e) =>
            {
                if (glucoseTextBox.Text == "Enter value in mg/dL")
                {
                    glucoseTextBox.Text = "";
                    glucoseTextBox.ForeColor = Color.Black;
                }
            };

            glucoseTextBox.Leave += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(glucoseTextBox.Text))
                {
                    glucoseTextBox.Text = "Enter value in mg/dL";
                    glucoseTextBox.ForeColor = Color.Gray;
                }
            };

            if (string.IsNullOrWhiteSpace(glucoseTextBox.Text))
            {
                glucoseTextBox.Text = "Enter value in mg/dL";
                glucoseTextBox.ForeColor = Color.Gray;
            }

            glucoseInputPanel.Controls.Add(glucoseTextBox);

            // Reading Type
            Label readingTypeLabel = new Label
            {
                Text = "Reading Type:",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 15, 0)
            };

            Panel typeInputPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(5)
            };

            ComboBox readingTypeCombo = new ComboBox
            {
                Font = new Font("Segoe UI", 12),
                BackColor = Color.White,
                Dock = DockStyle.Fill,
                DropDownStyle = ComboBoxStyle.DropDownList,
                FlatStyle = FlatStyle.Flat
            };
            readingTypeCombo.Items.AddRange(new string[] { "Fasting", "Before Meal", "After Meal", "Bedtime", "Random" });
            readingTypeCombo.SelectedIndex = 0;

            typeInputPanel.Controls.Add(readingTypeCombo);

            // Add to form layout
            formLayout.Controls.Add(glucoseLabel, 0, 0);
            formLayout.Controls.Add(glucoseInputPanel, 1, 0);
            formLayout.Controls.Add(readingTypeLabel, 0, 1);
            formLayout.Controls.Add(typeInputPanel, 1, 1);

            // Add Reading Button
            Button addReadingBtn = new Button
            {
                Text = "📝 Add Reading",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(200, 45),
                Location = new Point((addReadingCard.Width - 200) / 2, 220),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            addReadingBtn.FlatAppearance.BorderSize = 0;
            addReadingBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 85, 140);

            // Add rounded corners to button
            addReadingBtn.Paint += (sender, e) =>
            {
                Button btn = (Button)sender;
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

                Rectangle rect = new Rectangle(0, 0, btn.Width - 1, btn.Height - 1);
                int radius = 22;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(btn.BackColor), path);

                    StringFormat sf = new StringFormat();
                    sf.Alignment = StringAlignment.Center;
                    sf.LineAlignment = StringAlignment.Center;
                    e.Graphics.DrawString(btn.Text, btn.Font, new SolidBrush(btn.ForeColor), rect, sf);
                }
            };

            addReadingBtn.Click += (s, e) =>
            {
                string glucoseText = glucoseTextBox.Text;
                if (glucoseText == "Enter value in mg/dL")
                    glucoseText = "";

                if (double.TryParse(glucoseText, out double glucose))
                {
                    string status = GetGlucoseStatus(glucose, readingTypeCombo.Text);
                    AddGlucoseReading(glucose, readingTypeCombo.Text, "", "", status);

                    string message = $"Glucose reading added: {glucose} mg/dL\nReading Type: {readingTypeCombo.Text}\nStatus: {status}";
                    string title = status == "Critical" ? "⚠️ Critical Reading!" : "✓ Reading Added";
                    MessageBoxIcon icon = status == "Critical" ? MessageBoxIcon.Warning : MessageBoxIcon.Information;

                    MessageBox.Show(message, title, MessageBoxButtons.OK, icon);

                    glucoseTextBox.Text = "Enter value in mg/dL";
                    glucoseTextBox.ForeColor = Color.Gray;
                    glucoseTextBox.Focus();

                    // Refresh the tab to show updated data
                    ShowTabContent(1); // 1 is the glucose tab index
                }
                else
                {
                    MessageBox.Show("Please enter a valid glucose value (e.g., 120.5)!",
                        "❌ Invalid Input",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
            };

            addReadingCard.Controls.Add(addReadingTitle);
            addReadingCard.Controls.Add(formLayout);
            addReadingCard.Controls.Add(addReadingBtn);

            // ========== GLUCOSE HISTORY CARD ==========
            Panel historyCard = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 380),
                Location = new Point(20, 510),
                BackColor = Color.White,
                Padding = new Padding(25)
            };

            // Add rounded corners
            historyCard.Paint += (sender, e) =>
            {
                e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
                Rectangle rect = new Rectangle(0, 0, historyCard.Width - 1, historyCard.Height - 1);
                int radius = 12;

                using (GraphicsPath path = new GraphicsPath())
                {
                    path.AddArc(rect.X, rect.Y, radius, radius, 180, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y, radius, radius, 270, 90);
                    path.AddArc(rect.X + rect.Width - radius, rect.Y + rect.Height - radius, radius, radius, 0, 90);
                    path.AddArc(rect.X, rect.Y + rect.Height - radius, radius, radius, 90, 90);
                    path.CloseFigure();

                    e.Graphics.FillPath(new SolidBrush(Color.White), path);
                    e.Graphics.DrawPath(new Pen(Color.FromArgb(230, 230, 230), 1), path);
                }
            };

            Label historyTitle = new Label
            {
                Text = "📋 Recent Glucose Readings",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 10),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Create a modern styled DataGridView
            DataGridView historyGrid = new DataGridView
            {
                Location = new Point(0, 60),
                Size = new Size(historyCard.Width - 50, 280),
                BackgroundColor = Color.White,
                RowHeadersVisible = false,
                ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None,
                AllowUserToAddRows = false,
                AllowUserToResizeRows = false,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                GridColor = Color.FromArgb(240, 240, 240),
                DefaultCellStyle = new DataGridViewCellStyle
                {
                    Padding = new Padding(5),
                    SelectionBackColor = lightPurple,
                    SelectionForeColor = Color.Black
                },
                RowTemplate = { Height = 35 }
            };

            // Customize columns
            historyGrid.Columns.Add("Date", "Date & Time");
            historyGrid.Columns.Add("Value", "Glucose (mg/dL)");
            historyGrid.Columns.Add("Type", "Type");
            historyGrid.Columns.Add("Status", "Status");

            // Style the columns
            foreach (DataGridViewColumn column in historyGrid.Columns)
            {
                column.HeaderCell.Style.Font = new Font("Segoe UI", 11, FontStyle.Bold);
                column.HeaderCell.Style.BackColor = backgroundColor;
                column.HeaderCell.Style.ForeColor = primaryColor;
                column.HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }

            // Set column widths
            historyGrid.Columns["Date"].Width = 150;
            historyGrid.Columns["Value"].Width = 120;
            historyGrid.Columns["Type"].Width = 120;
            historyGrid.Columns["Status"].Width = 100;

            // Add cell formatting for status colors (using traditional switch statement instead of switch expression)
            historyGrid.CellFormatting += (sender, e) =>
            {
                if (e.ColumnIndex == historyGrid.Columns["Status"].Index && e.Value != null)
                {
                    string status = e.Value.ToString();

                    // Traditional switch statement (compatible with C# 7.3)
                    switch (status)
                    {
                        case "Normal":
                            e.CellStyle.ForeColor = safeColor;
                            break;
                        case "Low":
                            e.CellStyle.ForeColor = infoColor;
                            break;
                        case "High":
                            e.CellStyle.ForeColor = warningColor;
                            break;
                        case "Critical":
                            e.CellStyle.ForeColor = dangerColor;
                            break;
                        default:
                            e.CellStyle.ForeColor = Color.Black;
                            break;
                    }

                    e.CellStyle.Font = new Font(historyGrid.Font, FontStyle.Bold);
                }

                if (e.ColumnIndex == historyGrid.Columns["Value"].Index && e.Value != null)
                {
                    e.CellStyle.Font = new Font(historyGrid.Font, FontStyle.Bold);
                    e.CellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                }
            };

            // Style alternating rows
            historyGrid.AlternatingRowsDefaultCellStyle.BackColor = Color.FromArgb(248, 248, 248);

            // Add refresh button
            Button refreshBtn = new Button
            {
                Text = "🔄 Refresh",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = primaryColor,
                BackColor = Color.Transparent,
                Size = new Size(100, 35),
                Location = new Point(historyCard.Width - 120, 15),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            refreshBtn.FlatAppearance.BorderSize = 0;
            refreshBtn.FlatAppearance.MouseOverBackColor = lightPurple;
            refreshBtn.Click += (s, e) => LoadGlucoseHistory(historyGrid);

            historyCard.Controls.Add(historyTitle);
            historyCard.Controls.Add(refreshBtn);
            historyCard.Controls.Add(historyGrid);

            // Load initial data
            LoadGlucoseHistory(historyGrid);

            // Add all controls to main container
            mainContentContainer.Controls.Add(header);
            mainContentContainer.Controls.Add(summaryCard);
            mainContentContainer.Controls.Add(addReadingCard);
            mainContentContainer.Controls.Add(historyCard);

            // ========== HANDLE RESIZE ==========
            mainContentContainer.Resize += (s, e) =>
            {
                int containerWidth = mainContentContainer.ClientSize.Width - 40;

                // Update all card widths
                summaryCard.Size = new Size(containerWidth, 120);
                addReadingCard.Size = new Size(containerWidth, 280);
                historyCard.Size = new Size(containerWidth, 380);

                // Update positions
                addReadingCard.Location = new Point(20, 210);
                historyCard.Location = new Point(20, 510);

                // Update form layout size
                formLayout.Size = new Size(addReadingCard.Width - 50, 150);

                // Center the add button
                addReadingBtn.Location = new Point((addReadingCard.Width - 200) / 2, 220);

                // Update grid size
                historyGrid.Size = new Size(historyCard.Width - 50, 280);

                // Update refresh button position
                refreshBtn.Location = new Point(historyCard.Width - 120, 15);
            };

            mainContentContainer.ResumeLayout();
        }

        private string GetGlucoseStatus(double glucose, string readingType)
        {
            if (glucose < 70) return "Low";
            if (glucose < 180) return "Normal";
            if (glucose < 250) return "High";
            return "Critical";
        }

        private void AddGlucoseReading(double glucose, string readingType, string mealContext, string notes, string status)
        {
            ExecuteNonQuery(
                @"INSERT INTO glucose_readings (user_id, glucose_value, reading_type, meal_context, notes, status) 
                VALUES (@userId, @glucose, @type, @meal, @notes, @status)",
                new MySqlParameter("@userId", currentUserId),
                new MySqlParameter("@glucose", glucose),
                new MySqlParameter("@type", readingType),
                new MySqlParameter("@meal", string.IsNullOrEmpty(mealContext) ? DBNull.Value : (object)mealContext),
                new MySqlParameter("@notes", string.IsNullOrEmpty(notes) ? DBNull.Value : (object)notes),
                new MySqlParameter("@status", status)
            );
        }

        private void LoadGlucoseHistory(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT reading_time, glucose_value, reading_type, status 
                               FROM glucose_readings WHERE user_id=@userId 
                               AND reading_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                               ORDER BY reading_time DESC LIMIT 15";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    grid.Rows.Add(
                        Convert.ToDateTime(row["reading_time"]).ToString("MM/dd HH:mm"),
                        row["glucose_value"],
                        row["reading_type"],
                        row["status"]
                    );
                }
            }
            catch { }
        }

        private void CreateMedicationsTab()
        {
            mainContentContainer.SuspendLayout();

            Label header = new Label
            {
                Text = "💊 Medication Manager",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };

            // Today's Schedule
            Panel schedulePanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 250),
                Location = new Point(0, 50),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(20)
            };

            Label scheduleTitle = new Label
            {
                Text = "📅 Today's Medication Schedule",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            DataGridView scheduleGrid = new DataGridView
            {
                Location = new Point(0, 40),
                Size = new Size(schedulePanel.Width - 40, 170),
                BackgroundColor = Color.White,
                RowHeadersVisible = false,
                ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None,
                AllowUserToAddRows = false
            };

            scheduleGrid.Columns.Add("Time", "Time");
            scheduleGrid.Columns.Add("Medication", "Medication");
            scheduleGrid.Columns.Add("Dosage", "Dosage");
            scheduleGrid.Columns.Add("Status", "Status");

            LoadTodaysSchedule(scheduleGrid);

            // Add Medication Button
            Button addMedBtn = new Button
            {
                Text = "➕ Add New Medication",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(220, 40),
                Location = new Point(20, 320),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            addMedBtn.FlatAppearance.BorderSize = 0;
            addMedBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 100, 150);
            addMedBtn.Click += (s, e) => ShowAddMedicationForm();

            // Active Medications List
            Panel activeMedsPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 300),
                Location = new Point(0, 380),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(20)
            };

            Label activeMedsTitle = new Label
            {
                Text = "💊 Active Medications",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            ListBox medsListBox = new ListBox
            {
                Location = new Point(0, 40),
                Size = new Size(activeMedsPanel.Width - 40, 230),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            LoadActiveMedications(medsListBox);

            // Add controls
            schedulePanel.Controls.Add(scheduleTitle);
            schedulePanel.Controls.Add(scheduleGrid);
            activeMedsPanel.Controls.Add(activeMedsTitle);
            activeMedsPanel.Controls.Add(medsListBox);

            mainContentContainer.Controls.Add(header);
            mainContentContainer.Controls.Add(schedulePanel);
            mainContentContainer.Controls.Add(addMedBtn);
            mainContentContainer.Controls.Add(activeMedsPanel);

            // Handle resize
            mainContentContainer.Resize += (s, e) =>
            {
                schedulePanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 250);
                scheduleGrid.Size = new Size(schedulePanel.Width - 40, 170);
                addMedBtn.Location = new Point(20, 320);
                activeMedsPanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 300);
                activeMedsPanel.Location = new Point(0, 380);
                medsListBox.Size = new Size(activeMedsPanel.Width - 40, 230);
            };

            mainContentContainer.ResumeLayout();
        }

        private void LoadTodaysSchedule(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT name, dosage, schedule_time FROM medications 
                               WHERE user_id=@userId AND is_active=TRUE 
                               ORDER BY schedule_time";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    string time = "As needed";
                    if (row["schedule_time"] != DBNull.Value)
                        time = DateTime.Parse(row["schedule_time"].ToString()).ToString("hh:mm tt");

                    string dosage = "";
                    if (row["dosage"] != DBNull.Value)
                        dosage = row["dosage"].ToString();

                    grid.Rows.Add(time, row["name"].ToString(), dosage, "Due");
                }
            }
            catch { }
        }

        private void LoadActiveMedications(ListBox listBox)
        {
            listBox.Items.Clear();
            try
            {
                string query = @"SELECT name, dosage, schedule_time FROM medications 
                               WHERE user_id=@userId AND is_active=TRUE 
                               ORDER BY name";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    string med = row["name"].ToString();
                    string dosage = row["dosage"] != DBNull.Value ? row["dosage"].ToString() : "";
                    string time = row["schedule_time"] != DBNull.Value ?
                        DateTime.Parse(row["schedule_time"].ToString()).ToString("hh:mm tt") : "As needed";

                    listBox.Items.Add($"{med} - {dosage} at {time}");
                }
            }
            catch { }
        }

        private void ShowAddMedicationForm()
        {
            Form medForm = new Form
            {
                Text = "Add New Medication",
                Size = new Size(500, 350),
                StartPosition = FormStartPosition.CenterParent,
                BackColor = backgroundColor,
                Font = new Font("Segoe UI", 9)
            };

            Panel contentPanel = new Panel
            {
                Dock = DockStyle.Fill,
                Padding = new Padding(30)
            };

            TableLayoutPanel formLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 4,
                BackColor = Color.Transparent
            };
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40));
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60));

            // Medication Name
            Label nameLabel = new Label
            {
                Text = "Medication Name:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            TextBox nameTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Margin = new Padding(0, 5, 0, 5)
            };

            // Dosage
            Label dosageLabel = new Label
            {
                Text = "Dosage:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            TextBox dosageTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Margin = new Padding(0, 5, 0, 5)
            };

            // Schedule Time
            Label timeLabel = new Label
            {
                Text = "Schedule Time:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            DateTimePicker timePicker = new DateTimePicker
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Format = DateTimePickerFormat.Time,
                ShowUpDown = true,
                Margin = new Padding(0, 5, 0, 5)
            };

            // Buttons panel
            Panel buttonPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 60,
                BackColor = Color.Transparent
            };

            Button saveBtn = new Button
            {
                Text = "💾 Save Medication",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(180, 40),
                Location = new Point(80, 10),
                FlatStyle = FlatStyle.Flat
            };
            saveBtn.FlatAppearance.BorderSize = 0;

            Button cancelBtn = new Button
            {
                Text = "Cancel",
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.White,
                BackColor = mediumPurple,
                Size = new Size(100, 35),
                Location = new Point(280, 12),
                FlatStyle = FlatStyle.Flat
            };
            cancelBtn.FlatAppearance.BorderSize = 0;

            // Events
            saveBtn.Click += (s, e) =>
            {
                if (!string.IsNullOrWhiteSpace(nameTextBox.Text))
                {
                    ExecuteNonQuery(
                        @"INSERT INTO medications (user_id, name, dosage, schedule_time, medication_type, is_active) 
                        VALUES (@userId, @name, @dosage, @time, 'Other', TRUE)",
                        new MySqlParameter("@userId", currentUserId),
                        new MySqlParameter("@name", nameTextBox.Text),
                        new MySqlParameter("@dosage", dosageTextBox.Text),
                        new MySqlParameter("@time", timePicker.Value.TimeOfDay)
                    );

                    MessageBox.Show("Medication added successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    medForm.Close();
                    ShowTabContent(2); // Refresh medications tab
                }
            };

            cancelBtn.Click += (s, e) => medForm.Close();

            // Add to layouts
            formLayout.Controls.Add(nameLabel, 0, 0);
            formLayout.Controls.Add(nameTextBox, 1, 0);
            formLayout.Controls.Add(dosageLabel, 0, 1);
            formLayout.Controls.Add(dosageTextBox, 1, 1);
            formLayout.Controls.Add(timeLabel, 0, 2);
            formLayout.Controls.Add(timePicker, 1, 2);

            buttonPanel.Controls.Add(saveBtn);
            buttonPanel.Controls.Add(cancelBtn);

            contentPanel.Controls.Add(formLayout);
            contentPanel.Controls.Add(buttonPanel);

            medForm.Controls.Add(contentPanel);
            medForm.ShowDialog();
        }

        private void CreateFoodTrackerTab()
        {
            mainContentContainer.SuspendLayout();

            Label header = new Label
            {
                Text = "🍎 Food & Carb Tracker",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };

            // Today's Summary Panel
            Panel summaryPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 120),
                Location = new Point(0, 50),
                BackColor = accentColor,
                Padding = new Padding(20)
            };

            // Load today's carbs
            double todaysCarbs = 0;
            try
            {
                string query = @"SELECT SUM(carbs) as total_carbs FROM food_log 
                               WHERE user_id=@userId AND DATE(log_time) = CURDATE()";
                DataTable result = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));
                if (result.Rows.Count > 0 && result.Rows[0][0] != DBNull.Value)
                    todaysCarbs = Convert.ToDouble(result.Rows[0][0]);
            }
            catch { }

            Label carbsLabel = new Label
            {
                Text = $"Today's Carbs: {todaysCarbs}g",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(20, 20),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label goalLabel = new Label
            {
                Text = "Daily Goal: < 200g",
                Font = new Font("Segoe UI", 12),
                ForeColor = Color.White,
                Location = new Point(20, 60),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Progress bar
            int progressWidth = (int)Math.Min(300, (todaysCarbs / 200) * 300);
            Panel progressBar = new Panel
            {
                Size = new Size(progressWidth, 20),
                Location = new Point(summaryPanel.Width - 320, 50),
                BackColor = safeColor
            };

            Panel progressBack = new Panel
            {
                Size = new Size(300, 20),
                Location = new Point(summaryPanel.Width - 320, 50),
                BackColor = Color.FromArgb(200, 200, 200),
                BorderStyle = BorderStyle.FixedSingle
            };

            // Add Food Button
            Button addFoodBtn = new Button
            {
                Text = "➕ Add Food Entry",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = primaryColor,
                Size = new Size(220, 40),
                Location = new Point(20, 190),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            addFoodBtn.FlatAppearance.BorderSize = 0;
            addFoodBtn.FlatAppearance.MouseOverBackColor = secondaryColor;
            addFoodBtn.Click += (s, e) => ShowAddFoodForm();

            // Recent Food Log
            Panel foodLogPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 300),
                Location = new Point(0, 250),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(20)
            };

            Label logTitle = new Label
            {
                Text = "📝 Today's Food Log",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            DataGridView foodGrid = new DataGridView
            {
                Location = new Point(0, 40),
                Size = new Size(foodLogPanel.Width - 40, 230),
                BackgroundColor = Color.White,
                RowHeadersVisible = false,
                ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None,
                AllowUserToAddRows = false
            };

            foodGrid.Columns.Add("Time", "Time");
            foodGrid.Columns.Add("Food", "Food Item");
            foodGrid.Columns.Add("Carbs", "Carbs (g)");
            foodGrid.Columns.Add("Meal", "Meal Type");

            LoadTodaysFoodLog(foodGrid);

            // Add controls
            progressBack.Controls.Add(progressBar);
            summaryPanel.Controls.Add(carbsLabel);
            summaryPanel.Controls.Add(goalLabel);
            summaryPanel.Controls.Add(progressBack);
            foodLogPanel.Controls.Add(logTitle);
            foodLogPanel.Controls.Add(foodGrid);

            mainContentContainer.Controls.Add(header);
            mainContentContainer.Controls.Add(summaryPanel);
            mainContentContainer.Controls.Add(addFoodBtn);
            mainContentContainer.Controls.Add(foodLogPanel);

            // Handle resize
            mainContentContainer.Resize += (s, e) =>
            {
                summaryPanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 120);
                progressBack.Location = new Point(summaryPanel.Width - 320, 50);
                addFoodBtn.Location = new Point(20, 190);
                foodLogPanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 300);
                foodLogPanel.Location = new Point(0, 250);
                foodGrid.Size = new Size(foodLogPanel.Width - 40, 230);
            };

            mainContentContainer.ResumeLayout();
        }

        private void LoadTodaysFoodLog(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT log_time, food_item, carbs, meal_type FROM food_log 
                               WHERE user_id=@userId AND DATE(log_time) = CURDATE()
                               ORDER BY log_time DESC LIMIT 10";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    grid.Rows.Add(
                        Convert.ToDateTime(row["log_time"]).ToString("HH:mm"),
                        row["food_item"],
                        row["carbs"],
                        row["meal_type"]
                    );
                }
            }
            catch { }
        }

        private void ShowAddFoodForm()
        {
            Form foodForm = new Form
            {
                Text = "Add Food Entry",
                Size = new Size(500, 350),
                StartPosition = FormStartPosition.CenterParent,
                BackColor = backgroundColor,
                Font = new Font("Segoe UI", 9)
            };

            Panel contentPanel = new Panel
            {
                Dock = DockStyle.Fill,
                Padding = new Padding(30)
            };

            TableLayoutPanel formLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 4,
                BackColor = Color.Transparent
            };
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40));
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60));

            // Food Item
            Label foodLabel = new Label
            {
                Text = "Food Item:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            TextBox foodTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Margin = new Padding(0, 5, 0, 5)
            };

            // Carbs
            Label carbsLabel = new Label
            {
                Text = "Carbohydrates (g):",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            TextBox carbsTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Margin = new Padding(0, 5, 0, 5)
            };

            // Meal Type
            Label mealLabel = new Label
            {
                Text = "Meal Type:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            ComboBox mealCombo = new ComboBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                DropDownStyle = ComboBoxStyle.DropDownList,
                Margin = new Padding(0, 5, 0, 5)
            };
            mealCombo.Items.AddRange(new string[] { "Breakfast", "Lunch", "Dinner", "Snack" });
            mealCombo.SelectedIndex = 0;

            // Buttons panel
            Panel buttonPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 60,
                BackColor = Color.Transparent
            };

            Button saveBtn = new Button
            {
                Text = "💾 Save Food Entry",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(180, 40),
                Location = new Point(80, 10),
                FlatStyle = FlatStyle.Flat
            };
            saveBtn.FlatAppearance.BorderSize = 0;

            Button cancelBtn = new Button
            {
                Text = "Cancel",
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.White,
                BackColor = mediumPurple,
                Size = new Size(100, 35),
                Location = new Point(280, 12),
                FlatStyle = FlatStyle.Flat
            };
            cancelBtn.FlatAppearance.BorderSize = 0;

            // Events
            saveBtn.Click += (s, e) =>
            {
                if (!string.IsNullOrWhiteSpace(foodTextBox.Text) &&
                    double.TryParse(carbsTextBox.Text, out double carbs))
                {
                    ExecuteNonQuery(
                        @"INSERT INTO food_log (user_id, food_item, carbs, meal_type) 
                        VALUES (@userId, @food, @carbs, @meal)",
                        new MySqlParameter("@userId", currentUserId),
                        new MySqlParameter("@food", foodTextBox.Text),
                        new MySqlParameter("@carbs", carbs),
                        new MySqlParameter("@meal", mealCombo.SelectedItem.ToString())
                    );

                    MessageBox.Show("Food entry added successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    foodForm.Close();
                    ShowTabContent(3); // Refresh food tracker tab
                }
                else
                {
                    MessageBox.Show("Please enter valid food item and carbohydrates!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            };

            cancelBtn.Click += (s, e) => foodForm.Close();

            // Add to layouts
            formLayout.Controls.Add(foodLabel, 0, 0);
            formLayout.Controls.Add(foodTextBox, 1, 0);
            formLayout.Controls.Add(carbsLabel, 0, 1);
            formLayout.Controls.Add(carbsTextBox, 1, 1);
            formLayout.Controls.Add(mealLabel, 0, 2);
            formLayout.Controls.Add(mealCombo, 1, 2);

            buttonPanel.Controls.Add(saveBtn);
            buttonPanel.Controls.Add(cancelBtn);

            contentPanel.Controls.Add(formLayout);
            contentPanel.Controls.Add(buttonPanel);

            foodForm.Controls.Add(contentPanel);
            foodForm.ShowDialog();
        }

        private void CreateA1CTab()
        {
            mainContentContainer.SuspendLayout();

            Label header = new Label
            {
                Text = "📈 A1C Trends & Goals",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };

            // Container for A1C card and button
            Panel topContainer = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 200),
                Location = new Point(0, 50),
                BackColor = Color.Transparent
            };

            // Current A1C Card - FIXED SIZE
            Panel a1cCard = new Panel
            {
                Size = new Size(400, 180),
                Location = new Point(20, 0),
                BackColor = secondaryColor,
                Padding = new Padding(20)
            };

            // Load latest A1C value
            double latestA1C = 6.8;
            DateTime latestDate = DateTime.Now.AddMonths(-1);
            try
            {
                string query = @"SELECT a1c_value, test_date FROM a1c_records 
                               WHERE user_id=@userId 
                               ORDER BY test_date DESC LIMIT 1";
                DataTable result = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));
                if (result.Rows.Count > 0)
                {
                    latestA1C = Convert.ToDouble(result.Rows[0]["a1c_value"]);
                    latestDate = Convert.ToDateTime(result.Rows[0]["test_date"]);
                }
            }
            catch { }

            Label currentLabel = new Label
            {
                Text = "Current A1C",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(20, 20),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label valueLabel = new Label
            {
                Text = $"{latestA1C}%",
                Font = new Font("Segoe UI", 36, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(20, 50),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label dateLabel = new Label
            {
                Text = $"Last Test: {latestDate:MMM dd, yyyy}",
                Font = new Font("Segoe UI", 11),
                ForeColor = Color.White,
                Location = new Point(20, 100),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            Label goalLabel = new Label
            {
                Text = latestA1C < 7.0 ? "Goal: < 7.0% ✓" : "Goal: < 7.0% ⚠️",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(20, 130),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            // Add A1C Button
            Button addA1cBtn = new Button
            {
                Text = "➕ Add A1C Record",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(220, 40),
                Location = new Point(440, 20),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            addA1cBtn.FlatAppearance.BorderSize = 0;
            addA1cBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 100, 150);
            addA1cBtn.Click += (s, e) => ShowAddA1CForm();

            // A1C History
            Panel historyPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 300),
                Location = new Point(20, 270),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(20)
            };

            Label historyTitle = new Label
            {
                Text = "A1C History",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            DataGridView a1cGrid = new DataGridView
            {
                Location = new Point(0, 40),
                Size = new Size(historyPanel.Width - 40, 230),
                BackgroundColor = Color.White,
                RowHeadersVisible = false,
                ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.None,
                AllowUserToAddRows = false
            };

            a1cGrid.Columns.Add("Date", "Test Date");
            a1cGrid.Columns.Add("Value", "A1C Value");
            a1cGrid.Columns.Add("Lab", "Lab Name");
            a1cGrid.Columns.Add("Status", "Status");

            LoadA1CHistory(a1cGrid);

            // Add controls
            a1cCard.Controls.Add(currentLabel);
            a1cCard.Controls.Add(valueLabel);
            a1cCard.Controls.Add(dateLabel);
            a1cCard.Controls.Add(goalLabel);
            topContainer.Controls.Add(a1cCard);
            topContainer.Controls.Add(addA1cBtn);
            historyPanel.Controls.Add(historyTitle);
            historyPanel.Controls.Add(a1cGrid);

            mainContentContainer.Controls.Add(header);
            mainContentContainer.Controls.Add(topContainer);
            mainContentContainer.Controls.Add(historyPanel);

            // Handle resize
            mainContentContainer.Resize += (s, e) =>
            {
                topContainer.Size = new Size(mainContentContainer.ClientSize.Width - 40, 200);
                historyPanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 300);
                historyPanel.Location = new Point(20, 270);
                a1cGrid.Size = new Size(historyPanel.Width - 40, 230);
            };

            mainContentContainer.ResumeLayout();
        }

        private void LoadA1CHistory(DataGridView grid)
        {
            grid.Rows.Clear();
            try
            {
                string query = @"SELECT test_date, a1c_value, lab_name FROM a1c_records 
                               WHERE user_id=@userId 
                               ORDER BY test_date DESC LIMIT 10";
                DataTable data = ExecuteQuery(query, new MySqlParameter("@userId", currentUserId));

                foreach (DataRow row in data.Rows)
                {
                    double a1c = Convert.ToDouble(row["a1c_value"]);
                    string status = a1c < 7.0 ? "Good" : a1c < 8.0 ? "Fair" : "Poor";

                    grid.Rows.Add(
                        Convert.ToDateTime(row["test_date"]).ToString("MM/dd/yyyy"),
                        $"{a1c}%",
                        row["lab_name"] != DBNull.Value ? row["lab_name"].ToString() : "N/A",
                        status
                    );
                }
            }
            catch { }
        }

        private void ShowAddA1CForm()
        {
            Form a1cForm = new Form
            {
                Text = "Add A1C Record",
                Size = new Size(500, 300),
                StartPosition = FormStartPosition.CenterParent,
                BackColor = backgroundColor,
                Font = new Font("Segoe UI", 9)
            };

            Panel contentPanel = new Panel
            {
                Dock = DockStyle.Fill,
                Padding = new Padding(30)
            };

            TableLayoutPanel formLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 3,
                BackColor = Color.Transparent
            };
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40));
            formLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60));

            // A1C Value
            Label valueLabel = new Label
            {
                Text = "A1C Value (%):",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            TextBox valueTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Margin = new Padding(0, 5, 0, 5)
            };

            // Test Date
            Label dateLabel = new Label
            {
                Text = "Test Date:",
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            DateTimePicker datePicker = new DateTimePicker
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                Format = DateTimePickerFormat.Short,
                Margin = new Padding(0, 5, 0, 5)
            };

            // Buttons panel
            Panel buttonPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 60,
                BackColor = Color.Transparent
            };

            Button saveBtn = new Button
            {
                Text = "💾 Save A1C Record",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(180, 40),
                Location = new Point(80, 10),
                FlatStyle = FlatStyle.Flat
            };
            saveBtn.FlatAppearance.BorderSize = 0;

            Button cancelBtn = new Button
            {
                Text = "Cancel",
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.White,
                BackColor = mediumPurple,
                Size = new Size(100, 35),
                Location = new Point(280, 12),
                FlatStyle = FlatStyle.Flat
            };
            cancelBtn.FlatAppearance.BorderSize = 0;

            // Events
            saveBtn.Click += (s, e) =>
            {
                if (double.TryParse(valueTextBox.Text, out double a1c) && a1c > 0 && a1c <= 20)
                {
                    ExecuteNonQuery(
                        @"INSERT INTO a1c_records (user_id, a1c_value, test_date) 
                        VALUES (@userId, @value, @date)",
                        new MySqlParameter("@userId", currentUserId),
                        new MySqlParameter("@value", a1c),
                        new MySqlParameter("@date", datePicker.Value)
                    );

                    MessageBox.Show("A1C record added successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    a1cForm.Close();
                    ShowTabContent(4); // Refresh A1C tab
                }
                else
                {
                    MessageBox.Show("Please enter a valid A1C value (0-20)!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            };

            cancelBtn.Click += (s, e) => a1cForm.Close();

            // Add to layouts
            formLayout.Controls.Add(valueLabel, 0, 0);
            formLayout.Controls.Add(valueTextBox, 1, 0);
            formLayout.Controls.Add(dateLabel, 0, 1);
            formLayout.Controls.Add(datePicker, 1, 1);

            buttonPanel.Controls.Add(saveBtn);
            buttonPanel.Controls.Add(cancelBtn);

            contentPanel.Controls.Add(formLayout);
            contentPanel.Controls.Add(buttonPanel);

            a1cForm.Controls.Add(contentPanel);
            a1cForm.ShowDialog();
        }

        private void CreateDoctorVisitsTab()
        {
            mainContentContainer.SuspendLayout();

            Label header = new Label
            {
                Text = "🏥 Doctor Visits & Reports",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };

            // Upcoming Appointments
            Panel appointmentsPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 200),
                Location = new Point(20, 60),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(20)
            };

            Label appointmentsTitle = new Label
            {
                Text = "📅 Upcoming Appointments",
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                ForeColor = primaryColor,
                Location = new Point(0, 0),
                AutoSize = true,
                BackColor = Color.Transparent
            };

            ListBox appointmentsList = new ListBox
            {
                Location = new Point(0, 40),
                Size = new Size(appointmentsPanel.Width - 40, 130),
                Font = new Font("Segoe UI", 10),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            // Add sample appointment
            appointmentsList.Items.Add("Dr. Smith - Cardiology - Dec 15, 2024");
            appointmentsList.Items.Add("Dr. Johnson - Endocrinology - Jan 10, 2025");

            // Generate Report Button
            Button reportBtn = new Button
            {
                Text = "📄 Generate Doctor Report",
                Font = new Font("Segoe UI", 13, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = infoColor,
                Size = new Size(280, 45),
                Location = new Point(20, 280),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            reportBtn.FlatAppearance.BorderSize = 0;
            reportBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(100, 181, 246);
            reportBtn.Click += (s, e) => GenerateDoctorReport();

            // Add Visit Button
            Button addVisitBtn = new Button
            {
                Text = "➕ Add Doctor Visit",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = primaryColor,
                Size = new Size(220, 40),
                Location = new Point(320, 280),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            addVisitBtn.FlatAppearance.BorderSize = 0;
            addVisitBtn.FlatAppearance.MouseOverBackColor = secondaryColor;

            // Add controls
            appointmentsPanel.Controls.Add(appointmentsTitle);
            appointmentsPanel.Controls.Add(appointmentsList);

            mainContentContainer.Controls.Add(header);
            mainContentContainer.Controls.Add(appointmentsPanel);
            mainContentContainer.Controls.Add(reportBtn);
            mainContentContainer.Controls.Add(addVisitBtn);

            // Handle resize
            mainContentContainer.Resize += (s, e) =>
            {
                appointmentsPanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 200);
                appointmentsList.Size = new Size(appointmentsPanel.Width - 40, 130);
                reportBtn.Location = new Point(20, 280);
                addVisitBtn.Location = new Point(320, 280);
            };

            mainContentContainer.ResumeLayout();
        }

        private void CreateSettingsTab()
        {
            mainContentContainer.SuspendLayout();

            Label header = new Label
            {
                Text = "⚙️ Settings & Preferences",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = primaryColor,
                AutoSize = true,
                Location = new Point(0, 0),
                BackColor = Color.Transparent
            };

            // Settings Panel
            Panel settingsPanel = new Panel
            {
                Size = new Size(mainContentContainer.ClientSize.Width - 40, 400),
                Location = new Point(20, 60),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(30)
            };

            // Settings form using TableLayoutPanel
            TableLayoutPanel settingsLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 4,
                BackColor = Color.Transparent
            };
            settingsLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40));
            settingsLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60));

            // Notification Settings
            Label notifLabel = new Label
            {
                Text = "Enable Notifications:",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            CheckBox notifCheckbox = new CheckBox
            {
                Dock = DockStyle.Left,
                Checked = true,
                Margin = new Padding(0, 10, 0, 10)
            };

            // Glucose Reminders
            Label glucoseLabel = new Label
            {
                Text = "Glucose Reminders:",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            ComboBox glucoseCombo = new ComboBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                DropDownStyle = ComboBoxStyle.DropDownList,
                Margin = new Padding(0, 5, 0, 5)
            };
            glucoseCombo.Items.AddRange(new string[] { "Every 2 hours", "Every 3 hours", "Every 4 hours", "Custom" });
            glucoseCombo.SelectedIndex = 1;

            // Theme Selection
            Label themeLabel = new Label
            {
                Text = "Theme:",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = darkColor,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight,
                Padding = new Padding(0, 0, 10, 0)
            };

            ComboBox themeCombo = new ComboBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                DropDownStyle = ComboBoxStyle.DropDownList,
                Margin = new Padding(0, 5, 0, 5)
            };
            themeCombo.Items.AddRange(new string[] { "Purple Theme", "Blue Theme", "Green Theme", "Dark Mode" });
            themeCombo.SelectedIndex = 0;

            // Save Button
            Panel buttonPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 60,
                BackColor = Color.Transparent
            };

            Button saveSettingsBtn = new Button
            {
                Text = "💾 Save Settings",
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.White,
                BackColor = accentColor,
                Size = new Size(200, 40),
                Location = new Point(settingsPanel.Width / 2 - 100, 10),
                FlatStyle = FlatStyle.Flat,
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            saveSettingsBtn.FlatAppearance.BorderSize = 0;
            saveSettingsBtn.FlatAppearance.MouseOverBackColor = Color.FromArgb(255, 100, 150);

            saveSettingsBtn.Click += (s, e) =>
            {
                MessageBox.Show("Settings saved successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            };

            // Add to layouts
            settingsLayout.Controls.Add(notifLabel, 0, 0);
            settingsLayout.Controls.Add(notifCheckbox, 1, 0);
            settingsLayout.Controls.Add(glucoseLabel, 0, 1);
            settingsLayout.Controls.Add(glucoseCombo, 1, 1);
            settingsLayout.Controls.Add(themeLabel, 0, 2);
            settingsLayout.Controls.Add(themeCombo, 1, 2);

            buttonPanel.Controls.Add(saveSettingsBtn);

            settingsPanel.Controls.Add(settingsLayout);
            settingsPanel.Controls.Add(buttonPanel);

            mainContentContainer.Controls.Add(header);
            mainContentContainer.Controls.Add(settingsPanel);

            // Handle resize
            mainContentContainer.Resize += (s, e) =>
            {
                settingsPanel.Size = new Size(mainContentContainer.ClientSize.Width - 40, 400);
                saveSettingsBtn.Location = new Point(settingsPanel.Width / 2 - 100, 10);
            };

            mainContentContainer.ResumeLayout();
        }

        private void GenerateDoctorReport()
        {
            SaveFileDialog saveDialog = new SaveFileDialog
            {
                Filter = "Text Files|*.txt",
                Title = "Save Doctor Report",
                FileName = $"Diabetes_Report_{DateTime.Now:yyyyMMdd}.txt"
            };

            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    string report = GenerateReportText();
                    File.WriteAllText(saveDialog.FileName, report);
                    MessageBox.Show($"Report saved successfully!\n{saveDialog.FileName}",
                        "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error saving report: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private string GenerateReportText()
        {
            string report = $"DIABETES MANAGEMENT REPORT\n";
            report += $"Generated: {DateTime.Now:yyyy-MM-dd HH:mm}\n";
            report += $"Patient: {currentUsername}\n";
            report += new string('=', 50) + "\n\n";

            try
            {
                // Glucose Summary
                report += "GLUCOSE SUMMARY (Last 30 Days):\n";
                string glucoseQuery = @"SELECT 
                    COUNT(*) as readings,
                    AVG(glucose_value) as avg_glucose,
                    MIN(glucose_value) as min_glucose,
                    MAX(glucose_value) as max_glucose,
                    SUM(CASE WHEN status = 'Low' THEN 1 ELSE 0 END) as low_count,
                    SUM(CASE WHEN status = 'High' THEN 1 ELSE 0 END) as high_count
                    FROM glucose_readings 
                    WHERE user_id=@userId AND reading_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)";

                DataTable glucoseData = ExecuteQuery(glucoseQuery, new MySqlParameter("@userId", currentUserId));
                if (glucoseData.Rows.Count > 0)
                {
                    var row = glucoseData.Rows[0];
                    report += $"Total Readings: {row["readings"]}\n";

                    if (row["avg_glucose"] != DBNull.Value)
                        report += $"Average Glucose: {Math.Round(Convert.ToDouble(row["avg_glucose"]), 1)} mg/dL\n";

                    if (row["min_glucose"] != DBNull.Value && row["max_glucose"] != DBNull.Value)
                        report += $"Range: {row["min_glucose"]} - {row["max_glucose"]} mg/dL\n";

                    report += $"Low Readings: {row["low_count"]}\n";
                    report += $"High Readings: {row["high_count"]}\n";
                }

                // Medications
                report += "\nCURRENT MEDICATIONS:\n";
                string medsQuery = @"SELECT name, dosage, schedule_time FROM medications 
                                   WHERE user_id=@userId AND is_active=TRUE";
                DataTable medsData = ExecuteQuery(medsQuery, new MySqlParameter("@userId", currentUserId));
                if (medsData.Rows.Count > 0)
                {
                    foreach (DataRow row in medsData.Rows)
                    {
                        string dosage = row["dosage"] != DBNull.Value ? row["dosage"].ToString() : "";
                        string time = row["schedule_time"] != DBNull.Value ? row["schedule_time"].ToString() : "As needed";
                        report += $"• {row["name"]}: {dosage} at {time}\n";
                    }
                }
                else
                {
                    report += "No active medications\n";
                }

                // Recent Glucose Readings
                report += "\nRECENT GLUCOSE READINGS:\n";
                string recentQuery = @"SELECT reading_time, glucose_value, reading_type, status 
                                     FROM glucose_readings WHERE user_id=@userId 
                                     ORDER BY reading_time DESC LIMIT 10";
                DataTable recentData = ExecuteQuery(recentQuery, new MySqlParameter("@userId", currentUserId));
                if (recentData.Rows.Count > 0)
                {
                    foreach (DataRow row in recentData.Rows)
                    {
                        report += $"{Convert.ToDateTime(row["reading_time"]):MM/dd HH:mm} - ";
                        report += $"{row["glucose_value"]} mg/dL ({row["reading_type"]}) - {row["status"]}\n";
                    }
                }
                else
                {
                    report += "No recent glucose readings\n";
                }

                report += "\nEND OF REPORT";
            }
            catch (Exception ex)
            {
                report += $"Error generating report: {ex.Message}";
            }

            return report;
        }
    }
}