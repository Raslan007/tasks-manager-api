"""Flask application factory and API route definitions."""

from flask import Flask, jsonify
from flask.views import MethodView
from flask_smorest import Api, Blueprint

from config import Config
from models import db, Task
from schemas import TaskCreateSchema, TaskQueryArgsSchema, TaskSchema, TaskUpdateSchema


def create_app(config_class=Config):
    """Create, configure, and return the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    api = Api(app)

    # ── Tasks Blueprint ─────────────────────────────────────────────
    blp = Blueprint(
        "tasks",
        __name__,
        url_prefix="/api/v1",
        description="CRUD operations on tasks",
    )

    @blp.route("/tasks")
    class TaskList(MethodView):
        @blp.arguments(TaskQueryArgsSchema, location="query")
        @blp.response(200, TaskSchema(many=True))
        def get(self, args):
            """List all tasks with optional status / priority filtering."""
            query = Task.query
            if "status" in args:
                query = query.filter_by(status=args["status"])
            if "priority" in args:
                query = query.filter_by(priority=args["priority"])
            return query.order_by(Task.created_at.desc()).all()

        @blp.arguments(TaskCreateSchema)
        @blp.response(201, TaskSchema)
        def post(self, data):
            """Create a new task."""
            task = Task(**data)
            db.session.add(task)
            db.session.commit()
            return task

    @blp.route("/tasks/<int:task_id>")
    class TaskDetail(MethodView):
        @blp.response(200, TaskSchema)
        def get(self, task_id):
            """Get a single task by ID."""
            return db.get_or_404(Task, task_id)

        @blp.arguments(TaskUpdateSchema)
        @blp.response(200, TaskSchema)
        def put(self, data, task_id):
            """Update an existing task."""
            task = db.get_or_404(Task, task_id)
            for key, value in data.items():
                setattr(task, key, value)
            db.session.commit()
            return task

        @blp.response(204)
        def delete(self, task_id):
            """Delete a task by ID."""
            task = db.get_or_404(Task, task_id)
            db.session.delete(task)
            db.session.commit()

    api.register_blueprint(blp)

    # ── Health check ────────────────────────────────────────────────
    @app.get("/")
    def health_check():
        """Root endpoint — confirms the API is running."""
        return jsonify(status="ok", docs="/docs")

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
