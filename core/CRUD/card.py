from . import Card

def card2Dict(card) -> dict:
	return {
		'id': card.id,
		'user_id': card.user_id,
		'side1': card.side1,
		'side2': card.side2
	}

def create(user_id: int, side1: str, side2: str):
	return Card.create(
		user_id=user_id, side1=side1, side2=side2
	)

# TODO: добавить защиту от выхода за индекс
def readOne(card_id):
	return card2Dict(Card.get(id=card_id))

def readAllUserCards(user_id):
	cards = Card.select().where(Card.user_id == user_id)
	return [card2Dict(card) for card in cards]

def update(user_id, card_id, side1: str, side2: str):
	card = Card.get(id=card_id)
	if int(card.user_id) != user_id:
		raise PermissionError
	card.side1 = side1
	card.side2 = side2
	return card.save()

def delete(user_id, card_id):
	card = Card.get(id=card_id)
	if int(card.user_id) != user_id:
		raise PermissionError
	return card.delete_instance()