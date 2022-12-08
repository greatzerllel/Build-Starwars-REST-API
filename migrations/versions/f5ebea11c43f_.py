"""empty message

Revision ID: f5ebea11c43f
Revises: c098b7aed53c
Create Date: 2022-12-08 18:50:50.502043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5ebea11c43f'
down_revision = 'c098b7aed53c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('edad', sa.Integer(), nullable=True),
    sa.Column('especie', sa.String(length=50), nullable=True),
    sa.Column('lugarNacimiento', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('galaxia', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=80), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favoritos_personajes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('personaje_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['personaje_id'], ['people.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favoritos_planetas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('planeta_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['planeta_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('favoritos_planetas')
    op.drop_table('favoritos_personajes')
    op.drop_table('users')
    op.drop_table('planet')
    op.drop_table('people')
    # ### end Alembic commands ###
