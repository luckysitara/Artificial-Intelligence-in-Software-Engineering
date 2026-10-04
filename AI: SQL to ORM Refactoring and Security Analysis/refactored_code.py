#!/usr/bin/env python3
"""User management refactored to the SQLAlchemy ORM.

The procedural script becomes a declarative ``User`` model plus a small
data-access layer built on ORM sessions:

* the schema lives in one place (the model), not in scattered SQL strings;
* values are always bound as parameters by the ORM, never interpolated;
* each operation runs in a session that commits on success and rolls back
  automatically when an exception is raised.

The connection URL is read from the environment so credentials stay out of
the source code. Swapping the dialect prefix (mysql+mysqldb, sqlite://,
postgresql+psycopg) runs the same code on another database engine.
"""

import os
from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:yourpassword@localhost/example_db",
)

Base = declarative_base()


class User(Base):
    """The ``users`` table mapped to a Python object."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        """Return a developer-friendly representation of the row."""
        return "User(id={!r}, username={!r}, email={!r})".format(
            self.id, self.username, self.email)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# expire_on_commit=False keeps loaded attributes usable after the commit.
Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables():
    """Create the users table if it does not exist yet."""
    Base.metadata.create_all(engine)


def create_user(username, email):
    """Insert a new user and return its generated id."""
    if not username or not email:
        print("Username and email are required.")
        return None
    with session_scope() as session:
        user = User(username=username, email=email)
        session.add(user)
        session.flush()  # send the INSERT so the id is generated
        user_id = user.id
    print("User '{}' created successfully.".format(username))
    return user_id


def get_user_by_username(username):
    """Return the User with this username, or None."""
    with session_scope() as session:
        return session.query(User).filter_by(username=username).first()


def update_user_email(username, new_email):
    """Update the email of an existing user."""
    with session_scope() as session:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            print("User '{}' not found.".format(username))
            return False
        user.email = new_email  # the unit of work turns this into an UPDATE
    print("User '{}' updated successfully.".format(username))
    return True


def delete_user(username):
    """Delete a user by username."""
    with session_scope() as session:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            print("User '{}' not found.".format(username))
            return False
        session.delete(user)
    print("User '{}' deleted successfully.".format(username))
    return True


def list_users():
    """Return every user, ordered by id."""
    with session_scope() as session:
        return session.query(User).order_by(User.id).all()


if __name__ == "__main__":
    create_tables()
    create_user("alice", "alice@example.com")
    print(get_user_by_username("alice"))
    update_user_email("alice", "alice@new-domain.com")
    print(list_users())
    delete_user("alice")
    print(list_users())
