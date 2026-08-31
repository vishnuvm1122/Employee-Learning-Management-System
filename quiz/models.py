# ========================================================
# Django & Python Imports
# ========================================================
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from model_utils.managers import InheritanceManager
from course.models import Course


# ========================================================
# Constants
# ========================================================
CHOICE_ORDER_OPTIONS = (
    ("content", _("Content")),
    ("random", _("Random")),
    ("none", _("None")),
)

CATEGORY_OPTIONS = (
    ("assignment", _("Assignment")),
    ("exam", _("Exam")),
    ("practice", _("Practice Quiz")),
)


# ========================================================
# Quiz & Manager
# ========================================================
class QuizManager(models.Manager):
    """Custom manager for Quiz model."""
    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            ).distinct()
        return qs


class Quiz(models.Model):
    """Model representing a quiz."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(_("Title"), max_length=60)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_OPTIONS, blank=True)

    random_order = models.BooleanField(default=False)
    answers_at_end = models.BooleanField(default=False)
    exam_paper = models.BooleanField(default=False)
    single_attempt = models.BooleanField(default=False)

    pass_mark = models.SmallIntegerField(default=50, validators=[MaxValueValidator(100)])
    draft = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    objects = QuizManager()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.single_attempt:
            self.exam_paper = True
        if not (0 <= self.pass_mark <= 100):
            raise ValidationError("Pass mark must be between 0 and 100.")
        super().save(*args, **kwargs)

    def get_questions(self):
        """Return all questions for this quiz, including subclasses."""
        return self.question_set.all().select_subclasses()

    def get_absolute_url(self):
        return reverse("quiz_index", kwargs={"course_id": self.course.id})


# ========================================================
# Sitting & Manager
# ========================================================
class SittingManager(models.Manager):
    """Custom manager for Sitting model."""
    def new_sitting(self, employee, quiz, course):
        questions = quiz.get_questions()
        if quiz.random_order:
            questions = questions.order_by("?")

        ids = [q.id for q in questions]
        if not ids:
            raise ImproperlyConfigured("Quiz has no questions.")

        q_string = ",".join(map(str, ids)) + ","
        return self.create(
            employee=employee,
            quiz=quiz,
            course=course,
            question_order=q_string,
            question_list=q_string,
            incorrect_questions="",
            current_score=0,
            complete=False,
            user_answers="{}",
        )

    def user_sitting(self, employee, quiz, course):
        """Return an existing incomplete sitting or create a new one."""
        if quiz.single_attempt and self.filter(employee=employee, quiz=quiz, complete=True).exists():
            return None
        try:
            return self.get(employee=employee, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            return self.new_sitting(employee, quiz, course)


class Sitting(models.Model):
    """Tracks a user's progress for a specific quiz."""
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    question_order = models.CharField(max_length=1024)
    question_list = models.CharField(max_length=1024)
    incorrect_questions = models.CharField(max_length=1024, blank=True)

    current_score = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)
    user_answers = models.TextField(default="{}")

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)

    objects = SittingManager()

    class Meta:
        ordering = ["-end"]

    def __str__(self):
        return f"{self.employee} - {self.quiz}"

    # ---------------- Score & Completion ----------------
    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    def mark_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def mark_quiz_complete(self):
        self.mark_complete()

    # ---------------- User Answers ----------------
    def add_user_answer(self, question, answer):
        data = json.loads(self.user_answers or "{}")
        data[str(question.id)] = answer
        self.user_answers = json.dumps(data)
        self.save()

    # ---------------- Question Handling ----------------
    def get_question_ids(self):
        """Return remaining question IDs as a list of integers."""
        if self.question_list:
            return [int(q) for q in self.question_list.strip(",").split(",") if q]
        return []

    def get_first_question(self):
        ids = self.get_question_ids()
        if ids:
            return Question.objects.get(id=ids[0])
        return None

    def remove_first_question(self):
        ids = self.get_question_ids()
        if ids:
            ids.pop(0)
            self.question_list = ",".join(map(str, ids)) + ("," if ids else "")
            self.save()

    def add_incorrect_question(self, question):
        ids = self.incorrect_questions.strip(",").split(",") if self.incorrect_questions else []
        ids.append(str(question.id))
        self.incorrect_questions = ",".join(ids) + ","
        self.save()

    # ---------------- Progress ----------------
    @property
    def progress(self):
        total = self.quiz.get_questions().count()
        answered = total - len(self.get_question_ids())
        return {
            "answered": answered,
            "total": total,
            "percent": int((answered / total) * 100) if total else 0,
        }

    def get_current_score(self):
        return self.current_score

    def get_max_score(self):
        return self.quiz.get_questions().count()

    def get_percent_correct(self):
        total = self.get_max_score()
        return int((self.current_score / total) * 100) if total else 0

    def get_incorrect_questions(self):
        ids = [int(i) for i in self.incorrect_questions.strip(",").split(",") if i]
        return Question.objects.filter(id__in=ids)


# ========================================================
# Question & Subclasses
# ========================================================
class Question(models.Model):
    """Base question model with MPTT for multiple question types."""
    quiz = models.ManyToManyField(Quiz, blank=True)
    content = models.CharField(max_length=1000)
    explanation = models.TextField(blank=True)

    objects = InheritanceManager()

    def __str__(self):
        return self.content


class MCQuestion(Question):
    """Multiple choice question model."""
    choice_order = models.CharField(max_length=30, choices=CHOICE_ORDER_OPTIONS, blank=True)

    def check_if_correct(self, guess):
        try:
            return Choice.objects.get(id=int(guess)).correct
        except Choice.DoesNotExist:
            return False

    def get_choices(self):
        qs = Choice.objects.filter(question=self)
        if self.choice_order == "random":
            return qs.order_by("?")
        if self.choice_order == "content":
            return qs.order_by("choice_text")
        return qs

    def get_choices_list(self):
        return [(c.id, c.choice_text) for c in self.get_choices()]


class Choice(models.Model):
    """Choices for multiple choice questions."""
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=1000)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class EssayQuestion(Question):
    """Essay questions require manual grading."""
    def check_if_correct(self, guess):
        return False