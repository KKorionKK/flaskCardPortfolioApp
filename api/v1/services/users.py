from api.v1.database import User, Card, UserAndCards
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, Sequence, and_, delete

def get_user_by_username(username: str, db: SQLAlchemy) -> User | None:
    user = db.session.scalar(
        select(User)
        .where(User.username == username)
    )
    return user

def get_cards_by_user_uuid(user_uuid: str, db: SQLAlchemy) -> list[Card]:
    cards: Sequence[Card] = db.session.scalars(
        select(Card)
        .where(Card.card_uuid == UserAndCards.card_uuid)
        .join(UserAndCards, UserAndCards.user_uuid == user_uuid)
    ).all()
    return [card for card in cards]

def card_create(card_data: dict[str, str], user_uuid: str, db: SQLAlchemy) -> tuple:
    card = Card(**card_data)
    card_and_users = UserAndCards(card_uuid=card.card_uuid, user_uuid=user_uuid)
    db.session.add(card)
    db.session.add(card_and_users)
    db.session.commit()
    return ("Success", 200)

def check_is_owner(card_uuid: str, user_uuid: str, db: SQLAlchemy) -> UserAndCards | None:
    is_owner: UserAndCards | None = db.session.scalar(
        select(UserAndCards)
        .where(and_(UserAndCards.card_uuid == card_uuid, UserAndCards.user_uuid == user_uuid))
    )
    return is_owner

def delete_card_by_uuid(card_uuid: str, user_uuid: str, db: SQLAlchemy) -> tuple:
    check = check_is_owner(card_uuid=card_uuid, user_uuid=user_uuid, db=db)
    if check:
        db.session.execute(
            delete(Card)
            .where(Card.card_uuid == check.card_uuid)
        )
        db.session.delete(check)
        db.session.commit()
        return ("Success", 200)
    return ("У вас нет привилегий для данного действия", 400)


# TODO: 1. сохранение auth_token 2. редактировние + форма. 3. emoji меню. 4. загрузка файла. 5. выбор файла/emoji