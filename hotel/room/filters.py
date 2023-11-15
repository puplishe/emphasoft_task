from datetime import date

import django_filters

from .models import Room


class RoomFilter(django_filters.FilterSet):
    capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    check_in = django_filters.DateFilter(method='filter_check_in')
    check_out = django_filters.DateFilter(method='filter_check_out')

    class Meta:
        model = Room
        fields = ['capacity', 'price_per_night']

    def filter_check_in(self, queryset, name: str, value: date | str) -> Room:
        """
        Фильтр для вывода свободных комнат в интервале.
        """
        return queryset.exclude(reservation__check_out__gte=value, reservation__check_in__lte=value)

    def filter_check_out(self, queryset, name: str, value: date | str) -> Room:
        """
        Фильтр для вывода свободных комнат в интервале.
        """
        return queryset.exclude(reservation__check_out__gte=value, reservation__check_in__lte=value)
