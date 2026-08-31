from django.urls import path
from . import views

urlpatterns = [
    # ⭐ User Feedback
    path("course/feedback/add/", views.add_feedback, name="add_feedback"),
    path("course/<int:pk>/feedback/edit/", views.edit_feedback, name="edit_feedback"),
    path("course/<int:pk>/feedback/delete/", views.delete_feedback, name="delete_feedback"),

    # 🛠 Admin Reply
    path("feedback/<int:pk>/reply/", views.reply_feedback, name="reply_feedback"),

    # 📋 All Feedbacks
    path("feedback/all/", views.feedback_list, name="feedback_list"),
]