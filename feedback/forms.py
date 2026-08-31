from django import forms
from .models import Feedback


# =========================================================
# ⭐ MAIN FEEDBACK FORM (ADD / EDIT)
# =========================================================
class FeedbackForm(forms.ModelForm):
    """
    Feedback form with star rating and comment.
    """

    # =====================================================
    # RATING CHOICES
    # =====================================================
    RATING_CHOICES = [
        (5, "⭐⭐⭐⭐⭐ Excellent"),
        (4, "⭐⭐⭐⭐ Very Good"),
        (3, "⭐⭐⭐ Good"),
        (2, "⭐⭐ Average"),
        (1, "⭐ Poor"),
    ]

    # =====================================================
    # RATING FIELD
    # =====================================================
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input"
            }
        ),
        label="Rating",
    )

    # =====================================================
    # COMMENT FIELD
    # =====================================================
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": (
                    "Write your feedback (optional)..."
                ),
            }
        ),
        label="Comment",
    )

    # =====================================================
    # META
    # =====================================================
    class Meta:
        model = Feedback
        fields = [
            "rating",
            "comment",
        ]

    # =====================================================
    # CLEAN RATING
    # =====================================================
    def clean_rating(self):

        rating = self.cleaned_data.get("rating")

        if not rating:

            raise forms.ValidationError(
                "Please select a rating."
            )

        try:
            rating = int(rating)

        except (TypeError, ValueError):

            raise forms.ValidationError(
                "Invalid rating value."
            )

        if rating < 1 or rating > 5:

            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

    # =====================================================
    # CLEAN COMMENT
    # =====================================================
    def clean_comment(self):

        comment = self.cleaned_data.get(
            "comment",
            ""
        ).strip()

        # Optional comment validation
        if comment and len(comment) < 3:

            raise forms.ValidationError(
                "Comment is too short "
                "(minimum 3 characters)."
            )

        return comment

        
# =========================================================
# 💬 ADMIN REPLY FORM (SUPERUSER)
# =========================================================
class ReplyForm(forms.ModelForm):

    reply = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Write instructor reply..."
        })
    )

    class Meta:
        model = Feedback
        fields = ["reply"]

    def clean_reply(self):
        reply = self.cleaned_data.get("reply")

        if not reply or len(reply.strip()) == 0:
            raise forms.ValidationError("Reply cannot be empty")

        return reply