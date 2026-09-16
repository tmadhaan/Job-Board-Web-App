import os
from flask import Flask, render_template, request, redirect, url_for, flash
from model import db, Job

app = Flask(__name__)

# Use an environment variable for the secret key
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Configure SQLite database
instance_path = os.path.join(app.instance_path, "jobboard.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{instance_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create the database folder and tables if they don't exist
with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)
    db.create_all()


@app.route("/")
def home():
    search_query = request.args.get("search", "").strip()

    if search_query:
        jobs = Job.query.filter(
            Job.title.ilike(f"%{search_query}%")
        ).all()
    else:
        jobs = Job.query.all()

    return render_template("index.html", jobs=jobs)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()
        salary = request.form.get("salary", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not company or not location:
            flash("Title, Company, and Location are required.")
            return redirect(url_for("add"))

        try:
            new_job = Job(
                title=title,
                company=company,
                location=location,
                salary=salary,
                description=description
            )

            db.session.add(new_job)
            db.session.commit()

            return redirect(url_for("home"))

        except Exception:
            db.session.rollback()
            return "An error occurred while saving the job.", 500

    return render_template("add.html")


@app.route("/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()
        salary = request.form.get("salary", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not company or not location:
            flash("Title, Company, and Location are required.")
            return redirect(url_for("edit_job", job_id=job.id))

        try:
            job.title = title
            job.company = company
            job.location = location
            job.salary = salary
            job.description = description

            db.session.commit()

            return redirect(url_for("home"))

        except Exception:
            db.session.rollback()
            return "An error occurred while updating the job.", 500

    return render_template("edit.html", job=job)


@app.route("/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    try:
        db.session.delete(job)
        db.session.commit()

    except Exception:
        db.session.rollback()
        return "An error occurred while deleting the job.", 500

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)