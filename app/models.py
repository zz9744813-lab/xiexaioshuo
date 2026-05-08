from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pgvector.sqlalchemy

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    vault_path = Column(Text, nullable=False)
    active_style_id = Column(UUID(as_uuid=True))
    target_word_count = Column(Integer)
    genre_tags = Column(ARRAY(Text))
    settings = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class StyleProfile(Base):
    __tablename__ = 'style_profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(Text, nullable=False)
    reference_samples = Column(JSONB)
    params = Column(JSONB)
    prompt_overrides = Column(JSONB)
    extracted_features = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorldEntry(Base):
    __tablename__ = 'world_entries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    category = Column(Text, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('world_entries.id'))
    name = Column(Text, nullable=False)
    content_md = Column(Text)
    frontmatter = Column(JSONB, default=dict)
    links = Column(ARRAY(UUID(as_uuid=True)))
    obsidian_path = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_world_project_category', 'project_id', 'category'),
    )

class Character(Base):
    __tablename__ = 'characters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(Text, nullable=False)
    role = Column(Text)
    profile = Column(JSONB)
    language_samples = Column(ARRAY(Text))
    arc = Column(Text)
    current_status = Column(JSONB, default=dict)
    obsidian_path = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class CharacterRelation(Base):
    __tablename__ = 'character_relations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_char = Column(UUID(as_uuid=True), ForeignKey('characters.id', ondelete='CASCADE'))
    to_char = Column(UUID(as_uuid=True), ForeignKey('characters.id', ondelete='CASCADE'))
    relation_type = Column(Text)
    description = Column(Text)

    __table_args__ = (
        UniqueConstraint('from_char', 'to_char', 'relation_type', name='uq_char_relation'),
    )

class Outline(Base):
    __tablename__ = 'outlines'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    level = Column(Text, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('outlines.id'))
    sequence = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    content_md = Column(Text)
    scenes = Column(JSONB)
    characters_involved = Column(ARRAY(UUID(as_uuid=True)))
    plot_threads_involved = Column(ARRAY(UUID(as_uuid=True)))
    expected_words = Column(Integer)
    arc_position = Column(Text)
    obsidian_path = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_outline_project_level', 'project_id', 'level', 'sequence'),
    )

class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    outline_id = Column(UUID(as_uuid=True), ForeignKey('outlines.id'))
    sequence = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    content_md = Column(Text)
    word_count = Column(Integer, default=0)
    status = Column(Text, default='draft')
    current_version = Column(Integer, default=1)
    obsidian_path = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ChapterVersion(Base):
    __tablename__ = 'chapter_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey('chapters.id', ondelete='CASCADE'))
    version = Column(Integer, nullable=False)
    content_md = Column(Text)
    diff_summary = Column(Text)
    source = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('chapter_id', 'version', name='uq_chapter_version'),
    )

class ChapterSummary(Base):
    __tablename__ = 'chapter_summaries'

    chapter_id = Column(UUID(as_uuid=True), ForeignKey('chapters.id', ondelete='CASCADE'), primary_key=True)
    summary_md = Column(Text)
    key_events = Column(JSONB)
    character_changes = Column(JSONB)
    plot_thread_updates = Column(JSONB)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

class PlotThread(Base):
    __tablename__ = 'plot_threads'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(Text, nullable=False)
    description = Column(Text)
    planted_chapter = Column(UUID(as_uuid=True), ForeignKey('chapters.id'))
    planned_resolve_chapter = Column(UUID(as_uuid=True), ForeignKey('chapters.id'))
    resolved_chapter = Column(UUID(as_uuid=True), ForeignKey('chapters.id'))
    status = Column(Text, default='planted')
    importance = Column(Integer, default=3)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    scope = Column(Text, nullable=False)
    module = Column(Text)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    metadata_ = Column('metadata', JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_prompts_lookup', 'project_id', 'scope', 'module', 'is_active'),
    )

class Simulation(Base):
    __tablename__ = 'simulations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    mode = Column(Text, nullable=False)
    setup = Column(JSONB)
    transcript = Column(JSONB)
    saved_as_material = Column(Boolean, default=False)
    material_path = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QualityCheck(Base):
    __tablename__ = 'quality_checks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey('chapters.id', ondelete='CASCADE'))
    chapter_version = Column(Integer)
    round = Column(Integer, nullable=False)
    round_name = Column(Text)
    model_used = Column(Text)
    issues = Column(JSONB)
    score = Column(Integer)
    raw_response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AICall(Base):
    __tablename__ = 'ai_calls'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'))
    module = Column(Text)
    model = Column(Text)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    cost_usd = Column(Numeric(10, 6))
    latency_ms = Column(Integer)
    status = Column(Text)
    error = Column(Text)
    metadata_ = Column('metadata', JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_ai_calls_project_date', 'project_id', 'created_at'),
    )

class Embedding(Base):
    __tablename__ = 'embeddings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'))
    source_type = Column(Text, nullable=False)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    chunk_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)
    embedding = Column(pgvector.sqlalchemy.Vector(1024))
    metadata_ = Column('metadata', JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_embeddings_project_type', 'project_id', 'source_type'),
        Index('idx_embeddings_vector', 'embedding', postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'embedding': 'vector_cosine_ops'}),
    )

class Inspiration(Base):
    __tablename__ = 'inspirations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'))
    content = Column(Text)
    tags = Column(ARRAY(Text))
    used_in_chapter = Column(UUID(as_uuid=True), ForeignKey('chapters.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
