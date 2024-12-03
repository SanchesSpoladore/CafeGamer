const grade = document.getElementById('grade')
const bandeirasElemento = document.getElementById('bandeiras')
const tempoElemento = document.getElementById('tempo')
const btnReiniciar = document.getElementById('btn-reiniciar')

const TAMANHO_GRADE = 10
const QUANTIDADE_MINAS = 10

let celulas = []
let minas = []
let bandeiras = QUANTIDADE_MINAS
let tempo = 0
let jogoEncerrado = false
let intervaloTempo

function iniciarJogo() {
  celulas = []
  minas = []
  bandeiras = QUANTIDADE_MINAS
  tempo = 0
  jogoEncerrado = false
  clearInterval(intervaloTempo)

  grade.innerHTML = ''
  bandeirasElemento.textContent = `Bandeiras: ${bandeiras}`
  tempoElemento.textContent = 'Tempo: 0s'

  for (let i = 0; i < TAMANHO_GRADE * TAMANHO_GRADE; i++) {
    const celula = document.createElement('div')
    celula.classList.add('celula')
    celula.dataset.index = i
    celula.addEventListener('click', revelarCelula)
    celula.addEventListener('contextmenu', bandeirarCelula)
    grade.appendChild(celula)
    celulas.push(celula)
  }

  for (let i = 0; i < QUANTIDADE_MINAS; i++) {
    let indice
    do {
      indice = Math.floor(Math.random() * (TAMANHO_GRADE * TAMANHO_GRADE))
    } while (minas.includes(indice))
    minas.push(indice)
  }

  intervaloTempo = setInterval(() => {
    tempo++
    tempoElemento.textContent = `Tempo: ${tempo}s`
  }, 1000)
}

function revelarCelula(e) {
  if (jogoEncerrado) return
  const celula = e.target
  const indice = parseInt(celula.dataset.index)

  if (celula.classList.contains('bandeirada')) return

  if (minas.includes(indice)) {
    jogoEncerrado = true
    celula.classList.add('mina')
    revelarTodasMinas()
    clearInterval(intervaloTempo)
    alert('Game Over! Você perdeu!')
  } else {
    const quantidadeMinas = contarMinasAdjacentes(indice)
    celula.classList.add('revelada')
    if (quantidadeMinas > 0) {
      celula.textContent = quantidadeMinas
    } else {
      revelarCelulasAdjacentes(indice)
    }
  }

  verificarVitoria()
}

function bandeirarCelula(e) {
  e.preventDefault()
  if (jogoEncerrado) return
  const celula = e.target

  if (!celula.classList.contains('revelada')) {
    celula.classList.toggle('bandeirada')
    if (celula.classList.contains('bandeirada')) {
      bandeiras--
    } else {
      bandeiras++
    }
    bandeirasElemento.textContent = `Bandeiras: ${bandeiras}`
  }

  verificarVitoria()
}

function contarMinasAdjacentes(indice) {
  let count = 0
  const celulasAdjacentes = obterCelulasAdjacentes(indice)
  for (const indiceCelula of celulasAdjacentes) {
    if (minas.includes(indiceCelula)) {
      count++
    }
  }
  return count
}

function obterCelulasAdjacentes(indice) {
  const linha = Math.floor(indice / TAMANHO_GRADE)
  const coluna = indice % TAMANHO_GRADE
  const celulasAdjacentes = []

  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      const novaLinha = linha + i
      const novaColuna = coluna + j
      if (
        novaLinha >= 0 &&
        novaLinha < TAMANHO_GRADE &&
        novaColuna >= 0 &&
        novaColuna < TAMANHO_GRADE
      ) {
        celulasAdjacentes.push(novaLinha * TAMANHO_GRADE + novaColuna)
      }
    }
  }

  return celulasAdjacentes
}

function revelarCelulasAdjacentes(indice) {
  const celulasAdjacentes = obterCelulasAdjacentes(indice)
  for (const indiceCelula of celulasAdjacentes) {
    const celula = celulas[indiceCelula]
    if (
      !celula.classList.contains('revelada') &&
      !celula.classList.contains('bandeirada')
    ) {
      const quantidadeMinas = contarMinasAdjacentes(indiceCelula)
      celula.classList.add('revelada')
      if (quantidadeMinas > 0) {
        celula.textContent = quantidadeMinas
      } else {
        revelarCelulasAdjacentes(indiceCelula)
      }
    }
  }
}

function revelarTodasMinas() {
  for (const indice of minas) {
    celulas[indice].classList.add('mina')
  }
}

function verificarVitoria() {
  const quantidadeRevelada =
    document.querySelectorAll('.celula.revelada').length
  const minasBandeiradas = minas.filter((indice) =>
    celulas[indice].classList.contains('bandeirada')
  ).length

  if (
    quantidadeRevelada === TAMANHO_GRADE * TAMANHO_GRADE - QUANTIDADE_MINAS &&
    minasBandeiradas === QUANTIDADE_MINAS
  ) {
    jogoEncerrado = true
    clearInterval(intervaloTempo)
    alert(`Parabéns! Você venceu em ${tempo} segundos!`)
  }
}

btnReiniciar.addEventListener('click', iniciarJogo)

iniciarJogo()
