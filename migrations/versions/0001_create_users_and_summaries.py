from alembic import op
import sqlalchemy as sa

revision = '0001_users_summaries'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=260), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_user'),
        sa.UniqueConstraint('email', name='uq_user_email'),
    )
    op.create_table(
        'summary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('original_text', sa.Text(), nullable=False),
        sa.Column('summary_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_summary_user_id_user', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='pk_summary')
    )


def downgrade():
    op.drop_table('summary')
    op.drop_table('user')
