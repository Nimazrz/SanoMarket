import django_filters
from market.models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices=Product.Category.choices)

    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'description': ['iexact', 'icontains'],
            'price': ['iexact', 'lt', 'gt', 'range'],
            'category': ['exact']
        }
