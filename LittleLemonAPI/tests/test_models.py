from django.test import TestCase
from .. import models
from django.contrib.auth.models import User


# Create your tests here.
class CategoryModelTest(TestCase):
    def setUp(self):
        category = models.Category(title='testcategory', slug='test-category')
        category.save()
        user = User(username='tester',password='12345@Qwerty',email='tester@ll.com')
        user.save()
    
    def test_category(self):
        num_of_categories = models.Category.objects.all().count()
        category = models.Category(title='anothercategory', slug='test-category')
        category.save()
        self.assertEqual(num_of_categories+1,models.Category.objects.all().count())
        
    def test_menuitem(self):
        category = models.Category.objects.get(title='testcategory')
        num_of_menuitems = models.MenuItem.objects.all().count()
        menuitem = models.MenuItem(category = category, title='menuitem', price = 12, featured = False)
        menuitem.save()
        self.assertEqual(num_of_menuitems+1,models.MenuItem.objects.all().count())

    
    def test_booking(self):
        user = User.objects.get(username='tester')
        num_of_bookings = models.Booking.objects.all().count()
        booking = models.Booking(user=user, date='2000-04-21', tabel = 1, slot = 10, num_of_guests=1)
        booking.save()
        self.assertEqual(num_of_bookings+1,models.Booking.objects.all().count())
        

#TODO add testing for all models and test further than just createing objects
#TODO test views and add integration tests
        