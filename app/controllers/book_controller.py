from app.services.book_service import (
    get_all,
    get_book_by_id,
    add_book,
    update_book,
    patch_book,
    delete_book
)
from flask import jsonify, request


def get_books():
	"""EndPoint : GET /api/books"""
	books = get_all()
	payload = [book.to_dict() for book in books]
	return jsonify(payload), 200


def get_book(id: int):
	"""EndPoint : GET /api/book/<id>"""
	book = get_book_by_id(id)
	if (book):
		return jsonify(book.to_dict()), 200
	return jsonify({"error": "Livre non trouvé"}), 404


def create_book():
	"""EndPoint : POST /api/books"""
	data = request.get_json()
	if not data or "title" not in data or "author" not in data:
		return jsonify({"error": "Champs 'title et 'author' requis", }), 400

	new_book = add_book(data["title"], data["author"])
	return jsonify(new_book.to_dict()), 201


def update_book_full(id: int):
	"""EndPoint : PUT /api/books/<id> => mise à jour complète"""
	data = request.get_json()
	if not data or "title" not in data or "author" not in data:
		return jsonify({"error": "Champs 'title et 'author' requis", }), 400

	updated = update_book(id, data["title"], data["author"])
	if updated:
		return jsonify(updated.to_dict()), 200
	return jsonify({"error": "Livre non trouvé"}), 404


def update_book_partial(id: int):
	"""EndPoint : PATCH /api/books/<id> => mise à jour partielle"""
	data = request.get_json()
	if not data:
		return jsonify({"error": "données JSON requises"}), 400

	updated = patch_book(id, data)
	if updated:
		return jsonify(updated.to_dict()), 200
	return jsonify({"error": "Livre non trouvé"}), 404


def remove_book(id: int):
	"""EndPoint : DELETE /api/books/<id>"""
	deleted = delete_book(id)
	if deleted:
		return "", 204
	return jsonify({"error" : "Livre non trouvé"}), 404