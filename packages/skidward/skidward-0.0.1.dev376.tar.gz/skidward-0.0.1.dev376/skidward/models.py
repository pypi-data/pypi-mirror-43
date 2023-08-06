from datetime import datetime as dt
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import JSONType
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


# Creating Models
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, default="end_user")
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def __repr__(self):
        return self.username


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    tasks = db.relationship("Task", backref="worker")

    def __repr__(self):
        return self.name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"), nullable=False)
    context = db.Column(JSONType)
    cron_string = db.Column(db.String)

    def __repr__(self):
        return self.name


class JobStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    SUCCESS = "success"
    FAIL = "fail"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Enum(JobStatus), nullable=False, default=JobStatus.READY)
    ran_at = db.Column(db.DateTime(), default=dt.utcnow())
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    task = db.relationship("Task")

    def __repr__(self):
        return "Job %s at %s is %s. " % (self.task_id, self.ran_at, self.state)
