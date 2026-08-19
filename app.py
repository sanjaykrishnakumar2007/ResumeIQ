from flask import Flask, render_template, request, send_file
import os
from io import BytesIO

from PyPDF2 import PdfReader

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from analyzer import analyze_resume


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# RESUME UPLOAD + ANALYSIS
# ============================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_resume():

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if "resume" not in request.files:

        return """
        <h2>No resume uploaded.</h2>
        <a href="/">Go Back</a>
        """, 400


    file = request.files["resume"]


    if file.filename == "":

        return """
        <h2>No resume selected.</h2>
        <a href="/">Go Back</a>
        """, 400


    # --------------------------------------------------------
    # CHECK PDF
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        return """
        <h2>Invalid file type.</h2>

        <p>
        Please upload a PDF resume.
        </p>

        <a href="/">Go Back</a>
        """, 400


    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    # --------------------------------------------------------
    # SAVE FILE
    # --------------------------------------------------------

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)


    # --------------------------------------------------------
    # READ PDF
    # --------------------------------------------------------

    try:

        reader = PdfReader(filepath)

        text = ""


        for page in reader.pages:

            page_text = page.extract_text()


            if page_text:

                text += page_text + "\n"


    except Exception as e:

        return f"""
        <h2>Error reading PDF</h2>

        <p>
        {e}
        </p>

        <a href="/">
        Go Back
        </a>
        """, 500


    # --------------------------------------------------------
    # CHECK TEXT
    # --------------------------------------------------------

    if not text.strip():

        return """
        <div style="
            font-family: Arial;
            max-width: 600px;
            margin: 100px auto;
            text-align: center;
        ">

            <h2>
                Unable to extract text from this PDF
            </h2>

            <p>
                Please upload a text-based PDF resume.
            </p>

            <br>

            <a href="/">
                ← Go Back
            </a>

        </div>
        """, 400


    # --------------------------------------------------------
    # ANALYZE RESUME
    # --------------------------------------------------------

    try:

        analysis = analyze_resume(
            text,
            job_description
        )

    except Exception as e:

        return f"""
        <div style="
            font-family: Arial;
            max-width: 700px;
            margin: 80px auto;
            text-align: center;
        ">

            <h2>
                Resume Analysis Error
            </h2>

            <p>
                {e}
            </p>

            <br>

            <a href="/">
                ← Go Back
            </a>

        </div>
        """, 500


    # --------------------------------------------------------
    # SHOW RESULT PAGE
    # --------------------------------------------------------

    return render_template(

        "result.html",

        text=text,

        job_description=job_description,

        **analysis

    )


# ============================================================
# DOWNLOAD PDF REPORT
# ============================================================

@app.route(
    "/download-report",
    methods=["POST"]
)
def download_report():

    # --------------------------------------------------------
    # GET BASIC DATA
    # --------------------------------------------------------

    overall_score = request.form.get(
        "overall_score",
        "0"
    )

    ats_score = request.form.get(
        "ats_score",
        "0"
    )

    ats_status = request.form.get(
        "ats_status",
        ""
    )

    job_match_score = request.form.get(
        "job_match_score",
        ""
    )

    job_match_status = request.form.get(
        "job_match_status",
        ""
    )

    nlp_score = request.form.get(
        "nlp_score",
        ""
    )

    resume_text = request.form.get(
        "resume_text",
        ""
    )

    job_description = request.form.get(
        "job_description",
        ""
    )


    # --------------------------------------------------------
    # GET LIST DATA
    # --------------------------------------------------------

    skills = request.form.get(
        "skills",
        ""
    ).split("|")


    matching_skills = request.form.get(
        "matching_skills",
        ""
    ).split("|")


    missing_skills = request.form.get(
        "missing_skills",
        ""
    ).split("|")


    suggestions = request.form.get(
        "suggestions",
        ""
    ).split("|")


    job_roles = request.form.get(
        "job_roles",
        ""
    ).split("|")


    # --------------------------------------------------------
    # REMOVE EMPTY VALUES
    # --------------------------------------------------------

    skills = [
        item for item in skills
        if item.strip()
    ]


    matching_skills = [
        item for item in matching_skills
        if item.strip()
    ]


    missing_skills = [
        item for item in missing_skills
        if item.strip()
    ]


    suggestions = [
        item for item in suggestions
        if item.strip()
    ]


    job_roles = [
        item for item in job_roles
        if item.strip()
    ]


    # --------------------------------------------------------
    # CREATE PDF MEMORY BUFFER
    # --------------------------------------------------------

    buffer = BytesIO()


    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=40

    )


    # --------------------------------------------------------
    # PDF STYLES
    # --------------------------------------------------------

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "TitleStyle",

        parent=styles["Title"],

        fontSize=25,

        leading=30,

        alignment=TA_CENTER,

        spaceAfter=15

    )


    subtitle_style = ParagraphStyle(

        "SubtitleStyle",

        parent=styles["Normal"],

        fontSize=11,

        leading=16,

        alignment=TA_CENTER,

        textColor=colors.grey,

        spaceAfter=25

    )


    heading_style = ParagraphStyle(

        "HeadingStyle",

        parent=styles["Heading2"],

        fontSize=16,

        leading=20,

        spaceBefore=15,

        spaceAfter=10

    )


    normal_style = ParagraphStyle(

        "NormalStyle",

        parent=styles["Normal"],

        fontSize=10,

        leading=15,

        spaceAfter=6

    )


    # --------------------------------------------------------
    # STORY
    # --------------------------------------------------------

    story = []


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    story.append(

        Paragraph(
            "ResumeIQ",
            title_style
        )

    )


    story.append(

        Paragraph(
            "AI Resume Analysis Report",
            subtitle_style
        )

    )


    # --------------------------------------------------------
    # SCORE SECTION
    # --------------------------------------------------------

    story.append(

        Paragraph(
            "Resume Scores",
            heading_style
        )

    )


    score_data = [

        [
            "Overall Score",
            "ATS Score",
            "Job Match"
        ],

        [

            f"{overall_score}/100",

            f"{ats_score}%",

            (
                f"{job_match_score}%"
                if job_match_score
                else "N/A"
            )

        ],

        [

            "Resume Quality",

            ats_status,

            (
                job_match_status
                if job_match_status
                else "N/A"
            )

        ]

    ]


    score_table = Table(

        score_data,

        colWidths=[
            160,
            160,
            160
        ]

    )


    score_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#166534")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#f0fdf4")
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            )

        ])

    )


    story.append(
        score_table
    )

    story.append(
        Spacer(1, 15)
    )


    # --------------------------------------------------------
    # NLP
    # --------------------------------------------------------

    story.append(

        Paragraph(
            "NLP Semantic Analysis",
            heading_style
        )

    )


    if nlp_score:

        story.append(

            Paragraph(

                f"Semantic Similarity Score: "
                f"<b>{nlp_score}%</b>",

                normal_style

            )

        )


        story.append(

            Paragraph(

                "The NLP system uses TF-IDF "
                "vectorization and cosine similarity "
                "to compare the resume with the "
                "provided job description.",

                normal_style

            )

        )

    else:

        story.append(

            Paragraph(

                "No job description was provided.",

                normal_style

            )

        )


    # --------------------------------------------------------
    # DETECTED SKILLS
    # --------------------------------------------------------

    story.append(

        Paragraph(
            "Detected Skills",
            heading_style
        )

    )


    if skills:

        story.append(

            Paragraph(

                ", ".join(skills),

                normal_style

            )

        )

    else:

        story.append(

            Paragraph(

                "No technical skills detected.",

                normal_style

            )

        )


    # --------------------------------------------------------
    # MATCHING SKILLS
    # --------------------------------------------------------

    if matching_skills:

        story.append(

            Paragraph(
                "Matching Job Skills",
                heading_style
            )

        )


        story.append(

            Paragraph(

                ", ".join(matching_skills),

                normal_style

            )

        )


    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    if missing_skills:

        story.append(

            Paragraph(
                "Missing Job Skills",
                heading_style
            )

        )


        story.append(

            Paragraph(

                ", ".join(missing_skills),

                normal_style

            )

        )


    # --------------------------------------------------------
    # CAREER ROLES
    # --------------------------------------------------------

    if job_roles:

        story.append(

            Paragraph(
                "Recommended Career Roles",
                heading_style
            )

        )


        for role in job_roles:

            story.append(

                Paragraph(

                    f"• {role}",

                    normal_style

                )

            )


    # --------------------------------------------------------
    # SUGGESTIONS
    # --------------------------------------------------------

    story.append(

        Paragraph(
            "Improvement Suggestions",
            heading_style
        )

    )


    if suggestions:

        for suggestion in suggestions:

            story.append(

                Paragraph(

                    f"• {suggestion}",

                    normal_style

                )

            )

    else:

        story.append(

            Paragraph(

                "No additional suggestions.",

                normal_style

            )

        )


    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    if job_description:

        story.append(

            Paragraph(
                "Analyzed Job Description",
                heading_style
            )

        )


        safe_job_description = (

            job_description

            .replace("&", "&amp;")

            .replace("<", "&lt;")

            .replace(">", "&gt;")

            .replace("\n", "<br/>")

        )


        story.append(

            Paragraph(

                safe_job_description,

                normal_style

            )

        )


    # --------------------------------------------------------
    # RESUME TEXT
    # --------------------------------------------------------

    story.append(
        PageBreak()
    )


    story.append(

        Paragraph(
            "Extracted Resume Text",
            heading_style
        )

    )


    safe_resume = (

        resume_text

        .replace("&", "&amp;")

        .replace("<", "&lt;")

        .replace(">", "&gt;")

        .replace("\n", "<br/>")

    )


    story.append(

        Paragraph(

            safe_resume,

            normal_style

        )

    )


    # --------------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------------

    document.build(
        story
    )


    buffer.seek(0)


    # --------------------------------------------------------
    # SEND PDF
    # --------------------------------------------------------

    return send_file(

        buffer,

        as_attachment=True,

        download_name=
            "ResumeIQ_Analysis_Report.pdf",

        mimetype=
            "application/pdf"

    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )