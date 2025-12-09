namespace HealthMateLite.Models;

public class Medication
{
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Dosage { get; set; } = string.Empty;
    public DateTime AddedDate { get; set; } = DateTime.Now;
}