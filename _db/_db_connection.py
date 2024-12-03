from alembic.config import Config
from alembic import command
import os
import sqlite3
import hashlib

from utils.helpers import log_banco

_banco = './_db/_CafeGames.db'

def verificar_banco(banco=_banco):
    if not os.path.exists(banco):
        inicializar_banco()

def conectar(banco=_banco):
    log_banco("Conexão aberta")
    _conn = sqlite3.connect(banco)
    #_conn.row_factory = sqlite3.Row
    return _conn

def fechar(cursor : sqlite3):
    log_banco("Conexão encerrada")
    cursor.close()

def executar_migrations():
    alembic_cfg = Config('./alembic.ini')
    command.upgrade(alembic_cfg, "head")

def inicializar_banco():
    conexao = conectar()
    log_banco("Iniciado criação do banco")
    cursor = conexao.cursor()
    cursor.connection.autocommit = True

    executar_migrations()

    # Inserindo dados na tabela UsuarioPermissao
    usuarios_permissao = [
        (1, 0, 0, 1, 0, 0, 0, 0, 0), # Usuario padrão
        (1, 0, 1, 1, 1, 0, 1, 0, 1), # Admin
        (1, 1, 1, 1, 1, 1, 1, 1, 1)  # Master
    ]

    cursor.executemany('''
        INSERT INTO "UsuarioPermissao" ("EditarCadastro", "EditarJogo", "EditarAds", "VisualizarPerfil", "VisualizarJogo18", "VisualizarRelatorio", "VisualizarPainelAdmin", "ExcluirUsuario", "ModerarPontuacao")
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', usuarios_permissao)

    # Inserindo dados na tabela Usuario
    usuarios = [
        ('1@1.com', hashlib.md5('1'.encode()).hexdigest(), 1, '1', '1-1', '1', '2001-01-01 00:00:00'),
        ('teste@teste.com', hashlib.md5('teste'.encode()).hexdigest(), 1, 'Teste', 'Teste-teste', 'Perfil utilizado para testes do sistema', '2001-01-01 00:00:00'),
        ('moderador@cafegames.com', hashlib.md5('mod_CG_2024'.encode()).hexdigest(), 2, 'Moderador', 'Moderador', 'Perfil de moderação do sistema', '2001-01-01 00:00:00'),
        ('admin@email.com', hashlib.md5('123'.encode()).hexdigest(), 3, 'Admin', 'Admin', 'Perfil de administração do sistema', '1999-01-01 00:00:00'),
        ('marcos@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Marcos Vinicius', 'Parrrdal', 'Aooowba', '2000-01-01 00:00:00'),
        ('sanches@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Sanches', 'Sanches', 'Mestre na linguagem de programção HTML', '2000-01-01 00:00:00'),
        ('gabriel@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Gabriel', 'Pizetta', 'Deixa comigo que é sucesso!', '2000-01-01 00:00:00'),
        ('richardson@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Richardson', 'BloodMoon', 'Se vier no X1, vc vai rodar!', '2000-01-01 00:00:00'),
        ('maria@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Maria', 'Maria', 'Perfil exemplo', '2000-01-01 00:00:00'),
        ('pedro@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Pedro', 'Pedro', 'Perfil exemplo', '2000-01-01 00:00:00'),
        ('ana@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Ana', 'Ana', 'Perfil exemplo', '2000-01-01 00:00:00'),
        ('carlos@email.com', hashlib.md5('123'.encode()).hexdigest(),1,'Carlos', 'Carlos', 'Perfil exemplo', '2000-01-01 00:00:00')
    ]

    cursor.executemany('''
        INSERT INTO "Usuario" ("Email", "Senha", "IdUsuarioPermissao", "Nome", "Nick", "Descricao", "DataNascimento")
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', usuarios)

    # Inserindo dados na tabela Jogo
   
    jogos = [
        ("Snake","Icônico jogo da cobrinha, em HTML, CSS e JavaScript","capa-snakegame.png",0, 4),
        ("PacMan","A maior lenda das arcades!","capa-pacman.jpeg",0, 4),
        ("ColorBlast","Uma batalha de cores no melhor estilo space invaders","capa-colorblast.png",0, 4),
        ("BatalhaNaval","Esta pronto capitão?","capa-batalhanaval.jpg",0, 4),
        ("CampoMinado","A lenda do Windows XP","capa-campominado.png",0, 4),
        ("Dama","Único jogo com 'IA' kkkk","capa-dama.png",0, 4),
        ("Dino","Não, você não está sem internet!","capa-dino.png",0, 4),
        ("DuckHunt","Só usar o mouse como arminha","capa-duckhunt.png",0, 4),
        ("JogoDaVelha","Tem que jogar de dois!","capa-jogodavelha.png",0, 4),
        ("Xadrez","Esse é sinistro","capa-xadrez.png",0, 4),
        ("CorridaCavalo","Façam suas apostas","capa-corridacavalo.jpg",0, 4),
        ("SpaceInvaders","O clássico dos clássicos!","capa-spaceinvaders.jpg",0, 4),
    ]

    cursor.executemany('''
        INSERT INTO "Jogo" ("Nome", "Descricao", "CaminhoCapa", "FaixaEtaria", "IdUsuarioUpload")
        VALUES (?, ?, ?, ?, ?)
    ''', jogos)

    pontuacao = [
        (11,6,856099,1,3,0),
        (4,5,750000,1,3,0),
        (12,7,650000,1,3,0),
        (2,8,550000,1,3,0),
        (11,9,450000,1,3,0),
        (5,10,350000,1,3,0),
        (4,11,250000,1,3,0),
        (12,12,150000,1,3,0),
        (7,10,11900,1,3,0)
    ]

    cursor.executemany(''' 
        INSERT INTO "JogoPontuacao" ("IdJogo", "IdUsuario", "Pontuacao", "PontuacaoValida", "IdUsuarioModeracao", "Excluido")
        VALUES (?, ?, ?, ?, ?, ?)
    ''',pontuacao)

    conexao.close()


verificar_banco()