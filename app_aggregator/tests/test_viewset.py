import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from app_aggregator.model_choices import UserTypes
from app_aggregator.models import AppData, UserPurchasedApps


class AppDataViewSetTestCase(APITestCase):
    def setUp(self):
        # Create AGGREGATOR user
        self.aggregator_user = get_user_model().objects.create_user(
            username='aggregator_user',
            password='password123',
            type=UserTypes.AGGREGATOR
        )

        # Create USER user
        self.user_user = get_user_model().objects.create_user(
            username='user_user',
            password='password456',
            type=UserTypes.USER
        )
        self.valid_app_name = 'WhatsApp Messenger'
        self.valid_url = "https://play.google.com/store/apps/details?id=com.whatsapp"
        self.valid_data = {
            'url': self.valid_url,
            'active': True
        }

    def test_create_app(self):
        # Test case for AGGREGATOR user
        self.client.force_authenticate(self.aggregator_user)

        url = reverse('app_data-list')

        # Test valid creation
        response = self.client.post(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the data is parsed correctly and the app is created
        app_data = AppData.objects.get(id=response.data['id'])
        self.assertEqual(app_data.name, self.valid_app_name)
        self.assertEqual(app_data.url, self.valid_url)
        self.assertEqual(app_data.active, True)

        # Test case for USER user
        self.client.force_authenticate(self.user_user)
        response = self.client.post(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(AppData.objects.count(), 1)  # Ensure the app is not created

    def test_delete_app(self):
        self.client.force_authenticate(self.aggregator_user)
        url = reverse('app_data-list')
        valid_response = self.client.post(url, self.valid_data, format='json')

        # Test case for USER user
        self.client.force_authenticate(self.user_user)
        detail_url = reverse('app_data-detail', kwargs={'pk': valid_response.data['id']})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(AppData.objects.count(), 1)  # Ensure the app is not deleted

        self.client.force_authenticate(self.aggregator_user)

        # Test case for AGGREGATOR user
        # Test case to check if App can be deleted after Purchased by User
        UserPurchasedApps.objects.create(app_id=valid_response.data['id'], user=self.user_user)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, 'Cannot delete. Some Users have purchased this app')
        self.user_user.purchased_app.all().delete()

        # Test valid delete
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AppData.objects.count(), 0)  # Ensure the app is deleted

    def test_ban_app(self):
        self.client.force_authenticate(self.aggregator_user)
        url = reverse('app_data-list')
        valid_response = self.client.post(url, self.valid_data, format='json')
        detail_url = reverse('app_data-detail', kwargs={'pk': valid_response.data['id']})

        # Test case for USER user
        self.client.force_authenticate(self.user_user)
        response = self.client.patch(f'{detail_url}ban_app/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        app_data = AppData.objects.get(id=valid_response.data['id'])
        self.assertTrue(app_data.active)  # Ensure the app is not banned

        # Test case for AGGREGATOR user
        self.client.force_authenticate(self.aggregator_user)
        response = self.client.patch(f'{detail_url}ban_app/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        app_data = AppData.objects.get(id=valid_response.data['id'])
        self.assertFalse(app_data.active)  # Ensure the app is banned


class AppListViewSetTestCase(APITestCase):
    def setUp(self):
        # Create AGGREGATOR user
        self.aggregator_user = get_user_model().objects.create_user(
            username='aggregator_user',
            password='password123',
            type=UserTypes.AGGREGATOR
        )

        # Create USER user
        self.user_user = get_user_model().objects.create_user(
            username='user_user',
            password='password456',
            type=UserTypes.USER
        )

    def test_app_list(self):
        url = reverse('active_apps-list')

        # Create 2 active and 1 Inactive Apps
        self.client.force_authenticate(self.aggregator_user)
        self.client.post(reverse('app_data-list'),
                         data={'url': "https://play.google.com/store/apps/details?id=com.whatsapp", 'active': True},
                         format='json')
        self.client.post(reverse('app_data-list'),
                         data={'url': "https://play.google.com/store/apps/details?id=com.flipkart.android",
                               'active': True},
                         format='json')
        self.client.post(reverse('app_data-list'),
                         data={'url': "https://play.google.com/store/apps/details?id=com.activision.callofduty.warzone&hl=en&gl=US",
                               'active': False},
                         format='json')

        # Users should be able to access the list of active apps
        self.client.force_authenticate(self.user_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 active apps should be available in list view
        self.assertEqual(len(response.data), 2)

        # Aggregator should also be able to view
        self.client.force_authenticate(self.aggregator_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 active apps should be available in list view
        self.assertEqual(len(response.data), 2)


class UserPurchasesViewSetTestCase(APITestCase):
    def setUp(self):
        # Create AGGREGATOR user
        self.aggregator_user = get_user_model().objects.create_user(
            username='aggregator_user',
            password='password123',
            type=UserTypes.AGGREGATOR
        )

        # Create USER user
        self.user_user = get_user_model().objects.create_user(
            username='user_user',
            password='password456',
            type=UserTypes.USER
        )

    def test_purchased_apps(self):
        # Create App
        self.client.force_authenticate(self.aggregator_user)
        app_data_response = self.client.post(reverse('app_data-list'),
                         {'url': "https://play.google.com/store/apps/details?id=com.whatsapp", "active": True},
                         format='json')

        self.client.force_authenticate(self.user_user)

        url = reverse('user_purchases-list')
        response = self.client.post(url, data={'app': app_data_response.data['id']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['app_name'], "WhatsApp Messenger")

        # Same User should not be able to add same app
        response = self.client.post(url, data={'app': app_data_response.data['id']})
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
        self.assertEqual(response.data['error_data'], "You have already purchased this app.")
