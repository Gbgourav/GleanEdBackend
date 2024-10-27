from django.db import models

# Create your models here.

class UniversityShortlistRequest(models.Model):
    cgpa = models.FloatField()
    current_college = models.CharField(max_length=255)
    current_country = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    estimated_budget = models.IntegerField()
    shortlist_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shortlist request for {self.current_college} student to {self.destination_country}"
