from django.test import TestCase
from django.urls import reverse

from .models import Category, Listing, Cart, UserAccountManager, UserBase


class CategoryTest(TestCase):
    def setUp(self):
        self.data = Category.objects.create(name='Test Category', slug='test-category', details='')
    
    def test__str__(self):
        data = self.data
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'Test Category')

    def testGet_absolute_url(self):
        data = self.data
        response = self.client.post(reverse('MVC:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

 
class ListingTest(TestCase):
    def setUp(self):
        Category.objects.create(name='Test Category', slug='test-category', details='')
        UserBase.objects.create(email='testAdmin@email.com', user_name='testAdmin', password='')
        self.data1 = Listing.objects.create(category_id=1, name='Product 1 name', created_by_id=1,
                                            slug='product-1-name', price='20.00', image='default',
                                             inventory='3')
        self.data2 = Listing.listings.create(category_id=1, name='Product 2 name', created_by_id=1,
                                             slug='product-2-name', price='30.00', image='default',
                                              for_sale=False, inventory='6')
 
    def test__str__(self):
        data = self.data1
        self.assertTrue(isinstance(data, Listing))
        self.assertEqual(str(data), 'Product 1 name')

    def testGet_absolute_url(self):
        data = self.data1
        url = reverse('MVC:listing_detail', args=[data.slug])
        self.assertEqual(url, '/listing/product-1-name/')
        response = self.client.post( reverse('MVC:listing_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def testListingManager(self):
        data = Listing.listings.all()
        self.assertEqual(data.count(), 1)


class CartTest(TestCase):
    def setUp(self):
        Category.objects.create(name='Test Category', slug='test-category', details='')
        UserBase.objects.create(email='testAdmin@email.com', user_name='testAdmin', password='')
        Listing.objects.create(category_id=1, name='Product 1 name', created_by_id=1,
                                                slug='product-1-name', price='10.00',
                                                image='default', inventory='5')
        Listing.objects.create(category_id=1, name='Product 2 name', created_by_id=1,
                                                slug='product-2-name', price='20.00',
                                                image='default', inventory='6')
        Listing.objects.create(category_id=1, name='Product 3 name', created_by_id=1,
                                                slug='product-3-name', price='30.00',
                                                image='default', inventory='9')
        self.client.post(reverse('MVC:cart_add'), {"listingid": 1, "listingqty": 1, "action": "post"}, xhr=True)
        self.client.post(reverse('MVC:cart_add'), {"listingid": 2, "listingqty": 2, "action": "post"}, xhr=True)

    def test__str__(self):
        response = self.client.get(reverse('MVC:cart_summary'))
        self.assertEqual(response.status_code, 200)

    def testAdd(self):
        response = self.client.post(reverse('MVC:cart_add'), {"listingid": 3, "listingqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(reverse('MVC:cart_add'), {"listingid": 2, "listingqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def testDelete(self):
        response = self.client.post(reverse('MVC:cart_delete'), {"listingid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '10.00', 'total': '60.00'})

    def testUpdate(self):
        response = self.client.post(reverse('MVC:cart_update'), {"listingid": 2, "listingqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '30.00', 'total': '80.00'})


class UserAccountManagerTest(TestCase):
    def setUp(self):
        pass

    def testCreate_user(self):
        data = UserBase.objects.create_user(email='testUser@email.com', user_name='testUser', password='')
        self.assertEqual(data.is_active, True)
        self.assertEqual(data.is_staff, False)
        self.assertEqual(str(data), 'testUser')

    def testCreate_superuser(self):
        data = UserBase.objects.create_superuser(email='testAdmin@email.com', user_name='testAdmin', password='')
        self.assertEqual(data.is_active, True)
        self.assertEqual(data.is_staff, True)
        self.assertEqual(str(data), 'testAdmin')


class UserBaseTest(TestCase):
    def setUp(self):
        self.data = UserBase.objects.create(email='testAdmin@email.com', user_name='testAdmin', password='')
 
    def test__str__(self):
        data = self.data
        self.assertTrue(isinstance(data, UserBase))
        self.assertEqual(str(data), 'testAdmin')
