from django.db import models

# Create your models here.
class company(models.Model):
   companies = models.CharField(max_length=100)
   price = models.CharField(max_length=100)
   gmp = models.CharField(max_length=100)
   gain = models.IntegerField()
   date = models.CharField(max_length=100)
   type = models.CharField(max_length=100)
   sauda = models.CharField(max_length=100)
   allotment = models.CharField(max_length=100)
   qty = models.CharField(max_length=100)
   qi = models.CharField(max_length=100)
   ri = models.CharField(max_length=100)
   ni = models.CharField(max_length=100)
   total_sub = models.CharField(max_length=100)

   def _str_(self):
      return self.companies
