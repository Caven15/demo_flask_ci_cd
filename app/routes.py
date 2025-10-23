from flask import Flask
from app.controllers import book_controller


def init_routes(app: Flask) -> None:
	app.add_url_rule(
		"/api/books",
		endpoint="get_books",
		view_func=book_controller.get_books,
		methods=["GET"],
	)

	app.add_url_rule(
		"/api/books/<int:id>",
		endpoint="get_book_by_id",
		view_func=lambda id: book_controller.get_book(id),
		methods=["GET"],
	)
	app.add_url_rule(
		"/api/books",
		endpoint="create_book",
		view_func=book_controller.create_book,
		methods=["POST"]
	)
	app.add_url_rule(
		"/api/books/<int:id>",
		endpoint="update_book_full",
		view_func=lambda id : book_controller.update_book_full(id),
		methods=["PUT"]
	)
	app.add_url_rule(
		"/api/books/<int:id>",
		endpoint="update_book_partial",
		view_func=lambda id : book_controller.update_book_partial(id),
		methods=["PATCH"]
	)
	app.add_url_rule(
		"/api/books/<int:id>",
		endpoint="delete_book",
		view_func=lambda id : book_controller.remove_book(id),
		methods=["DELETE"]
	)
	app.add_url_rule(
		"/api/books/search",
		endpoint="search_book",
		view_func=book_controller.search_book,
		methods=["GET"]
	)