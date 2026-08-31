from django import forms
from .models import (
    Program,
    Course,
    CourseDocument,
    CourseVideo,
)
from django.core.exceptions import ValidationError


# ========================
# PROGRAM FORM
# ========================
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'summary', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Program title'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Program description'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


# ========================
# COURSE FORM
# ========================
class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title",
                "code",
                "summary",
                "duration",
                "level",
                "photo",
                )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["code"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["duration"].widget.attrs.update({"class": "form-control"})
        self.fields["level"].widget.attrs.update({"class": "form-control"})
        model = Course
        fields = [
            'title',
            'code',
            'photo',
            'duration',
            'summary',
            'program',
            'level',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course title'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course code'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Course description'
            }),
            'program': forms.Select(attrs={
                'class': 'form-select'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            }),
        }




# ========================
# FILE UPLOAD FORM
# ========================
class UploadFile(forms.ModelForm):
    class Meta:
        model = CourseDocument
        fields = ['title','file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document title'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


# ========================
# VIDEO UPLOAD FORM
# ========================
class UploadVideo(forms.ModelForm):
    class Meta:
        model = CourseVideo
        # Removed 'course' field
        fields = ['no', 'title', 'video', 'summary']
        widgets = {
            'no': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Video sequence number'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Video title'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Video description'
            }),
        }

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            # Max size 200MB
            if video.size > 1024 * 1024 * 1024:
                raise ValidationError("Max file size is 1GB.")
            
            # Allowed extensions
            valid_extensions = ['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi']
            ext = video.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError(
                    f"Unsupported file extension. Allowed: {', '.join(valid_extensions)}"
                )
        return video

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()  # Save video first
            
            # Generate thumbnail after saving
            if instance.video:
                instance.generate_thumbnail()
                instance.save(update_fields=['thumbnail'])

        return instance




# ========================
# SEARCH FORM
# ========================
class CourseSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search courses...'
        })
    )