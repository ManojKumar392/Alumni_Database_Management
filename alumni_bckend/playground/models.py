from django.db import models

class Alumni(models.Model):
    Alumni_ID = models.CharField(max_length=10, primary_key=True)
    First_name = models.CharField(max_length=10)
    Last_name = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=20, null=True)
    Address = models.CharField(max_length=20, null=True)
    Contact_No = models.BigIntegerField(null=True)
    minors = models.CharField(max_length=10, null=True)
    Batch_id = models.CharField(max_length=10, null=True)
    Position_id = models.CharField(max_length=10, null=True)
    Donation_id = models.CharField(max_length=10, null=True)

    def __str__(self):
        if self.Last_name:   
            return self.First_name + ' ' + self.Last_name
        else:
            return self.First_name
    class Meta:
        db_table = 'alumni'


class Work(models.Model):
    position_id = models.CharField(max_length=10)
    position_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.position_name
    

class JobOpening(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    application_deadline = models.DateField()
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return self.title
    
class User(models.Model):
    password = models.CharField(max_length=100)
    passkey = models.CharField(max_length=100)