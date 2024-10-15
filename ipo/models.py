from django.db import models

# Create your models here.
class company(models.Model):
   companies = models.CharField(max_length=100, blank=True)
   price = models.CharField(max_length=100, blank=True)
   gmp = models.CharField(max_length=100, blank=True, default= "₹0")
   gain = models.FloatField(blank=True, default = 0)
   changed = models.CharField(max_length=100, blank=True, default= "")
   date = models.CharField(max_length=100, blank=True)
   type = models.CharField(max_length=100, blank=True)
   sauda = models.CharField(max_length=100, blank=True, default="₹0")
   qty = models.CharField(max_length=100, blank=True)
   pe = models.FloatField(null=True, blank=True)
   qi = models.CharField(max_length=100, blank=True)
   ri = models.CharField(max_length=100, blank=True)
   ni = models.CharField(max_length=100, blank=True)
   shni = models.CharField(max_length=100, blank=True)
   bhni = models.CharField(max_length=100, blank=True)
   total_sub = models.CharField(max_length=100, blank=True)
   closing = models.CharField(max_length=100, blank=True)

   def _str_(self):
      return self.companies
