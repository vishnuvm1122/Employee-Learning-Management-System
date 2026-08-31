from django.db.models import Q
import django_filters
from .models import Program


# ========================
# Program Filter
# ========================
class ProgramFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label=""
    )

    class Meta:
        model = Program
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters["title"].field.widget.attrs.update({
            "class": "form-control",
            "placeholder": "Search program..."
        })


