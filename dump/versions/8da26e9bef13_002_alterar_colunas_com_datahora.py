"""Alterar colunas com datahora

Revision ID: 8da26e9bef13
Revises: c6935689d948
Create Date: 2024-11-03 22:31:22.251239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8da26e9bef13'
down_revision: Union[str, None] = 'c6935689d948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(): 
    op.create_table(
        'Ads_tmp',
        sa.Column('IdAds', sa.Integer, primary_key=True),
        sa.Column('DataCadastro', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('DataInicio', sa.TIMESTAMP(timezone=True), nullable=True, server_default=sa.text("CURRENT_TIMESTAMP")),
        # Outras colunas de `Ads` devem ser incluídas aqui
    )

    op.execute('INSERT INTO Ads_tmp (IdAds, DataCadastro, DataInicio) SELECT IdAds, DataCadastro, DataInicio FROM Ads')
    op.drop_table('Ads')
    op.rename_table('Ads_tmp', 'Ads')


def downgrade():
    # Reverter para a tabela `Ads`
    op.create_table(
        'Ads_tmp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('DataCadastro', sa.TIMESTAMP(), nullable=False),
        sa.Column('DataInicio', sa.TIMESTAMP(), nullable=True),
        # Outras colunas de `Ads` devem ser incluídas aqui
    )

    op.execute('INSERT INTO Ads_tmp (IdAds, DataCadastro, DataInicio) SELECT IdAds, DataCadastro, DataInicio FROM Ads')
    op.drop_table('Ads')
    op.rename_table('Ads_tmp', 'Ads')