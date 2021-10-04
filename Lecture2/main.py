from decouple import config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate


app = Flask(__name__)

db_user = config('DB_USER')
db_password = config("DB_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5433/store'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class BookModel(db.Model):
    __tablename__ = 'books'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    some_column = db.Column(db.String, nullable=False, default="some", server_default="ok")
    reader_pk = db.Column(db.Integer, db.ForeignKey('readers.pk'))
    reader = db.relationship('ReaderModel')

    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(db.Model):
    __tablename__ = 'readers'
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    books = db.relationship("BookModel", backref="book", lazy='dynamic')


class Books(Resource):
    def post(self):
        data = request.get_json()
        new_book = BookModel(**data)
        db.session.add(new_book)
        db.session.commit()
        return new_book.as_dict()


class Reader(Resource):
    def get(self, reader_pk):
        reader = ReaderModel.query.filter_by(pk=reader_pk).first()
        books = BookModel.query.filter_by(reader_pk=reader_pk)
        return {"data": [book.as_dict() for book in reader.books]}



db.create_all()
api.add_resource(Books, "/")
api.add_resource(Reader, "/readers/<int:reader_pk>/books")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)