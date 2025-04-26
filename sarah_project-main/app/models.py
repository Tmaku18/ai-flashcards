from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Text,
    case,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    flashcard_sets = relationship(
        "FlashcardSet", back_populates="owner", cascade="all, delete-orphan"
    )
    study_sessions = relationship(
        "StudySession", back_populates="user", cascade="all, delete-orphan"
    )
    progress_records = relationship("FlashcardProgress", back_populates="user")

    @classmethod
    def get_by_username(cls, db, username):
        """Get a user by username."""
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def get_by_email(cls, db, email):
        """Get a user by email."""
        return db.query(cls).filter(cls.email == email).first()


class FlashcardSet(Base):
    __tablename__ = "flashcard_sets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    source_document = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    owner = relationship("User", back_populates="flashcard_sets")
    flashcards = relationship(
        "Flashcard", back_populates="flashcard_set", cascade="all, delete-orphan"
    )
    study_sessions = relationship(
        "StudySession", back_populates="flashcard_set", cascade="all, delete-orphan"
    )

    @classmethod
    def get_by_id(cls, db, set_id, user_id=None):
        """Get a flashcard set by ID, optionally filtering by user ID."""
        query = db.query(cls).filter(cls.id == set_id)
        if user_id is not None:
            query = query.filter(cls.user_id == user_id)
        return query.first()

    @classmethod
    def get_all_by_user(cls, db, user_id, skip=0, limit=100):
        """Get all flashcard sets for a user."""
        return (
            db.query(cls).filter(cls.user_id == user_id).offset(skip).limit(limit).all()
        )

    def add_flashcard(self, db, question, answer):
        """Add a flashcard to this set."""
        from . import models

        flashcard = models.Flashcard(question=question, answer=answer, set_id=self.id)
        db.add(flashcard)
        db.commit()
        db.refresh(flashcard)
        return flashcard


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"))

    # Relationships
    flashcard_set = relationship("FlashcardSet", back_populates="flashcards")
    progress_records = relationship("FlashcardProgress", back_populates="flashcard")

    @classmethod
    def get_by_id(cls, db, card_id, set_id=None):
        """Get a flashcard by ID, optionally filtering by set ID."""
        query = db.query(cls).filter(cls.id == card_id)
        if set_id is not None:
            query = query.filter(cls.set_id == set_id)
        return query.first()

    @classmethod
    def get_all_by_set(cls, db, set_id, skip=0, limit=100):
        """Get all flashcards in a set."""
        return (
            db.query(cls).filter(cls.set_id == set_id).offset(skip).limit(limit).all()
        )


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"))

    # Relationships
    user = relationship("User", back_populates="study_sessions")
    flashcard_set = relationship("FlashcardSet", back_populates="study_sessions")
    progress_records = relationship("FlashcardProgress", back_populates="study_session")

    @classmethod
    def get_by_id(cls, db, session_id, user_id=None):
        """Get a study session by ID, optionally filtering by user ID."""
        query = db.query(cls).filter(cls.id == session_id)
        if user_id is not None:
            query = query.filter(cls.user_id == user_id)
        return query.first()

    @classmethod
    def get_all_by_user(cls, db, user_id, skip=0, limit=100):
        """Get all study sessions for a user."""
        return (
            db.query(cls).filter(cls.user_id == user_id).offset(skip).limit(limit).all()
        )

    def end_session(self, db):
        """End a study session."""
        from datetime import datetime, timezone

        # Use UTC time with timezone info to avoid timezone issues
        self.end_time = datetime.now(timezone.utc)
        db.add(self)
        db.commit()
        db.refresh(self)
        return self


class FlashcardProgress(Base):
    __tablename__ = "flashcard_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"))
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=True)
    is_correct = Column(Boolean)
    difficulty = Column(String)  # 'easy', 'medium', 'hard'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="progress_records")
    flashcard = relationship("Flashcard", back_populates="progress_records")
    study_session = relationship("StudySession", back_populates="progress_records")

    @classmethod
    def get_by_flashcard(cls, db, flashcard_id, user_id):
        """Get all progress records for a flashcard and user."""
        return (
            db.query(cls)
            .filter(cls.flashcard_id == flashcard_id, cls.user_id == user_id)
            .order_by(cls.created_at.desc())
            .all()
        )

    @classmethod
    def get_stats_by_flashcard(cls, db, flashcard_id, user_id):
        """Get statistics for a flashcard and user."""
        from sqlalchemy import func

        stats = (
            db.query(
                cls.flashcard_id,
                func.sum(cls.is_correct.cast(Integer)).label("correct_count"),
                func.sum((~cls.is_correct).cast(Integer)).label("incorrect_count"),
                func.max(cls.created_at).label("last_studied"),
                func.avg(
                    case(
                        (cls.difficulty == "easy", 1),
                        (cls.difficulty == "medium", 2),
                        (cls.difficulty == "hard", 3),
                        else_=2,
                    )
                ).label("average_difficulty"),
            )
            .filter(cls.flashcard_id == flashcard_id, cls.user_id == user_id)
            .group_by(cls.flashcard_id)
            .first()
        )

        return stats

    @classmethod
    def get_stats_by_set(cls, db, set_id, user_id):
        """Get statistics for all flashcards in a set for a user."""
        from sqlalchemy import func
        from sqlalchemy.orm import aliased

        flashcard_alias = aliased(Flashcard)

        stats = (
            db.query(
                cls.flashcard_id,
                func.sum(cls.is_correct.cast(Integer)).label("correct_count"),
                func.sum((~cls.is_correct).cast(Integer)).label("incorrect_count"),
                func.max(cls.created_at).label("last_studied"),
                func.avg(
                    case(
                        (cls.difficulty == "easy", 1),
                        (cls.difficulty == "medium", 2),
                        (cls.difficulty == "hard", 3),
                        else_=2,
                    )
                ).label("average_difficulty"),
            )
            .join(flashcard_alias, cls.flashcard_id == flashcard_alias.id)
            .filter(flashcard_alias.set_id == set_id, cls.user_id == user_id)
            .group_by(cls.flashcard_id)
            .all()
        )

        return stats
