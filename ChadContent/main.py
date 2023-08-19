from flask import Flask, render_template, url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from chad_app import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)



