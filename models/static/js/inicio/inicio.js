const pontuacoes = [
  {
    nome: 'Sanches Spoladore',
    imagemUrl: '/static/img/inicio/capa-corridacavalo.jpg',
    pontos: 856099,
    tempo: '2 mins',
  },
  {
    nome: 'Marcos Vinicius',
    imagemUrl: '/static/img/inicio/capa-batalhanaval.jpg',
    pontos: 750000,
    tempo: '5 mins',
  },
  {
    nome: 'Gabriel',
    imagemUrl: '/static/img/inicio/capa-spaceinverds.jpg',
    pontos: 650000,
    tempo: '8 mins',
  },
  {
    nome: 'Richardson',
    imagemUrl: '/static/img/inicio/capa-pacman.jpeg',
    pontos: 550000,
    tempo: '10 mins',
  },
  {
    nome: 'Maria',
    imagemUrl: '/static/img/inicio/capa-corridacavalo.jpg',
    pontos: 450000,
    tempo: '15 mins',
  },
  {
    nome: 'Pedro',
    imagemUrl: '/static/img/inicio/capa-campominado.jpg',
    pontos: 350000,
    tempo: '20 mins',
  },
  {
    nome: 'Ana',
    imagemUrl: '/static/img/inicio/capa-batalhanaval.jpg',
    pontos: 250000,
    tempo: '25 mins',
  },
  {
    nome: 'Carlos',
    imagemUrl: '/static/img/inicio/capa-spaceinverds.jpg',
    pontos: 150000,
    tempo: '30 mins',
  },
]

function criarItensCarrossel() {
  const carrossel = document.getElementById('carrossel')
  pontuacoes.forEach((pontuacao) => {
    const elementoPontuacao = document.createElement('div')
    elementoPontuacao.className = 'pontuacao'
    elementoPontuacao.innerHTML = `
      <div class="pontuacao-conteudo">
        <div class="pontuacao-header">
          <h3>${pontuacao.nome}</h3>
          <img src="${pontuacao.imagemUrl}" alt="${pontuacao.nome}">
        </div>
        <div class="pontuacao-footer">
          <p>${pontuacao.pontos.toLocaleString()} Pontos</p>
          <span>${pontuacao.tempo}</span>
        </div>
      </div>
    `
    carrossel.appendChild(elementoPontuacao)
  })
}

function obterItensVisiveis() {
  const larguraContainer = document.querySelector(
    '.carrossel-container'
  ).offsetWidth
  const larguraItem = document.querySelector('.pontuacao').offsetWidth
  return Math.floor(larguraContainer / larguraItem)
}

function configurarCarrossel() {
  const carrossel = document.getElementById('carrossel')
  let indiceAtual = 0
  let itensVisiveis = obterItensVisiveis()

  function moverCarrossel() {
    const larguraItem = carrossel.children[0].offsetWidth
    const maxIndice = carrossel.children.length - itensVisiveis

    if (indiceAtual < maxIndice) {
      indiceAtual++
    } else {
      indiceAtual = 0
      carrossel.style.transition = 'none'
      carrossel.style.transform = 'translateX(0)'
      setTimeout(() => {
        carrossel.style.transition = 'transform 1s ease-in-out'
      }, 50)
    }

    carrossel.style.transform = `translateX(-${indiceAtual * larguraItem}px)`
  }

  setInterval(moverCarrossel, 3000)

  window.addEventListener('resize', () => {
    itensVisiveis = obterItensVisiveis()
    indiceAtual = 0
    carrossel.style.transition = 'none'
    carrossel.style.transform = 'translateX(0)'
    setTimeout(() => {
      carrossel.style.transition = 'transform 1s ease-in-out'
    }, 50)
  })
}

document.addEventListener('DOMContentLoaded', () => {
  criarItensCarrossel()
  configurarCarrossel()
})

const botaoMenu = document.getElementById('menu-btn')
const menuPrincipal = document.getElementById('menu-principal')
const botaoPerfil = document.getElementById('perfil-btn')
const menuPerfil = document.getElementById('menu-perfil')

function alternarMenu(menu) {
  if (menu === 'principal') {
    menuPrincipal.classList.toggle('ativo')
    if (menuPerfil.classList.contains('ativo')) {
      menuPerfil.classList.remove('ativo')
    }
  } else if (menu === 'perfil') {
    menuPerfil.classList.toggle('ativo')
    if (menuPrincipal.classList.contains('ativo')) {
      menuPrincipal.classList.remove('ativo')
    }
  }
}

botaoMenu.addEventListener('click', () => alternarMenu('principal'))
botaoPerfil.addEventListener('click', () => alternarMenu('perfil'))
