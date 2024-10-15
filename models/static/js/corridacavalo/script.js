let carteira = 500
const valorCarteiraMostrado = document.getElementById('valorCarteira')
const resultado = document.getElementById('resultado')
const cavalos = ['cavalo1', 'cavalo2', 'cavalo3', 'cavalo4', 'cavalo5']
const nomeCavalos = {
  cavalo1: 'Trovão',
  cavalo2: 'Tempestade',
  cavalo3: 'Relâmpago',
  cavalo4: 'Chama',
  cavalo5: 'Sombra',
}
let corridaEmAndamento = false

function atualizarCarteira() {
  valorCarteiraMostrado.innerText = carteira
}

function iniciarCorrida() {
  if (corridaEmAndamento) return
  const valorAposta = parseInt(document.getElementById('valorAposta').value)
  const cavaloSelecionado = document.getElementById('cavaloSelecionado').value
  if (isNaN(valorAposta) || valorAposta <= 0 || valorAposta > carteira) {
    resultado.textContent = 'Por favor, insira um valor de aposta válido!'
    return
  }
  carteira -= valorAposta
  atualizarCarteira()
  corridaEmAndamento = true
  resultado.textContent = 'A corrida começou!'
  cavalos.forEach((cavalo) => {
    document.getElementById(cavalo).style.left = '0px'
    document.getElementById(cavalo).style.top = `${
      (parseInt(cavalo.slice(-1)) - 1) * 60
    }px`
  })
  const larguraMaximaPista = document.getElementById('pista').offsetWidth - 60
  let intervaloCorrida = setInterval(function () {
    let algumCavaloGanhou = false
    cavalos.forEach((cavalo) => {
      let posicao = parseInt(document.getElementById(cavalo).style.left) || 0
      posicao += Math.random() * 10
      document.getElementById(cavalo).style.left = `${posicao}px`
      if (posicao >= larguraMaximaPista) {
        clearInterval(intervaloCorrida)
        corridaEmAndamento = false
        algumCavaloGanhou = true
        finalizarCorrida(cavalo, cavaloSelecionado, valorAposta)
      }
    })
    if (algumCavaloGanhou) {
      clearInterval(intervaloCorrida)
    }
  }, 50)
}

function finalizarCorrida(vencedor, selecionado, aposta) {
  if (vencedor === selecionado) {
    const ganhos = aposta * 2
    carteira += ganhos
    resultado.textContent = `Parabéns! Você ganhou R$${ganhos}! O cavalo ${nomeCavalos[vencedor]} venceu!`
    criarConfete()
  } else {
    resultado.textContent = `Que pena! Você perdeu. O cavalo ${nomeCavalos[vencedor]} venceu!`
  }
  atualizarCarteira()
}

function criarConfete() {
  const quantidadeConfete = 200
  const cores = ['#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1', '#f7fff7']
  for (let i = 0; i < quantidadeConfete; i++) {
    const confete = document.createElement('div')
    confete.style.position = 'fixed'
    confete.style.left = Math.random() * 100 + 'vw'
    confete.style.top = -20 + 'px'
    confete.style.width = '10px'
    confete.style.height = '10px'
    confete.style.backgroundColor =
      cores[Math.floor(Math.random() * cores.length)]
    confete.style.borderRadius = '50%'
    confete.style.zIndex = '1000'
    document.body.appendChild(confete)
    const animacao = confete.animate(
      [
        {
          transform: 'translateY(0) rotate(0)',
          opacity: 1,
        },
        {
          transform: `translateY(${window.innerHeight}px) rotate(${
            Math.random() * 360
          }deg)`,
          opacity: 0,
        },
      ],
      {
        duration: Math.random() * 3000 + 2000,
        easing: 'cubic-bezier(0,0,0.2,1)',
      }
    )
    animacao.onfinish = () => confete.remove()
  }
}
atualizarCarteira()
