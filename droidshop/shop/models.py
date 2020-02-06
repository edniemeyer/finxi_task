from django.db import models

class Demand(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]
    
    description = models.TextField()
    address = models.TextField()
    info = models.TextField()
    advertiser = models.ForeignKey('auth.User', related_name='demands', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=OPEN,
    )