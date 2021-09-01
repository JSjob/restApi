from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import desc

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class BookModel(db.Model):
	id = db.Column(db.String, primary_key=True)
	title = db.Column(db.String(1024), nullable=False)
	authors = db.Column(db.String(100), nullable=False)
	published_date = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Book(title={title}, authors={authors}, published_date={published_date})"
#db.create_all()

resource_fields = {
	'id': fields.String,
	'title': fields.String,
	'authors': fields.String,
	'published_date' : fields.Integer
}

class BookByID(Resource):
	@marshal_with(resource_fields)
	def get(self, book_id):
		result = BookModel.query.filter_by(id=book_id).first()
		if not result:
			abort(404, message="Book does not exist...")
		return result

class NewBook(Resource):
	@marshal_with(resource_fields)
	def put(self, book_id):
		book_put_args = reqparse.RequestParser()
		book_put_args.add_argument("title", type=str, help="title is required", required=True)
		book_put_args.add_argument("authors", type=str, help="authors are required", required=True)
		book_put_args.add_argument("published_date", type=int, help="published_date is required", required=True)
		args = book_put_args.parse_args()

		result = BookModel.query.filter_by(id=book_id).first()
		if result:
			abort(409, message="Book already exists...")
		
		book = BookModel(id=book_id, title = args['title'], authors= args['authors'], published_date=args['published_date'])
		db.session.add(book)
		db.session.commit()
		return book, 201

class Books(Resource):
	def get(self):
		books = {}
		query = BookModel.query.all()
		for q in query:
			books[q.id] = {'title':q.title, 'authors':q.authors, 'published_date':q.published_date}
		return books

class BooksByAuthor(Resource):
	def get(self, auth):
		books = {}
		query = BookModel.query.filter_by(authors=auth).all()
		if not query:
			abort(404, message="I dont think that author exists, check your spelling and try again...")
		for q in query:
			books[q.id] = {'title':q.title, 'authors':q.authors, 'published_date':q.published_date}
		return books

class BooksByDate(Resource):
	def get(self, date):
		books = {}
		query = BookModel.query.filter_by(published_date=date).all()
		if not query:
			abort(404, message="Book does not exist...")
		for q in query:
			books[q.id] = {'title':q.title, 'authors':q.authors, 'published_date':q.published_date}
		return books

class BooksByOrder(Resource):
	def get(self, type):
		books = {}
		if type == 'asc':
			query = BookModel.query.order_by(desc('published_date')).all()
		elif type == 'desc':
			query = BookModel.query.order_by('published_date').all()
		else:
			abort(404, message="sorry that type of order does not exist")
		for q in query:
			books[q.id] = {'title':q.title, 'authors':q.authors, 'published_date':q.published_date}
		return books

api.add_resource(NewBook, "/new_book/<string:book_id>")
api.add_resource(BookByID, "/book_by_id/<string:book_id>")
api.add_resource(Books, "/all_books")
api.add_resource(BooksByAuthor, "/book_by_author/<string:auth>")
api.add_resource(BooksByDate, "/book_by_date/<string:date>")
api.add_resource(BooksByOrder, "/books_by_order/<string:type>")


if __name__ == "__main__":
	app.run(debug=True)
