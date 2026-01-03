from typing import Optional
from sqlalchemy import (
    ARRAY,
    Float,
    String,
    ForeignKey,
    BigInteger,
    Text,
    UniqueConstraint,
    Integer,
    Boolean,
)
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
    password_hash: Mapped[bytes]
    isActive: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    role: Mapped[str] = mapped_column(String(32))

    documents: Mapped[list["Document"]] = relationship(back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, default="")

    s3_object_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    source_url: Mapped[str] = mapped_column(String(512), nullable=False)
    media_type: Mapped[str] = mapped_column(String(100), nullable=False)

    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document")
    user: Mapped["User"] = relationship(back_populates="documents")

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", name="fk_document_user_id")
    )


class Chunk(Base):
    __tablename__ = "chunks"

    start_index: Mapped[int] = mapped_column(BigInteger)
    end_index: Mapped[int] = mapped_column(BigInteger)
    serial_idx: Mapped[int] = mapped_column()
    document: Mapped["Document"] = relationship(back_populates="chunks")
    vector: Mapped[Optional["ChunkVector"]] = relationship(back_populates="chunk")
    tokens: Mapped[Optional["ChunkTokens"]] = relationship(back_populates="chunk")

    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("documents.id", name="fk_embedded_chunks_document_id"),
    )


class ChunkVector(Base):
    __tablename__ = "chunk_vector"

    vector: Mapped[list[float]] = mapped_column(ARRAY(Float))
    model: Mapped[str] = mapped_column(String(128))

    chunk: Mapped["Chunk"] = relationship(back_populates="vector")

    chunk_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("chunks.id", name="fk_chunk_vector_chunk_id"),
    )


class ChunkTokens(Base):
    __tablename__ = "chunk_tokens"

    tokens: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    model: Mapped[str] = mapped_column(String(128))

    chunk: Mapped["Chunk"] = relationship(back_populates="tokens")

    chunk_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("chunks.id", name="fk_chunk_tokens_chunk_id"),
    )


class Prompt(Base):
    __tablename__ = "prompts"

    __table_args__ = (UniqueConstraint("template_key", name="uq_prompts_tkey"),)

    template_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    template: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(10), default="en")
