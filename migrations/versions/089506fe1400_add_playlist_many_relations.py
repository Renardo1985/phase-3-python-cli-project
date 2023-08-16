"""add playlist Many relations

Revision ID: 089506fe1400
Revises: a8db355b37de
Create Date: 2023-08-15 17:15:24.937360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '089506fe1400'
down_revision: Union[str, None] = 'a8db355b37de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist_songs',
    sa.Column('songs_id', sa.Integer(), nullable=True),
    sa.Column('playlist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlists.id'], ),
    sa.ForeignKeyConstraint(['songs_id'], ['songs.id'], )
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(), nullable=True))

    op.drop_table('playlist_songs')
    # ### end Alembic commands ###