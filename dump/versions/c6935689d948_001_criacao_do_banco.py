"""Criacao do banco

Revision ID: c6935689d948
Revises: 
Create Date: 2024-10-29 20:22:37.514637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6935689d948'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criação da tabela UsuarioPermissao
    op.create_table(
        "UsuarioPermissao",
        sa.Column("IdUsuarioPermissao", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("EditarCadastro", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("EditarJogo", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("EditarAds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("VisualizarPerfil", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("VisualizarJogo18", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("VisualizarRelatorio", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("VisualizarPainelAdmin", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ExcluirUsuario", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ModerarPontuacao", sa.Integer(), nullable=False, server_default="0")
    )

    # Criação da tabela Usuario
    op.create_table(
        "Usuario",
        sa.Column("IdUsuario", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("Email", sa.String(200), nullable=False),
        sa.Column("Senha", sa.String(200), nullable=False),
        sa.Column("IdUsuarioPermissao", sa.Integer(), sa.ForeignKey("UsuarioPermissao.IdUsuarioPermissao"), nullable=False),
        sa.Column("Nome", sa.String(200), nullable=False),
        sa.Column("Nick", sa.String(200)),
        sa.Column("Descricao", sa.Text()),
        sa.Column("Telefone", sa.String(20)),
        sa.Column("CaminhoFoto", sa.String(200)),
        sa.Column("DataCadastro", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("DataNascimento", sa.TIMESTAMP(timezone=True)),
        sa.Column("DataUltimoLogin", sa.TIMESTAMP(timezone=True)),
        sa.Column("Ativo", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("Excluido", sa.Integer(), nullable=False, server_default="0")
    )

    # Criação da tabela Jogo
    op.create_table(
        "Jogo",
        sa.Column("IdJogo", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("Nome", sa.String(200), nullable=False),
        sa.Column("Descricao", sa.Text(), nullable=False),
        sa.Column("CaminhoCapa", sa.Text(), nullable=False),
        sa.Column("FaixaEtaria", sa.Integer(), nullable=False),
        sa.Column("IdUsuarioUpload", sa.Integer(), sa.ForeignKey("Usuario.IdUsuario"), nullable=False),
        sa.Column("DataCadastro", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("DataUltimaAtualizacao", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("DataUltimoAcesso", sa.TIMESTAMP(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("QtdeCurtida", sa.Integer(), server_default="0"),
        sa.Column("IdJogoPontuacao", sa.Integer(), sa.ForeignKey("JogoPontuacao.IdJogoPontuacao")),
        sa.Column("MaiorPontuacao", sa.Integer(), server_default="0"),
        sa.Column("IdUsuarioMaiorPontuacao", sa.Integer(), sa.ForeignKey("Usuario.IdUsuario")),
        sa.Column("Excluido", sa.Integer(), nullable=False, server_default="0")
    )

    # Criação da tabela JogoPontuacao
    op.create_table(
        "JogoPontuacao",
        sa.Column("IdJogoPontuacao", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("IdJogo", sa.Integer(), sa.ForeignKey("Jogo.IdJogo"), nullable=False),
        sa.Column("IdUsuario", sa.Integer(), sa.ForeignKey("Usuario.IdUsuario"), nullable=False),
        sa.Column("Pontuacao", sa.Numeric(20, 5), nullable=False, server_default="0.0"),
        sa.Column("DataPontuacao", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("PontuacaoValida", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("IdUsuarioModeracao", sa.Integer(), sa.ForeignKey("Usuario.IdUsuario")),
        sa.Column("Excluido", sa.Integer(), nullable=False, server_default="0")
    )

    # Criação da tabela Ads
    op.create_table(
        "Ads",
        sa.Column("IdAds", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("IdUsuario", sa.Integer(), sa.ForeignKey("Usuario.IdUsuario"), nullable=False),
        sa.Column("DataCadastro", sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("DataInicio", sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("DataFinal", sa.TIMESTAMP(), nullable=False, server_default=sa.text("(datetime('now', '+15 days'))")),
        sa.Column("Ativo", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("QtdeClique", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("Excluido", sa.Integer(), nullable=False, server_default="0")
    )


def downgrade() -> None:
    op.drop_table("Ads")
    op.drop_table("JogoPontuacao")
    op.drop_table("Jogo")
    op.drop_table("Usuario")
    op.drop_table("UsuarioPermissao")


