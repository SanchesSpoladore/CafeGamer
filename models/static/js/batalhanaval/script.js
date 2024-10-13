const telaInicial = document.getElementById('tela-inicial')
const telaDoJogo = document.getElementById('tela-do-jogo')
const botaoIniciar = document.getElementById('botao-iniciar')
const botaoReiniciar = document.getElementById('botao-reiniciar')
const tabuleiroDeJogo = document.getElementById('tabuleiro-de-jogo')
const statusDoNavio = document.getElementById('status-do-navio')
const tamanhoDoTabuleiro = 8
const modalDoJogo = document.getElementById('modal-do-jogo')
const tituloModal = document.getElementById('titulo-modal')
const mensagemModal = document.getElementById('mensagem-modal')
const botaoJogarNovamente = document.getElementById('botao-jogar-novamente')
const fecharModal = document.getElementById('fechar-modal')

const tiposDeNavio = {
  portaAvioes: {
    tamanho: 5,
    quantidade: 1,
    pontos: 15,
    icone: '🚢',
    nome: 'Porta-aviões',
  },
  navioTanque: {
    tamanho: 4,
    quantidade: 4,
    pontos: 10,
    icone: '⛴️',
    nome: 'Navio-tanque',
  },
  contratorpedeiro: {
    tamanho: 3,
    quantidade: 6,
    pontos: 6,
    icone: '🚤',
    nome: 'Contratorpedeiro',
  },
  submarino: {
    tamanho: 2,
    quantidade: 8,
    pontos: 5,
    icone: '🌊',
    nome: 'Submarino',
  },
}

let tabuleiro = []
let navios = []
let naviosRestantes = {}
let pontos = 100
const displayPontos = document.createElement('div')

botaoIniciar.addEventListener('click', iniciarJogo)
botaoReiniciar.addEventListener('click', reiniciarJogo)
botaoJogarNovamente.addEventListener('click', reiniciarJogo)
fecharModal.addEventListener('click', () => modalDoJogo.classList.add('oculto'))

function iniciarJogo() {
  telaInicial.classList.add('oculto')
  telaDoJogo.classList.remove('oculto')
  inicializarJogo()
}

function reiniciarJogo() {
  telaDoJogo.classList.add('oculto')
  telaInicial.classList.remove('oculto')
  modalDoJogo.classList.add('oculto')
  pontos = 100
  window.location.reload()
}

function fecharModalFuncao() {
  modalDoJogo.classList.add('oculto')
  reiniciarJogo()
}

function inicializarJogo() {
  tiposDeNavio.navioTanque.quantidade = tiposDeNavio.navioTanque.quantidade - 3
  tiposDeNavio.contratorpedeiro.quantidade =
    tiposDeNavio.contratorpedeiro.quantidade - 5
  tiposDeNavio.submarino.quantidade = tiposDeNavio.submarino.quantidade - 7

  tabuleiro = Array(tamanhoDoTabuleiro)
    .fill()
    .map(() => Array(tamanhoDoTabuleiro).fill(null))
  navios = []
  naviosRestantes = Object.fromEntries(
    Object.entries(tiposDeNavio).map(([chave, valor]) => [
      chave,
      valor.quantidade,
    ])
  )

  for (const [tipoDeNavio, infoDoNavio] of Object.entries(tiposDeNavio)) {
    for (let i = 0; i < infoDoNavio.quantidade; i++) {
      colocarNavio(tipoDeNavio, infoDoNavio.tamanho)
    }
  }

  console.log('Matriz do Tabuleiro:')
  console.table(tabuleiro)

  tabuleiroDeJogo.innerHTML = ''
  for (let y = 0; y < tamanhoDoTabuleiro; y++) {
    for (let x = 0; x < tamanhoDoTabuleiro; x++) {
      const celula = document.createElement('div')
      celula.classList.add('celula')
      celula.dataset.x = x
      celula.dataset.y = y
      celula.addEventListener('click', lidarComCliqueNaCelula)
      tabuleiroDeJogo.appendChild(celula)
    }
  }

  atualizarStatusDosNavios()
  atualizarPontos()
  telaDoJogo.appendChild(displayPontos)
}

function colocarNavio(tipoDeNavio, tamanho) {
  let x, y, direcao
  do {
    x = Math.floor(Math.random() * tamanhoDoTabuleiro)
    y = Math.floor(Math.random() * tamanhoDoTabuleiro)
    direcao = Math.random() < 0.5 ? 'horizontal' : 'vertical'
  } while (!podeColocarNavio(x, y, tamanho, direcao))

  for (let i = 0; i < tamanho; i++) {
    if (direcao === 'horizontal') {
      tabuleiro[y][x + i] = tipoDeNavio
    } else {
      tabuleiro[y + i][x] = tipoDeNavio
    }
  }
  navios.push({ tipo: tipoDeNavio, acertos: 0, tamanho })
}

function podeColocarNavio(x, y, tamanho, direcao) {
  if (direcao === 'horizontal' && x + tamanho > tamanhoDoTabuleiro) return false
  if (direcao === 'vertical' && y + tamanho > tamanhoDoTabuleiro) return false

  for (let i = 0; i < tamanho; i++) {
    if (direcao === 'horizontal') {
      if (tabuleiro[y][x + i] !== null) return false
    } else {
      if (tabuleiro[y + i][x] !== null) return false
    }
  }
  return true
}

function lidarComCliqueNaCelula(event) {
  const x = parseInt(event.target.dataset.x)
  const y = parseInt(event.target.dataset.y)

  if (
    event.target.classList.contains('acerto') ||
    event.target.classList.contains('erro')
  ) {
    return
  }

  if (tabuleiro[y][x]) {
    const tipoDeNavio = tabuleiro[y][x]
    event.target.classList.add('acerto')
    event.target.textContent = tiposDeNavio[tipoDeNavio].icone

    const navioAcertado = navios.find((navio) => navio.tipo === tipoDeNavio)
    navioAcertado.acertos++

    pontos += tiposDeNavio[tipoDeNavio].pontos
    const audioExplosao = new Audio('/static/audio/batalhanaval/explosao.mp3')
    audioExplosao.play()
    setTimeout(() => {
      audioExplosao.pause()
    }, 2000)
    atualizarPontos()

    if (navioAcertado.acertos === navioAcertado.tamanho) {
      naviosRestantes[tipoDeNavio]--
      console.log('Navios Restantes:', naviosRestantes) // Log para depuração
      atualizarStatusDosNavios()
    }

    if (verificarVitoria()) {
      mostrarModal('Você ganhou', 'Parabéns! Você afundou todos os navios!')
    }
  } else {
    event.target.classList.add('erro')
    event.target.textContent = '💦'
    if (pontos >= 10) {
      pontos -= 10
    } else {
      pontos = 0
    }
    const audioAgua = new Audio('/static/audio/batalhanaval/agua.mp3')
    audioAgua.currentTime = 1
    audioAgua.play()
    setTimeout(() => {
      audioAgua.pause()
    }, 2000)
    atualizarPontos()
    if (pontos <= 0) {
      mostrarModal('Você perdeu', 'Você perdeu! Seus pontos acabaram.')
    }
  }
}

function verificarVitoria() {
  return navios.every((navio) => navio.acertos === navio.tamanho)
}

function mostrarModal(titulo, mensagem) {
  tituloModal.innerHTML = titulo
  mensagemModal.innerHTML = mensagem
  modalDoJogo.classList.remove('oculto')
}

function atualizarPontos() {
  displayPontos.textContent = `Pontos: ${pontos}`
  displayPontos.id = 'display-pontos'
}

function atualizarStatusDosNavios() {
  statusDoNavio.innerHTML = ''
  for (const [tipoDeNavio, infoDoNavio] of Object.entries(tiposDeNavio)) {
    const elementoNavio = document.createElement('div')
    elementoNavio.classList.add('info-do-navio')
    elementoNavio.innerHTML = `
            <span class="icone-do-navio">${infoDoNavio.icone}</span>
            <span>${naviosRestantes[tipoDeNavio]}</span>
        `
    statusDoNavio.appendChild(elementoNavio)
  }
}

window.addEventListener('load', () => {
  telaDoJogo.classList.add('oculto')
})
