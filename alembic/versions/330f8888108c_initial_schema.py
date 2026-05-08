"""initial schema

Revision ID: 330f8888108c
Revises:
Create Date: 2026-05-08 02:41:18.979372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '330f8888108c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table('projects',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('vault_path', sa.Text(), nullable=False),
    sa.Column('active_style_id', sa.UUID(), nullable=True),
    sa.Column('target_word_count', sa.Integer(), nullable=True),
    sa.Column('genre_tags', sa.ARRAY(sa.Text()), nullable=True),
    sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('style_profiles',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('reference_samples', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('params', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('prompt_overrides', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('extracted_features', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('world_entries',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('category', sa.Text(), nullable=False),
    sa.Column('parent_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('content_md', sa.Text(), nullable=True),
    sa.Column('frontmatter', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('links', sa.ARRAY(sa.UUID()), nullable=True),
    sa.Column('obsidian_path', sa.Text(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['world_entries.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_world_project_category', 'world_entries', ['project_id', 'category'], unique=False)

    op.create_table('characters',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('role', sa.Text(), nullable=True),
    sa.Column('profile', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('language_samples', sa.ARRAY(sa.Text()), nullable=True),
    sa.Column('arc', sa.Text(), nullable=True),
    sa.Column('current_status', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('obsidian_path', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('character_relations',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('from_char', sa.UUID(), nullable=True),
    sa.Column('to_char', sa.UUID(), nullable=True),
    sa.Column('relation_type', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['from_char'], ['characters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_char'], ['characters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('from_char', 'to_char', 'relation_type', name='uq_char_relation')
    )

    op.create_table('outlines',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('level', sa.Text(), nullable=False),
    sa.Column('parent_id', sa.UUID(), nullable=True),
    sa.Column('sequence', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('content_md', sa.Text(), nullable=True),
    sa.Column('scenes', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('characters_involved', sa.ARRAY(sa.UUID()), nullable=True),
    sa.Column('plot_threads_involved', sa.ARRAY(sa.UUID()), nullable=True),
    sa.Column('expected_words', sa.Integer(), nullable=True),
    sa.Column('arc_position', sa.Text(), nullable=True),
    sa.Column('obsidian_path', sa.Text(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['outlines.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_outline_project_level', 'outlines', ['project_id', 'level', 'sequence'], unique=False)

    op.create_table('chapters',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('outline_id', sa.UUID(), nullable=True),
    sa.Column('sequence', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('content_md', sa.Text(), nullable=True),
    sa.Column('word_count', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('current_version', sa.Integer(), nullable=True),
    sa.Column('obsidian_path', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['outline_id'], ['outlines.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('chapter_versions',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('chapter_id', sa.UUID(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('content_md', sa.Text(), nullable=True),
    sa.Column('diff_summary', sa.Text(), nullable=True),
    sa.Column('source', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chapter_id', 'version', name='uq_chapter_version')
    )

    op.create_table('chapter_summaries',
    sa.Column('chapter_id', sa.UUID(), nullable=False),
    sa.Column('summary_md', sa.Text(), nullable=True),
    sa.Column('key_events', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('character_changes', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('plot_thread_updates', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('chapter_id')
    )

    op.create_table('plot_threads',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('planted_chapter', sa.UUID(), nullable=True),
    sa.Column('planned_resolve_chapter', sa.UUID(), nullable=True),
    sa.Column('resolved_chapter', sa.UUID(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('importance', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['planned_resolve_chapter'], ['chapters.id'], ),
    sa.ForeignKeyConstraint(['planted_chapter'], ['chapters.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resolved_chapter'], ['chapters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('prompts',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('scope', sa.Text(), nullable=False),
    sa.Column('module', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_prompts_lookup', 'prompts', ['project_id', 'scope', 'module', 'is_active'], unique=False)

    op.create_table('simulations',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('mode', sa.Text(), nullable=False),
    sa.Column('setup', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('transcript', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('saved_as_material', sa.Boolean(), nullable=True),
    sa.Column('material_path', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('quality_checks',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('chapter_id', sa.UUID(), nullable=True),
    sa.Column('chapter_version', sa.Integer(), nullable=True),
    sa.Column('round', sa.Integer(), nullable=False),
    sa.Column('round_name', sa.Text(), nullable=True),
    sa.Column('model_used', sa.Text(), nullable=True),
    sa.Column('issues', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('raw_response', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('ai_calls',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('module', sa.Text(), nullable=True),
    sa.Column('model', sa.Text(), nullable=True),
    sa.Column('prompt_tokens', sa.Integer(), nullable=True),
    sa.Column('completion_tokens', sa.Integer(), nullable=True),
    sa.Column('cost_usd', sa.Numeric(precision=10, scale=6), nullable=True),
    sa.Column('latency_ms', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_calls_project_date', 'ai_calls', ['project_id', 'created_at'], unique=False)

    op.create_table('embeddings',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('source_type', sa.Text(), nullable=False),
    sa.Column('source_id', sa.UUID(), nullable=False),
    sa.Column('chunk_index', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=1024), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_embeddings_project_type', 'embeddings', ['project_id', 'source_type'], unique=False)
    op.execute('CREATE INDEX idx_embeddings_vector ON embeddings USING hnsw (embedding vector_cosine_ops);')

    op.create_table('inspirations',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('tags', sa.ARRAY(sa.Text()), nullable=True),
    sa.Column('used_in_chapter', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['used_in_chapter'], ['chapters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    pass
