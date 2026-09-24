from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date

app = Flask(__name__)

app.secret_key = "job-tracker-secret-key"

DATABASE = "instance/jobs.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            job_title TEXT NOT NULL,
            location TEXT,
            job_type TEXT,
            application_date TEXT,
            deadline TEXT,
            status TEXT NOT NULL,
            job_url TEXT,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/applications")
def applications():
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "")

    connection = get_db_connection()

    query = "SELECT * FROM applications WHERE 1=1"
    parameters = []

    if search:
        query += " AND (company LIKE ? OR job_title LIKE ?)"
        parameters.append(f"%{search}%")
        parameters.append(f"%{search}%")

    if status:
        query += " AND status = ?"
        parameters.append(status)

    if sort == "deadline_asc":
        query += " ORDER BY deadline ASC"
    elif sort == "deadline_desc":
        query += " ORDER BY deadline DESC"

    applications = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "applications.html",
        applications=applications,
        search=search,
        status=status,
        sort=sort
    )


@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":

        company = request.form["company"].strip()
        job_title = request.form["job_title"].strip()
        location = request.form["location"].strip()
        job_type = request.form["job_type"]
        application_date = request.form["application_date"]
        deadline = request.form["deadline"]
        status = request.form["status"]
        job_url = request.form["job_url"].strip()
        notes = request.form["notes"].strip()

        # Server-side validation
        if not company or not job_title:
            flash("Company name and job title are required.", "error")
            return redirect(url_for("add_application"))
        connection = get_db_connection()

        connection.execute("""
            INSERT INTO applications (
                company, job_title, location, job_type,
                application_date, deadline, status, job_url, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company, job_title, location, job_type,
            application_date, deadline, status, job_url, notes
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("applications"))

    return render_template("add_application.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    connection = get_db_connection()

    application = connection.execute(
        "SELECT * FROM applications WHERE id = ?",
        (id,)
    ).fetchone()

    if application is None:
        connection.close()
        return "Application not found", 404

    if request.method == "POST":
        company = request.form["company"]
        job_title = request.form["job_title"]
        location = request.form["location"]
        job_type = request.form["job_type"]
        application_date = request.form["application_date"]
        deadline = request.form["deadline"]
        status = request.form["status"]
        job_url = request.form["job_url"]
        notes = request.form["notes"]

        connection.execute("""
            UPDATE applications
            SET company = ?,
                job_title = ?,
                location = ?,
                job_type = ?,
                application_date = ?,
                deadline = ?,
                status = ?,
                job_url = ?,
                notes = ?
            WHERE id = ?
        """, (
            company,
            job_title,
            location,
            job_type,
            application_date,
            deadline,
            status,
            job_url,
            notes,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("applications"))

    connection.close()

    return render_template(
        "edit_application.html",
        application=application
    )


@app.route("/delete/<int:id>")
def delete_application(id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM applications WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("applications"))


@app.route("/dashboard")
def dashboard():

    connection = get_db_connection()

    total = connection.execute(
        "SELECT COUNT(*) FROM applications"
    ).fetchone()[0]

    applied = connection.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Applied",)
    ).fetchone()[0]

    interviews = connection.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Interview",)
    ).fetchone()[0]

    offers = connection.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Offer",)
    ).fetchone()[0]

    rejected = connection.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Rejected",)
    ).fetchone()[0]

    upcoming_deadlines = connection.execute("""
        SELECT *
        FROM applications
        WHERE deadline IS NOT NULL
        AND deadline != ''
        AND deadline >= date('now')
        ORDER BY deadline ASC
        LIMIT 5
    """).fetchall()

    connection.close()

    deadlines = []

    today = date.today()

    for application in upcoming_deadlines:

        deadline_date = date.fromisoformat(application["deadline"])

        days_left = (deadline_date - today).days

        if days_left <= 3:
            urgency = "Due within 3 days"

        elif days_left <= 7:
            urgency = "Due within 7 days"

        else:
            urgency = "Upcoming"

        deadlines.append({
            "application": application,
            "days_left": days_left,
            "urgency": urgency
        })

    return render_template(
        "dashboard.html",
        total=total,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        upcoming_deadlines=deadlines
    )

    


if __name__ == "__main__":
    init_db()
    app.run(debug=True)