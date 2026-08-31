# ========================================================
# Django Core Imports
# ========================================================
from django import forms
from django.forms import RadioSelect, Textarea
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory

# ========================================================
# Local App Imports
# ========================================================
from .models import Question, Quiz, MCQuestion, Choice


# ========================================================
# Essay Question Form
# ========================================================
class EssayForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)  # Keep consistency with other forms
        super().__init__(*args, **kwargs)

        self.fields["answers"] = forms.CharField(
            label=_("Your answer"),
            widget=Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your answer here..."
            }),
            required=True,
        )


# ========================================================
# Quiz Creation / Update Form
# ========================================================
class QuizAddForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(_("Questions"), is_stacked=False),
    )

    class Meta:
        model = Quiz
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["questions"].initial = self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super().save(commit=False)
        if commit:
            quiz.save()

        if "questions" in self.cleaned_data:
            quiz.question_set.set(self.cleaned_data["questions"])

        return quiz


# ========================================================
# Multiple Choice Question Form
# ========================================================
class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# ========================================================
# MCQuestion Choice Formset Validation
# ========================================================
class MCQuestionFormSetBase(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Keep only valid (not deleted) forms
        valid_forms = [form for form in self.forms if form.cleaned_data and not form.cleaned_data.get("DELETE", False)]

        # Minimum 2 choices required
        if len(valid_forms) < 2:
            raise forms.ValidationError(_("At least 2 choices are required."))

        # Ensure exactly one correct answer
        correct_count = sum(1 for form in valid_forms if form.cleaned_data.get("correct", False))
        if correct_count == 0:
            raise forms.ValidationError(_("One correct answer is required."))
        if correct_count > 1:
            raise forms.ValidationError(_("Only one correct answer is allowed."))


# ========================================================
# Inline Formset for MCQuestion Choices
# ========================================================
MCQuestionFormSet = inlineformset_factory(
    MCQuestion,
    Choice,
    fields=("choice_text", "correct"),
    extra=4,
    can_delete=True,
    formset=MCQuestionFormSetBase,
)


# ========================================================
# Student Quiz Question Form (Used During Quiz)
# ========================================================
class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        super().__init__(*args, **kwargs)

        # Default empty choices
        choices = []

        # Populate choices if question has a choice list
        if question and hasattr(question, "get_choices_list"):
            choices = question.get_choices_list()

        self.fields["answers"] = forms.ChoiceField(
            label=_("Select an answer"),
            choices=choices,
            widget=RadioSelect,
            required=True,
        )