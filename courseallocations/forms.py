from django import forms
from django.contrib.auth import get_user_model
from .models import CourseAllocation
from course.models import Course  # assuming Course model exists

User = get_user_model()


# ==============================
# Create Form: Multi-employee selection
# ==============================

class CourseAllocationCreateForm(forms.ModelForm):
    # Multiple employee selection
    employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().order_by('username'),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 6  # height of the multi-select box
        }),
        required=True,
        label="Select Employees"
    )

    class Meta:
        model = CourseAllocation
        fields = ['employees', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),  # checkbox for multiple courses
        }
        labels = {
            'courses': 'Select Courses'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the employee dropdown labels
        self.fields['employees'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})".strip()

    # Validation: at least one course must be selected
    def clean_courses(self):
        courses = self.cleaned_data.get('courses')
        if not courses:
            raise forms.ValidationError("Please select at least one course.")
        return courses

    # Validation: at least one employee must be selected
    def clean_employees(self):
        employees = self.cleaned_data.get('employees')
        if not employees:
            raise forms.ValidationError("Please select at least one employee.")
        return employees

# ==============================
# Edit Form: Single-employee selection
# ==============================

class CourseAllocationEditForm(forms.ModelForm):
    # -----------------------------
    # Employee (readonly)
    # -----------------------------
    employee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,   # ⚠️ IMPORTANT: prevent validation error when disabled
        label="Employee"
    )

    class Meta:
        model = CourseAllocation
        fields = ['employee', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'courses': 'Select Courses'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # ✅ Show only current employee
            self.fields['employee'].queryset = User.objects.filter(pk=self.instance.employee.pk)

            # ✅ Set initial values
            self.fields['employee'].initial = self.instance.employee
            self.fields['courses'].initial = self.instance.courses.all()

            # ✅ Disable employee field (readonly)
            self.fields['employee'].disabled = True

        # ✅ Better display label
        self.fields['employee'].label_from_instance = lambda obj: (
            f"{obj.username} ({obj.first_name} {obj.last_name})".strip()
        )

    # -----------------------------
    # FIX: Preserve employee value when field is disabled
    # -----------------------------
    def clean_employee(self):
        return self.instance.employee

    # -----------------------------
    # Validation: ensure courses selected
    # -----------------------------
    def clean_courses(self):
        courses = self.cleaned_data.get('courses')
        if not courses:
            raise forms.ValidationError("Please select at least one course.")
        return courses