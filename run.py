from app import create_app, db
from app.extension.to_sql import json_to_sql

app = create_app()

with app.app_context():
    db.create_all()
    json_to_sql()


if __name__ == "__main__":
    app.run(debug=True)


