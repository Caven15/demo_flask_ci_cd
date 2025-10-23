from app.dtos.book_dto import (
	BookCreateDTO,
	BookUpdateDTO,
	BookPatchDTO
)

from app.services.book_service import (
    get_all,
    get_book_by_id,
    add_book,
    update_book,
    patch_book,
    delete_book,
    search_book_by_author
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

	dto, err = BookCreateDTO.from_json(data)
	if err:
		return jsonify(err), 400 # retourne le message d'erreur du dto

	new_book = add_book(dto.title, dto.author)
	return jsonify(new_book.to_dict()), 201

def update_book_full(id: int):
	"""EndPoint : PUT /api/books/<id> => mise à jour complète"""
	dto, err = BookUpdateDTO.from_json(request.get_json())
	if err:
		return jsonify(err), 400

	updated = update_book(id, dto.title, dto.author)
	if not updated:
		return jsonify({"error": f"Livre avec Id {id} introuvable"}), 404

	return jsonify(updated.to_dict()), 200

def update_book_partial(id: int):
	"""EndPoint : PATCH /api/books/<id> => mise à jour partielle"""
	dto, err = BookPatchDTO.from_json(request.get_json())
	if err:
		return jsonify(err), 400

	update_data = {k: v for k,v in dto.__dict__.items() if v is not None} # on filtre les champs None

	updated = patch_book(id, update_data) # Transforme le DTO en Dictionnaire
	if not updated:
		return jsonify({"error": f"Livre avec Id {id} introuvable"}), 404

	return jsonify(updated.to_dict()), 200

def remove_book(id: int):
	"""EndPoint : DELETE /api/books/<id>"""
	deleted = delete_book(id)
	if deleted:
		return "", 204
	return jsonify({"error" : "Livre non trouvé"}), 404

def search_book():
	"""EndPoint : DELETE /api/books/search?author=Nom"""
	author = request.args.get("author", "")
	if not author:
		return jsonify({"error": "Paramètre 'author' requis"}), 400

	books = search_book_by_author(author)
	return jsonify([b.to_dict() for b in books]), 200