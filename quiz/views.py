# ========================================================
# Django Core Imports
# ========================================================
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    ListView,
    FormView,
)
import json

# ========================================================
# Local App Imports
# ========================================================
from course.models import Course
from .models import Quiz, Sitting, Question, MCQuestion, EssayQuestion
from .forms import QuizAddForm, MCQuestionForm, MCQuestionFormSet, QuestionForm, EssayForm
from django.utils.translation import gettext as _


# ========================================================
# Quiz Views
# ========================================================
@method_decorator(login_required, name="dispatch")
class QuizCreateView(CreateView):
    model = Quiz
    form_class = QuizAddForm
    template_name = "quiz/quiz_form.html"

    def get_initial(self):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        return {"course": course}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, id=self.kwargs["course_id"])
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        form.instance.course = course
        with transaction.atomic():
            self.object = form.save()
        return redirect("mc_create", quiz_id=self.object.id)


@method_decorator(login_required, name="dispatch")
class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizAddForm
    template_name = "quiz/quiz_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, id=self.kwargs["course_id"])
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
        return redirect("quiz_index", course_id=self.kwargs["course_id"])


@login_required
def quiz_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizzes = Quiz.objects.filter(course=course).order_by("-timestamp")
    return render(request, "quiz/quiz_list.html", {"quizzes": quizzes, "course": course})


@login_required
def quiz_delete(request, course_id, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    messages.success(request, "Quiz successfully deleted.")
    return redirect("quiz_index", course_id=course_id)


# ========================================================
# Multiple Choice Question Views
# ========================================================
@method_decorator(login_required, name="dispatch")
class MCQuestionCreate(CreateView):
    model = MCQuestion
    form_class = MCQuestionForm
    template_name = "quiz/mcquestion_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = get_object_or_404(Quiz, id=self.kwargs["quiz_id"])
        context["quiz_obj"] = quiz
        context["course"] = quiz.course
        context["quiz_questions_count"] = Question.objects.filter(quiz=quiz).count()
        context["formset"] = MCQuestionFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.save()
                quiz = get_object_or_404(Quiz, id=self.kwargs["quiz_id"])
                self.object.quiz.add(quiz)
                formset.instance = self.object
                formset.save()

            if "another" in self.request.POST:
                return redirect("mc_create", quiz_id=self.kwargs["quiz_id"])
            return redirect("quiz_index", course_id=quiz.course.id)

        return self.form_invalid(form)


# ========================================================
# Quiz Progress & Marking Views
# ========================================================
@method_decorator(login_required, name="dispatch")
class QuizMarkingList(ListView):
    model = Sitting
    template_name = "quiz/quiz_marking_list.html"

    def get_queryset(self):
        qs = Sitting.objects.filter(complete=True)
        if not self.request.user.is_superuser:
            qs = qs.filter(employee=self.request.user)

        quiz_filter = self.request.GET.get("quiz_filter")
        if quiz_filter:
            qs = qs.filter(quiz__title__icontains=quiz_filter)

        user_filter = self.request.GET.get("user_filter")
        if user_filter:
            qs = qs.filter(employee__username__icontains=user_filter)

        return qs.order_by("-end")



@method_decorator(login_required, name="dispatch")
class QuizMarkingDetail(DetailView):

    model = Sitting

    template_name = "quiz/quiz_marking_detail.html"

    # =====================================================
    # POST METHOD
    # =====================================================

    def post(self, request, *args, **kwargs):

        sitting = self.get_object()

        question_id = request.POST.get("qid")

        if question_id:

            question = get_object_or_404(
                Question,
                id=int(question_id)
            )

            incorrect_ids = [
                str(i)
                for i in sitting.incorrect_questions.strip(",").split(",")
                if i
            ]

            # TOGGLE QUESTION STATUS

            if str(question.id) in incorrect_ids:

                incorrect_ids.remove(str(question.id))

            else:

                incorrect_ids.append(str(question.id))

            sitting.incorrect_questions = (
                ",".join(incorrect_ids) + ("," if incorrect_ids else "")
            )

            sitting.save()

        return redirect(
            "quiz_marking_detail",
            pk=sitting.id
        )

    # =====================================================
    # CONTEXT DATA
    # =====================================================

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        sitting = self.object

        questions_qs = (
            sitting.quiz.get_questions()
            .select_subclasses()
        )

        # =====================================================
        # LOAD USER ANSWERS JSON
        # =====================================================

        try:

            user_answers = json.loads(
                sitting.user_answers or "{}"
            )

        except Exception:

            user_answers = {}

        # =====================================================
        # INCORRECT QUESTION IDS
        # =====================================================

        incorrect_qs_ids = [
            q.id
            for q in sitting.get_incorrect_questions()
        ]

        question_list = []

        correct_count = 0

        # =====================================================
        # LOOP QUESTIONS
        # =====================================================

        for q in questions_qs:

            raw_user_answer = user_answers.get(
                str(q.id),
                None
            )

            user_answer_text = _("No answer submitted")

            correct_answer_text = _("N/A")

            # =====================================================
            # MCQ QUESTIONS
            # =====================================================

            if isinstance(q, MCQuestion):

                # -----------------------------------------
                # CORRECT ANSWERS
                # -----------------------------------------

                correct_choices = q.get_choices().filter(
                    correct=True
                )

                correct_answer_text = ", ".join(
                    [
                        choice.choice_text
                        for choice in correct_choices
                    ]
                )

                # -----------------------------------------
                # USER ANSWERS
                # -----------------------------------------

                if raw_user_answer:

                    try:

                        # =====================================
                        # SINGLE ANSWER
                        # =====================================

                        if isinstance(raw_user_answer, (str, int)):

                            selected_choice = (
                                q.get_choices()
                                .filter(id=int(raw_user_answer))
                                .first()
                            )

                            if selected_choice:

                                user_answer_text = (
                                    selected_choice.choice_text
                                )

                            else:

                                user_answer_text = _(
                                    "Answer not found"
                                )

                        # =====================================
                        # MULTIPLE ANSWERS
                        # =====================================

                        elif isinstance(raw_user_answer, list):

                            answer_ids = []

                            for ans in raw_user_answer:

                                try:

                                    answer_ids.append(
                                        int(ans)
                                    )

                                except:

                                    pass

                            selected_choices = (
                                q.get_choices()
                                .filter(id__in=answer_ids)
                            )

                            user_answer_text = ", ".join(
                                [
                                    choice.choice_text
                                    for choice in selected_choices
                                ]
                            )

                        # =====================================
                        # UNKNOWN FORMAT
                        # =====================================

                        else:

                            user_answer_text = str(
                                raw_user_answer
                            )

                    except Exception:

                        user_answer_text = _(
                            "Invalid answer"
                        )

            # =====================================================
            # TEXT / ESSAY QUESTIONS
            # =====================================================

            else:

                if raw_user_answer:

                    user_answer_text = raw_user_answer

                correct_answer_text = _(
                    "Manual grading required"
                )

            # =====================================================
            # QUESTION STATUS
            # =====================================================

            is_correct = q.id not in incorrect_qs_ids

            if is_correct:

                correct_count += 1

            # =====================================================
            # APPEND QUESTION
            # =====================================================

            question_list.append({

                "question": q,

                "user_answer": user_answer_text,

                "correct_answer": correct_answer_text,

                "is_correct": is_correct,

            })

        # =====================================================
        # CONTEXT UPDATE
        # =====================================================

        context.update({

            "questions": question_list,

            "total_questions": questions_qs.count(),

            "correct_count": correct_count,

            "wrong_count": (
                questions_qs.count() - correct_count
            ),

        })

        return context
        
        

# ========================================================
# Quiz Taking View
# ========================================================
@method_decorator(login_required, name="dispatch")
class QuizTake(FormView):
    form_class = QuestionForm
    template_name = "quiz/question.html"
    result_template_name = "quiz/result.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs["quiz_id"], course=self.course)

        if not Question.objects.filter(quiz=self.quiz).exists():
            messages.warning(request, "No questions available.")
            return redirect("quiz_index", course_id=self.course.pk)

        self.sitting = Sitting.objects.user_sitting(request.user, self.quiz, self.course)
        if not self.sitting:
            messages.info(request, "You already completed this quiz.")
            return redirect("quiz_index", course_id=self.course.pk)

        self.question = self.sitting.get_first_question()
        if self.question:
            self.question = Question.objects.get_subclass(id=self.question.id)

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "question": self.question}

    def form_valid(self, form):
        guess = form.cleaned_data["answers"]
        is_correct = hasattr(self.question, "check_if_correct") and self.question.check_if_correct(guess)

        if is_correct:
            self.sitting.add_to_score(1)
        else:
            self.sitting.add_incorrect_question(self.question)

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

        if not self.sitting.get_first_question():
            return self.final_result_user()

        return redirect(self.request.path)

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "question": self.question, "quiz": self.quiz, "course": self.course}

    def final_result_user(self):
        self.sitting.mark_quiz_complete()
        questions = self.quiz.get_questions()
        user_answers = json.loads(self.sitting.user_answers or "{}")
        for q in questions:
            q.user_answer = user_answers.get(str(q.id))

        score = self.sitting.get_current_score()
        total = self.sitting.get_max_score()
        percent = int((score / total) * 100) if total else 0

        return render(self.request, self.result_template_name, {
            "quiz": self.quiz,
            "score": score,
            "max_score": total,
            "percent": percent,
            "questions": questions,
            "course": self.course,
        })