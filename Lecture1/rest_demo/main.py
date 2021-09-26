from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class BookModel:
    _pk = 1
    def __init__(self, title, author):
        self.pk = BookModel._pk
        self.title = title
        self.author = author
        BookModel._pk += 1

    def serialize(self):
        return self.__dict__


books = [BookModel(f"Title {i}", f"Author {i}") for i in range(1, 11)]


class Book(Resource):
    def get(self, pk):
        try:
            book = [b for b in books if b.pk == pk][0]
            return book.serialize()
        except IndexError:
            return {"error": "Not Found"}, 404

    def put(self, pk):
        try:
            data = request.get_json()
            book = [b for b in books if b.pk == pk][0]
            book.title = data["title"]
            book.author = data["author"]
            return book.serialize(), 200
        except IndexError:
            return {"error": "Not Found"}, 404
        except:
            return {"error": "Bad Request"}, 400

    def delete(self, pk):
        try:
            book = [b for b in books if b.pk == pk][0]
            books.remove(book)
            return 204
        except IndexError:
            return {"error": "Not Found"}, 404



class Books(Resource):
    def get(self):
        return {"data": [b.serialize() for b in books]}

    def post(self):
        try:
            data = request.get_json()
            book = BookModel(**data)
            books.append(book)
            return book.serialize(), 201
        except Exception as ex:
            return {"error": "Bad Request"}, 400





api.add_resource(Book, "/<int:pk>")
api.add_resource(Books, "/")


if __name__ == "__main__":
    app.run(debug=True)
