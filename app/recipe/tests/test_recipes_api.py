from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """ Create and return a sample recipe """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ Test the publicly available recipe API """

    def setUp(self):
        self.client = APIClient()

    def test_login(self):
        """ Test that login is required to access the endpoint """
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """ Test the private recipes API """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe_list(self):
        """ Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user, title='Sample Recipe 2')

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.order_by('-price')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """ Test that only recipes for
            the authenticated user are returned """
        other_user = get_user_model().objects.create_user(
            'other@email.com',
            'password',
        )
        sample_recipe(user=other_user, title='Other 1')
        sample_recipe(user=other_user, title='Other 2')

        recipe_title = 'Title'
        sample_recipe(user=self.user, title=recipe_title)

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], recipe_title)
