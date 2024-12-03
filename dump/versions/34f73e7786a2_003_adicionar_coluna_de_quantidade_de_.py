"""Adicionar coluna de quantidade de acessos do jogo

Revision ID: 34f73e7786a2
Revises: 8da26e9bef13
Create Date: 2024-11-12 23:24:19.172094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34f73e7786a2'
down_revision: Union[str, None] = '8da26e9bef13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Adiciona a coluna QtdeAcessos na tabela Jogo
    op.add_column('Jogo', sa.Column('QtdeAcessos', sa.Integer, nullable=False, server_default="0"))

    # Remove a coluna IdUsuario da tabela JogoPontuacao
    #op.drop_column('JogoPontuacao', 'IdUsuario')


def downgrade():
    # Reverte as mudanças feitas no upgrade

    # Remove a coluna QtdeAcessos da tabela Jogo
    op.drop_column('Jogo', 'QtdeAcessos')

    # Adiciona de volta a coluna IdUsuario na tabela JogoPontuacao
    #op.add_column('JogoPontuacao', sa.Column('IdUsuario', sa.Integer, nullable=True))
