import os

from sqlalchemy import create_engine, select, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Credentials come from the environment, not from source code
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:@localhost/example_db",
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username!r}, email={self.email!r})"


def create_user(session, username, email):
    if not username or not email:
        print("Username and email are required.")
        return None
    try:
        user = User(username=username, email=email)
        session.add(user)
        session.commit()
        print(f"User '{username}' created successfully.")
        return user
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating user: {e}")
        return None


def get_user_by_username(session, username):
    return session.scalars(select(User).where(User.username == username)).first()


def update_user_email(session, username, new_email):
    user = get_user_by_username(session, username)
    if user is None:
        print("User not found.")
        return
    try:
        user.email = new_email
        session.commit()
        print(f"Email for '{username}' updated successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating email: {e}")


def delete_user(session, username):
    user = get_user_by_username(session, username)
    if user is None:
        print("User not found.")
        return
    try:
        session.delete(user)
        session.commit()
        print(f"User '{username}' deleted successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting user: {e}")


def list_users(session):
    return session.scalars(select(User).order_by(User.id)).all()


if __name__ == "__main__":
    # 1. Create the table from the model metadata
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # 2. Add a new user
        create_user(session, "alice", "alice@example.com")

        # 3. Query for that user
        print(get_user_by_username(session, "alice"))

        # 4. List all users
        print(list_users(session))
