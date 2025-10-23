from app.models.book_model import Book


BOOKS = [
	Book(1, "Harry Potter", "JK Rowling"),
	Book(2, "ça", "Stephen King"),
	Book(3, "La Bible", "Dieu")
]

def get_all() -> list[Book]:
	"""Retourne une liste complète des livres"""
	return BOOKS

def get_book_by_id(book_id : int) -> Book | None:
	"""Retourne un livre par son identifiant, sinon None."""
	return next((b for b in BOOKS if b.id == book_id), None)

def add_book(title : str, author : str) -> Book:
    """Ajoute un nouveau livre à la liste"""
    new_id = max(b.id for b in BOOKS) + 1 if BOOKS else 1
    new_book = Book(new_id, title, author)
    BOOKS.append(new_book)
    return new_book

def update_book(book_id : int, title : str, author : str) -> Book | None:
	"""Mise à jour complète (PUT) : remplacer le titre et l'auteur"""
	book = get_book_by_id(book_id)
	if book:
		book.title = title
		book.author = author
		return book
	return None

def patch_book(book_id: int, data:dict) -> Book | None:
	"""mise à jout partielle (PATCH) : ne modifie que les champs présents"""
	book = get_book_by_id(book_id)
	if not book:
		return None

	if "title" in data:
		book.title = data["title"]
	if "author" in data:
		book.author = data["author"]
	return book

def delete_book(book_id : int) -> bool:
	"""Supprime un livre par id"""
	book = get_book_by_id(book_id)
	if not book:
		return False
	BOOKS.remove(book)
	return True

def search_book_by_author(author : str) -> list[Book]:
	"""Recherche les livre d'un auteur donné"""
	return [b for b in BOOKS if author.lower() in b.author.lower()]