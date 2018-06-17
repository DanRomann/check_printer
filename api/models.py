from django.db import models
from django.contrib.postgres.fields import JSONField


CHECK_TYPE = (
    ('KT', 'kitchen'),
    ('CL', 'client')
)


STATUS = (
    ('NW', 'new'),
    ('RN', 'rendered'),
    ('PR', 'printed')
)


# Create your models here.
class Printer(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    check_type = models.CharField(choices=CHECK_TYPE, max_length=10)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + str(self.point_id)


class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, blank=True)
    type = models.CharField(choices=CHECK_TYPE, max_length=10)
    order = JSONField()
    status = models.CharField(choices=STATUS, max_length=10)
    pdf_file = models.FileField()

    # def __str__(self):
    #     return