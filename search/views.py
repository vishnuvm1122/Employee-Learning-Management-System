# ========================================================
# Django & Python Imports
# ========================================================
from itertools import chain
from django.views.generic import ListView
from django.db.models import Q

from core.models import NewsAndEvents
from course.models import Program, Course
from quiz.models import Quiz, Sitting
from courseallocations.models import CourseAllocation


# ========================================================
# Search View
# ========================================================
from itertools import chain
from django.views.generic import ListView
from django.db.models import Q


class SearchView(ListView):
    template_name = "search/search_view.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q", "")
        return context

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        user = self.request.user

        if not query:
            return []

        # =====================================
        # NEWS & EVENTS
        # =====================================
        news_events_results = NewsAndEvents.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query)
        )

        # =====================================
        # PROGRAMS
        # =====================================
        program_results = Program.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query)
        )

        # =====================================
        # COURSES
        # =====================================
        # course_results = Course.objects.filter(
        #     Q(title__icontains=query) |
        #     Q(summary__icontains=query) |
        #     Q(code__icontains=query)
        # )

        # =====================================
        # QUIZ
        # =====================================
        # quiz_results = Quiz.objects.filter(
        #     Q(title__icontains=query) |
        #     Q(description__icontains=query) |
        #     Q(category__icontains=query)
        # )

        # =====================================
        # COURSE ALLOCATION
        # Hide current user + superuser
        # =====================================
        allocation_results = CourseAllocation.objects.filter(
            Q(courses__title__icontains=query) |
            Q(employee__username__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query)
        ).exclude(
            employee=user
        ).exclude(
            employee__is_superuser=True
        ).distinct()

        # =====================================
        # SITTING
        # Hide current user + superuser
        # =====================================
        sitting_results = Sitting.objects.filter(
            Q(employee__username__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(quiz__title__icontains=query) |
            Q(course__title__icontains=query)
        ).exclude(
            employee=user
        ).exclude(
            employee__is_superuser=True
        )

        # =====================================
        # COMBINE
        # =====================================
        combined_results = chain(
            news_events_results,
            program_results,
            # course_results,
            # quiz_results,
            allocation_results,
            sitting_results
        )

        queryset = sorted(
            combined_results,
            key=lambda obj: getattr(obj, "pk", 0),
            reverse=True
        )

        self.count = len(queryset)
        return queryset