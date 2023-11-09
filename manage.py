from flask import render_template, url_for
from api import create_app, db
from api.v1.database import User, UserAndCards, Card  # noqa
import click

app = create_app()

app.template_folder = "./v1/templates"
app.static_folder = "./v1/static"


@click.group()
def cli():
    pass


@app.get("/")
def index():
    url_for("static", filename="hello.css")
    return render_template("authPage.html")


@cli.command()
def run():
    click.echo("Запуск сервера Flask")
    app.run()


@cli.command()
def initdb():
    click.echo("Попытка инициализации базы данных")
    try:
        with app.app_context():
            db.create_all()
        click.echo("Инициализация прошла успешно")
    except Exception as e:
        click.echo(f"Ошибка: {e}")


@cli.command()
def reinitdb():
    click.echo("Попытка реинициализации базы данных")
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
        click.echo("Реинициализация прошла успешно")
    except Exception as e:
        click.echo(f"Ошибка: {e}")


if __name__ == "__main__":
    cli()
