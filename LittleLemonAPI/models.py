from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255,db_index=True)
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255,db_index=True)
    price = models.DecimalField(max_digits=5,decimal_places=2,db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta():
        unique_together = ('menuitem','user')
        
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='delivery_crew',null=True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    date = models.DateField(db_index=True)    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="order",on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta():
        unique_together=('order','menuitem')
        
        
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    tabel = models.SmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    slot = models.SmallIntegerField(validators=[MinValueValidator(8),MaxValueValidator(23)])
    num_of_guests = models.SmallIntegerField(validators=[MinValueValidator(1)])

    #TODO add limits maybe in conf file
    
    class Meta():
        unique_together=('date','slot','tabel')
    
    
#TODO add reviews from users