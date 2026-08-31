from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


# ---------------- CHOICES ----------------

class PostType(models.TextChoices):
    NEWS = "News", _("Training Announcement")
    EVENTS = "Events", _("Employee Appreciation")


# ---------------- QUERYSET ----------------

class NewsAndEventsQuerySet(models.QuerySet):
    def search(self, query):
        if not query:
            return self

        return self.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(posted_as__icontains=query)
        ).distinct()


# ---------------- MANAGER ----------------

class NewsAndEventsManager(models.Manager):
    def get_queryset(self):
        return NewsAndEventsQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def search(self, query):
        return self.get_queryset().search(query)


# ---------------- MODEL ----------------

class NewsAndEvents(models.Model):
    title = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to='news_events_pictures/',
        blank=True,
        null=True
    )

    posted_as = models.CharField(
        max_length=30,
        choices=PostType.choices,
        default=PostType.NEWS
    )

    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    objects = NewsAndEventsManager()

    class Meta:
        ordering = ['-upload_time']
        verbose_name = "News / Event"
        verbose_name_plural = "News & Events"

    def __str__(self):
        return self.title if self.title else "Untitled"

    def get_post_type_display_name(self):
        return self.get_posted_as_display()
    
    
class ActivityLog(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message