namespace HealthMateLite.Models;

public class HealthMetric
{
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public DateTime Date { get; set; } = DateTime.Now;
    public decimal Weight { get; set; }
    public int Systolic { get; set; }
    public int Diastolic { get; set; }
    public decimal SleepHours { get; set; }
    
    public string BloodPressure => $"{Systolic}/{Diastolic}";
}