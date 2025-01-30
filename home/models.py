from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    rating = models.IntegerField()
    feedback_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        db_table = 'feedback'  # Specify the existing table name
        managed = False  # Tell Django not to manage this table

    def __str__(self):
        return f"{self.name}'s feedback"