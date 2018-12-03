from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

if __name__ == '__main__': 
  # Using the standard RequestFactory API to create a form POST request
  factory = APIRequestFactory()
  request = factory.post('/api/', {'title': 'new idea'}, format='json')