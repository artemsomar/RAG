from datetime import datetime
from sqlalchemy import ARRAY, Float, String, ForeignKey, BigInteger, Text, UniqueConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime]
    role: Mapped[str] = mapped_column(String(32))


class Document(Base):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str | None]
    is_embedded: Mapped[Boolean] = mapped_column(Boolean, default=False, server_default="false")
    is_tokenized: Mapped[Boolean] = mapped_column(Boolean, default=False, server_default="false")

    embedded_chunks: Mapped[list["EmbeddedChunk"]] = relationship(back_populates="document")
    tokenized_chunks: Mapped[list["TokenizedChunk"]] = relationship(back_populates="document")


class EmbeddedChunk(Base):
    __tablename__ = "embedded_chunks"

    model: Mapped[str] = mapped_column(String(128))
    start_index: Mapped[int] = mapped_column(BigInteger)
    end_index: Mapped[int] = mapped_column(BigInteger)
    serial_idx: Mapped[int] = mapped_column()
    document: Mapped["Document"] = relationship(back_populates="tokenized_chunks")

    vector: Mapped[list[float]] = mapped_column(ARRAY(Float))
    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("documents.id", name="fk_embedded_chunks_document_id"),
    )


class TokenizedChunk(Base):
    __tablename__ = "tokenized_chunks"

    model: Mapped[str] = mapped_column(String(128))
    start_index: Mapped[int] = mapped_column(BigInteger)
    end_index: Mapped[int] = mapped_column(BigInteger)
    serial_idx: Mapped[int] = mapped_column()
    document: Mapped["Document"] = relationship(back_populates="tokenized_chunks")

    tokens: Mapped[list[str]] = mapped_column(ARRAY(String))
    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("documents.id", name="fk_tokenized_chunks_document_id")
    )


class Prompt(Base):
    __tablename__ = "prompts"

    __table_args__ = (
        UniqueConstraint("template_key", name="uq_prompts_tkey"),
    )

    template_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    template: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(10), default="en")