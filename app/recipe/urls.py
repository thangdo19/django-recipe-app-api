from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'


# 'app_name' and 'name' is supported
# for 'reverse': 'user:create' when testing in request
urlpatterns = [
    path('', include(router.urls)),
]
