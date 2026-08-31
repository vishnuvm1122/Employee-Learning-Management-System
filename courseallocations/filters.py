import django_filters
from django.db.models import Q
from .models import CourseAllocation

# ========================
# Course Allocation Filter
# ========================
class CourseAllocationFilter(django_filters.FilterSet):
    course = django_filters.CharFilter(
        method="filter_by_course",
        label=""
    )

    class Meta:
        model = CourseAllocation
        fields = []  # No direct model fields, filtering via method

    # 🔍 Filter by Course Name
    def filter_by_course(self, queryset, name, value):
        # Filter allocations where any assigned course title contains the value
        return queryset.filter(courses__title__icontains=value).distinct()

    # Customize widget
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["course"].field.widget.attrs.update({
            "class": "form-control",
            "placeholder": "Search course..."
        })