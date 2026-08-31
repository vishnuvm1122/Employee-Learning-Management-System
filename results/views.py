from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.db.models import Sum

from django.views.generic import ListView, DetailView, TemplateView

from quiz.models import *
from course.models import *
from courseallocations.models import *

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor



@method_decorator(login_required, name="dispatch")
class ResultView(TemplateView):

    template_name = "results/result.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.request.user

        # -----------------------------
        # QUIZ DATA
        # -----------------------------
        quizzes = Sitting.objects.filter(
            complete=True
        ).select_related(
            "quiz",
            "course",
            "employee"
        )

        # ✅ Normal user only own quiz
        if not user.is_superuser:
            quizzes = quizzes.filter(employee=user)

        # -----------------------------
        # COURSE ALLOCATION
        # -----------------------------
        allocations = CourseAllocation.objects.select_related(
            'courses',
            'employee'
        )

        # ✅ Restrict normal user
        if not user.is_superuser:
            allocations = allocations.filter(employee=user)

        allocation_data = []

        for alloc in allocations:

            total_course_seconds = 0
            watched_seconds = 0
            courses_detail = []

            # ✅ Single course
            course = alloc.courses

            # -----------------------------
            # VIDEO CALCULATION
            # -----------------------------
            course_total_sec = (
                course.videos.aggregate(
                    total=Sum('duration')
                )['total'] or 0
            )

            course_watched_sec = (
                VideoWatchProgress.objects.filter(
                    employee=alloc.employee,
                    video__course=course
                ).aggregate(
                    total=Sum('watched_duration')
                )['total'] or 0
            )

            total_course_seconds += course_total_sec
            watched_seconds += course_watched_sec

            progress_percent = round(
                (course_watched_sec / course_total_sec) * 100,
                2
            ) if course_total_sec else 0

            # -----------------------------
            # QUIZ CALCULATION
            # -----------------------------
            course_quizzes = quizzes.filter(
                employee=alloc.employee,
                course=course
            )

            best_quiz = None
            best_score = 0
            obtained_marks = 0
            total_marks = 0

            for q in course_quizzes:

                percent = q.get_percent_correct()

                total_marks += q.get_max_score()
                obtained_marks += q.get_current_score()

                if percent > best_score:
                    best_score = percent
                    best_quiz = q

            # -----------------------------
            # APPEND COURSE
            # -----------------------------
            courses_detail.append({
                'course': course,
                'total_hours': round(course_total_sec / 3600, 2),
                'watched_hours': round(course_watched_sec / 3600, 2),
                'progress_percent': progress_percent,
                'best_quiz': best_quiz,
                'best_score': best_score,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
            })

            # -----------------------------
            # OVERALL PROGRESS
            # -----------------------------
            overall_progress = round(
                (watched_seconds / total_course_seconds) * 100,
                2
            ) if total_course_seconds else 0

            allocation_data.append({
                'allocation': alloc,
                'total_course_hours': round(total_course_seconds / 3600, 2),
                'watched_hours': round(watched_seconds / 3600, 2),
                'overall_progress_percent': overall_progress,
                'courses_detail': courses_detail
            })

        context['allocation_data'] = allocation_data
        context['title'] = "Results Dashboard"

        return context




User = get_user_model()

# -------------------------
# 🎯 Certificate Border
# -------------------------
def draw_background(canvas, doc):
    width, height = landscape(A4)

    # Background
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, width, height, fill=1)

    # -------------------------
    # SMOOTH GRADIENT STRIP
    # -------------------------
    start_color = HexColor("#2563eb")
    end_color = HexColor("#1e3a8a")

    steps = 100  # more steps = smoother gradient
    strip_width = 30

    for i in range(steps):
        ratio = i / steps

        r = start_color.red + (end_color.red - start_color.red) * ratio
        g = start_color.green + (end_color.green - start_color.green) * ratio
        b = start_color.blue + (end_color.blue - start_color.blue) * ratio

        canvas.setFillColorRGB(r, g, b)

        x = (strip_width / steps) * i
        canvas.rect(x, 0, strip_width / steps + 1, height, fill=1, stroke=0)


# -------------------------
#  Certificate Generator
# -------------------------
def download_certificate(request, user_id, course_id):
    user = get_object_or_404(User, id=user_id)
    course = get_object_or_404(Course, id=course_id)

    # =====================================================
    # GET LATEST COMPLETED SITTING
    # =====================================================
    sitting = Sitting.objects.filter(
        employee=user,
        course=course,
        complete=True
    ).order_by("-end").first()

    # =====================================================
    # RESPONSE
    # =====================================================
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="certificate_{user.username}.pdf"'
    )

    # =====================================================
    # DOCUMENT
    # =====================================================
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        leftMargin=80,
        rightMargin=80,
        topMargin=40,
        bottomMargin=40
    )

    # =====================================================
    # STYLES
    # =====================================================
    title_style = ParagraphStyle(
        name="Title",
        fontSize=35,
        leading=44,
        alignment=TA_LEFT,
        textColor=HexColor("#0f172a"),
        spaceAfter=10
    )

    subtitle_style_top = ParagraphStyle(
        name="SubtitleTop",
        fontSize=16,
        alignment=TA_LEFT,
        textColor=HexColor("#64748b"),
        spaceAfter=10
    )

    subtitle_style_bottom = ParagraphStyle(
        name="SubtitleBottom",
        fontSize=16,
        alignment=TA_LEFT,
        textColor=HexColor("#64748b"),
        spaceAfter=10,
        spaceBefore=20
    )

    subtitle_style_center = ParagraphStyle(
        name="SubtitleCenter",
        fontName="Helvetica-Oblique",
        fontSize=8,
        alignment=TA_CENTER,
        textColor=HexColor("#64748b")
    )

    name_style = ParagraphStyle(
        name="Name",
        fontSize=33,
        alignment=TA_LEFT,
        textColor=HexColor("#2563eb"),
        spaceAfter=20
    )

    course_style = ParagraphStyle(
        name="Course",
        fontSize=24,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceAfter=20
    )

    label_style = ParagraphStyle(
        name="Label",
        fontSize=13,
        textColor=HexColor("#64748b"),
        fontName="Helvetica-Bold"
    )

    value_style = ParagraphStyle(
        name="Value",
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=HexColor("#0f172a")
    )

    # =====================================================
    # LOGOS
    # =====================================================
    try:
        left_logo = Image(
            "static/certificate/eka_logo.png",
            width=7.5 * cm,
            height=2.5 * cm
        )
    except:
        left_logo = Spacer(1, 60)

    try:
        right_logo = Image(
            "static/certificate/right_logo.png",
            width=8 * cm,
            height=1* cm
        )
    except:
        right_logo = Spacer(1, 60)

    logo_table = Table(
        [[left_logo, right_logo]],
        colWidths=[doc.width * 0.55, doc.width * 0.45]
    )

    logo_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),

        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),

        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    # =====================================================
    # DATE + VERIFICATION
    # =====================================================
    completion_date = (
        sitting.end.strftime("%d %b %Y")
        if sitting and sitting.end else "Not Completed"
    )

    details_data = [
        [
            Paragraph("<b>COMPLETION DATE</b>", label_style),
            Paragraph("<b>VERIFICATION ID</b>", label_style),
        ],
        [
            Paragraph(completion_date, value_style),
            Paragraph(f"EKA-LMS-{user.id}-{course.id}", value_style),
        ]
    ]

    details_table = Table(
        details_data,
        colWidths=[doc.width * 0.30, doc.width * 0.30]
    )

    # =====================================================
    # LEFT COLUMN
    # =====================================================
    left_column = [
        Paragraph("<b>CERTIFICATE OF</b>", title_style),
        Paragraph("<b>COMPLETION</b>", title_style),
        Spacer(1, 20),

        Paragraph(
            "This Certificate is Presented to",
            subtitle_style_top
        ),

        Paragraph(
            f"<b>{user.get_full_name}</b>",
            name_style
        ),

        Paragraph(
            "For successful completion of training in",
            subtitle_style_bottom
        ),

        Paragraph(
            f"<b>{course.title}</b>",
            course_style
        ),

        Spacer(1, 80),
        details_table
    ]

    # =====================================================
    # RIGHT COLUMN
    # =====================================================
    try:
        badge = Image(
            "static/certificate/official_badge.png",
            width=9 * cm,
            height=9 * cm
        )
    except:
        badge = Spacer(1, 200)

    right_column = Table([
        [Spacer(1, 5)],
        [badge],
        [Spacer(1, 10)],
        [Paragraph(
            "Digital signature verified via",
            subtitle_style_center
        )],
        [Paragraph(
            "EKA Secure Servers",
            subtitle_style_center
        )],
    ])

    right_column.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    # =====================================================
    # MAIN TABLE
    # =====================================================
    main_table = Table(
        [[left_column, right_column]],
        colWidths=[doc.width * 0.75, doc.width * 0.25]
    )

    main_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    # =====================================================
    # BUILD PDF
    # =====================================================
    elements = [
        logo_table,
        Spacer(1, 20),
        main_table
    ]

    doc.build(elements, onFirstPage=draw_background)

    return response