from django.test import TestCase 
from django.urls import reverse 

class BaseTest(TestCase):
    def setUp(self): 
        self.register_url = reverse('registerView')
        self.user = { 
            'first_name':'User',
            'last_name':'User', 
            'username':'user',
            'email':'user@gmail.com',
            'password1':'django123',
            'password2':'django123',
        }
        return super().setUp()

class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Register/register.html')
    
 
