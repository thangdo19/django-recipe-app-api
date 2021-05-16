# Test 'Client', allow us to make test requests
# to the application in unit tests
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
# Helper function 'reverse', allow us to generate URLs for admin page
from django.urls import reverse


class AdminSiteTests(TestCase):
    # Setup function - function that runs before every test that we
    # run. Sometime, there're some tasks that needs to be done before
    # every test in our TestCase class
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@email.com',
            password='password',
        )
        # Login with the Django authentication
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@email.com',
            password='password',
            name='Test user full name',
        )

    def test_users_listed(self):
        """ Test that users are listed on user page """
        # This will generate the URL for out list user page
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """
        # /admin/core/user/:id
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
