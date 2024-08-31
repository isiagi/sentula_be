from django_filters import rest_framework as filters
from .models import Wagubumbuzi

class WagubumbuziFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="user__username",lookup_expr='icontains')
    class Meta:
        model = Wagubumbuzi
        fields = ['username']