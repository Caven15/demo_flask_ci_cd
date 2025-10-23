# - Introduire le DTO (Data Transfert object)
# - Séparer la validation des données du controlleur
# - Amélriorer la qualite des retorus d'erreur API

# Permet de créer des classe avec moins de de code (auto-contructeur)
from dataclasses import dataclass, field
# Permet d'indiquer les types attendus
from typing import Optional, Tuple, Dict


@dataclass
class BookCreateDTO:
	"""
	Présenté les données nécéssaire pour créer un livre
	- Data class me permet de créer un contructeur automatiquement
	- Pour ce DTO les Champs (title, author) sont obligatoire
	"""

	title: str
	author: str

	@staticmethod
	def from_json(data: dict) -> Tuple[Optional['BookCreateDTO'], Optional[Dict]]:
		"""
		Méthode statique qui sera apelée depuis le controlleur pour valider les données
		Elle retourne :
		- Un Tuple(DTO,None) si tout va bien
		- ou Elle retourne une erreur {"error": "Message"} Si un erreur est detectée
		"""

		if not data:
			return None, {"error": "Aucune donnée fournie"}

		title = data.get("title")
		author = data.get("author")

		if not isinstance(title, str) or not isinstance(author, str):
			return None, {"error": "Les champ title et author doivent être des de caractères"}

		title = title.strip()
		author = author.strip()

		if not title:
			return None, {"error": "Le titre ne peut pas être vide."}
		if len(title) > 100:
			return None, {"error": "Le titre ne peux pas dépasser 100 caractères."}

		if not author:
			return None, {"error": "Le nom de l'auteur est obligatoire"}
		if len(author) < 3:
			return None, {"error": "Le nom de l'auteur doit contenir moins de 3 caractères"}

		return BookCreateDTO(title=title, author=author), None

@dataclass
class BookUpdateDTO:
	title: str
	author: str

	@staticmethod
	def from_json(data: dict) -> Tuple[Optional['BookUpdateDTO'], Optional[Dict]]:
		if not data:
			return None, {"error": "Données manquantes pur la mise à jour complètes"}

		dto, err = BookCreateDTO.from_json(data)

		if err:
			return None, err

		return BookUpdateDTO(title=dto.title, author=dto.author), None

@dataclass
class BookPatchDTO:
	title: Optional[str] = field(default=None)
	author: Optional[str] = field(default=None)

	@staticmethod
	def from_json(data: dict) -> Tuple[Optional['BookPatchDTO'], Optional[Dict]]:
		if not data:
			return None, {"error": "Aucune donnée fournie pour la mise à jour partielle"}

		title = data.get("title")
		author = data.get("author")

		if title is None and author is None:
			return None, {"error": "aucun champ valide à mettre à jour"}

		if title is not None:
			if not isinstance(title, str):
				return None, {"error": "Le titre doit être une chaine de caractère"}
			title = title.strip()
			if len(title) > 100:
				return None, {"error": "Le titre ne peut pas dépasser 100 caractères"}

		if author is not None:
			if not isinstance(author, str):
				return None, {"error": "L'auteur doit être une chaine de caractère"}
			author = author.strip()
			if len(author) < 3:
				return None, {"error": "L'auteur doit contenir au moins 3 caractères"}

		return BookPatchDTO(title=title, author=author), None
