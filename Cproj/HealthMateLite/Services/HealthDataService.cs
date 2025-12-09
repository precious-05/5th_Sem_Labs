using HealthMateLite.Models;

namespace HealthMateLite.Services;

public class HealthDataService
{
    private readonly List<User> _users = new()
    {
        new User { Username = "john", Password = "123", DisplayName = "John Doe" },
        new User { Username = "jane", Password = "456", DisplayName = "Jane Smith" }
    };

    private readonly List<HealthMetric> _healthMetrics = new();
    private readonly List<Medication> _medications = new();
    private int _healthMetricId = 1;
    private int _medicationId = 1;

    public User? Authenticate(string username, string password)
    {
        return _users.FirstOrDefault(u => 
            u.Username == username && u.Password == password);
    }

    // Health Metrics Methods
    public void AddHealthMetric(HealthMetric metric)
    {
        metric.Id = _healthMetricId++;
        _healthMetrics.Add(metric);
    }

    public List<HealthMetric> GetHealthMetrics(string username)
    {
        return _healthMetrics
            .Where(m => m.Username == username)
            .OrderByDescending(m => m.Date)
            .ToList();
    }

    // Medications Methods
    public void AddMedication(Medication medication)
    {
        medication.Id = _medicationId++;
        _medications.Add(medication);
    }

    public List<Medication> GetMedications(string username)
    {
        return _medications
            .Where(m => m.Username == username)
            .OrderBy(m => m.Name)
            .ToList();
    }

    public void RemoveMedication(int id, string username)
    {
        var medication = _medications.FirstOrDefault(m => 
            m.Id == id && m.Username == username);
        if (medication != null)
        {
            _medications.Remove(medication);
        }
    }
}