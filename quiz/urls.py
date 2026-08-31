from django.urls import path
from .views import (
    quiz_list,
    QuizMarkingList,
    QuizMarkingDetail,
    QuizTake,
    QuizCreateView,
    QuizUpdateView,
    quiz_delete,
    MCQuestionCreate,
)

urlpatterns = [

    # =========================
    # 📚 COURSE QUIZ LIST
    # =========================
    path("<int:course_id>/quizzes/", quiz_list, name="quiz_index"),

    # =========================
    # 📊 USER PROGRESS
    # =========================

    # =========================
    # 📝 QUIZ MARKING
    # =========================
    path("marking/", QuizMarkingList.as_view(), name="quiz_marking"),
    path("marking/<int:pk>/", QuizMarkingDetail.as_view(), name="quiz_marking_detail"),

    # =========================
    # ▶️ TAKE QUIZ
    # =========================
    path("quiz/<int:course_id>/<int:quiz_id>/take/", QuizTake.as_view(), name="quiz_take"),

    # =========================
    # ➕ CREATE QUIZ
    # =========================
    path("<int:course_id>/quiz/add/", QuizCreateView.as_view(), name="quiz_create"),

    # =========================
    # ✏️ UPDATE QUIZ
    # =========================
    path("<int:course_id>/quiz/<int:pk>/edit/", QuizUpdateView.as_view(), name="quiz_update"),

    # =========================
    # 🗑 DELETE QUIZ
    # =========================
    path("<int:course_id>/quiz/<int:pk>/delete/", quiz_delete, name="quiz_delete"),

    # =========================
    # ❓ MCQ QUESTIONS
    # =========================
    path("quiz/<int:quiz_id>/mcq/add/", MCQuestionCreate.as_view(), name="mc_create"),
]

