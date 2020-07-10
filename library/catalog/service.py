from django_filters import rest_framework as filters
from .models import BookInstance


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookInstanceFilter(filters.FilterSet):
    book = CharFilterInFilter(field_name='book__title', lookup_expr='in')
    publishing_year = filters.RangeFilter()

    class Meta:
        model = BookInstance
        fields = ['book', 'publishing_year']
