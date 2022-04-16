from django.test import TestCase, Client
from django.urls import reverse
from .models import Vendor 

import json 
from pprint import pprint as pp 
class TestViews(TestCase):



    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.vendor_admin_url = reverse('vendor_admin')
        


    def _test_login(self):

        '''
            Unit test for logging in. 
            - Asserts that a status of 200 is returned 
            - Asserts that the vendor/login.html template
        '''
        response = self.client.post(self.login_url, {'username': 'francesco', 'password': '1234    '})

        self.assertEqual(response.status_code,200) # HTTP OK
        self.assertTemplateUsed(response,'vendor/login.html') # Check the right template was served
    
    # def test_admin_page(self):
        
    #     response = self.client.get(self.vendor_admin_url)


    def test_update_name(self):

        response = self.client.post(self.login_url, {'username': 'francesco', 'password': '1234    '},SERVER_NAME='127.0.0.1')
        print(response)
        response = self.client.post(self.vendor_admin_url,{'update':'1','store_name':'OLDNAME'},follow=True)
        name = Vendor.objects.first()
        self.assertEqual('OLDNAME',name)
        self.assertEqual(response.status_code,200) # HTTP OK
        