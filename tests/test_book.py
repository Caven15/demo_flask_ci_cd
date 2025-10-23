import pytest
from app import create_app


@pytest.fixture
def client():
	"""Client de test Flask isolé pour chaque test"""
	app = create_app()
	app.testing = True
	return app.test_client()

#region GET
def test_get_all_books(client):
	# Quand / When
	response = client.get("/api/books")

	# Alors / Then
	assert response.status_code == 200
	data = response.get_json()
	assert isinstance(data, list)
	assert len(data) == 3  # Correpond aux fake data
	# Vérification basique de notre schéma
	assert set(data[0].keys()) == {"id", "title", "author"}


def test_get_book_not_found(client):
	response = client.get("/api/books/999")

	assert response.status_code == 404
	assert response.get_json()['error'] == "Livre non trouvé"


def test_get_single_book(client):
	response = client.get("/api/books/1")

	assert response.status_code == 200
	data = response.get_json()
	assert data["title"] == "Harry Potter"
	assert data["author"] == "JK Rowling"

# endregion

#region POST

def test_post_book(client):
	# on récupère d'abord la longueur avant l'ajout
	response_before = client.get("/api/books")
	count_before = len(response_before.get_json())

	# on ajoute une nouveau livre
	new_book = {
		"title": "DevWeb",
		"author": "Bstorm"
	}
	response = client.post("/api/books", json=new_book)

	assert response.status_code == 201
	data = response.get_json()
	assert data["title"] == "DevWeb"
	assert data["author"] == "Bstorm"

	# Vérification que la taille de la liste a augmenté
	response_after = client.get("/api/books")
	count_after = len(response_after.get_json())
	assert count_after == count_before + 1

#endregion

#region PUT

def test_put_book(client):
	# ON met a jour complètement le livre qui comporte l'id 1
	updated_data = {
		"title": "test_update_title",
		"author": "test_update_author"
	}
	response = client.put("/api/books/1", json=updated_data)

	assert response.status_code == 200
	data = response.get_json()
	assert data["title"] == "test_update_title"
	assert data["author"] == "test_update_author"

def test_put_book_not_found(client):
	response = client.put("/api/books/999", json={"title": "x", "author": "y"})
	assert response.status_code == 404


#endregion

#region PATCH

def test_patch_book(client):
	# Mise à jour partielle (author)
	response = client.patch("/api/books/2", json={"author": "Laboon"})
	assert response.status_code == 200
	data = response.get_json()
	assert data["author"] == "Laboon"
	assert "title" in data


def test_patch_book_not_found(client):
	response = client.patch("/api/books/999", json={"title": "Inconnu"})
	assert response.status_code == 404


#endregion

#region DELETE

def test_delete_book(client):
    # Création d'un livre à supprimer
	new_book = {
		"title": "DevWeb",
		"author": "Bstorm"
	}
	client.post("/api/books", json=new_book)

	# Taille avant suppression
	before = len(client.get("/api/books").get_json())

	# On supprime le dernier livre ajouté
	last_id = before
	response = client.delete(f"/api/books/1")

	assert response.status_code == 204

	# Vérifie que la taille a diminué
	after = len(client.get("/api/books").get_json())
	assert after == before - 1


def test_delete_book_not_found(client):
	response = client.delete("/api/books/999")
	assert response.status_code == 404

#endregion
