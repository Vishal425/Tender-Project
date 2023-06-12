from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class test_tender_model(models.Model):
    IDs = models.AutoField(primary_key=True)
    E_Published_Date = models.DateField()
    Closing_Date = models.DateField()
    Opening_Date= models.DateField()
    Organisation_Chain= models.CharField(max_length=500)
    Tender_Title= models.CharField(max_length=1000)
    Ref_NO= models.CharField(max_length=100)
    Tender_ID= models.CharField(max_length=50)
    Tender_URL=models.CharField(max_length = 1000)
    
    class Meta:
      db_table = "test_tender_model"


class tender_keword_models(models.Model):
    keywords= models.CharField(max_length=50)
    class Meta:
        db_table='test_tender_kewords'      
            
        

        
