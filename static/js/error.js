document.addEventListener('DOMContentLoaded', () => {
    const jogador = document.querySelector('.jogador')
    const formulario = document.getElementById('notificacao-formulario')
    const areaJogo = document.querySelector('.area-jogo')
  
    function movejogador(direcao) {
      const jogadorCerta = jogador.getBoundingClientRect()
      const areaJogoCerta = areaJogo.getBoundingClientRect()
  
      switch (direcao) {
        case 'left':
          if (jogadorCerta.left > areaJogoCerta.left) {
            jogador.style.left = `${jogadorCerta.left - areaJogoCerta.left - 10}px`
          }
          break
        case 'right':
          if (jogadorCerta.right < areaJogoCerta.right) {
            jogador.style.left = `${jogadorCerta.left - areaJogoCerta.left + 10}px`
          }
          break
        case 'up':
          if (jogadorCerta.top > areaJogoCerta.top) {
            jogador.style.bottom = `${
              areaJogoCerta.bottom - jogadorCerta.bottom + 10
            }px`
          }
          break
        case 'down':
          if (jogadorCerta.bottom < areaJogoCerta.bottom) {
            jogador.style.bottom = `${
              areaJogoCerta.bottom - jogadorCerta.bottom - 10
            }px`
          }
          break
      }
    }
  
    document.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'ArrowLeft':
          movejogador('left')
          break
        case 'ArrowRight':
          movejogador('right')
          break
        case 'ArrowUp':
          movejogador('up')
          break
        case 'ArrowDown':
          movejogador('down')
          break
      }
    })
  
    function criarMoeda() {
      const moeda = document.createElement('div')
      moeda.classList.add('moeda')
      moeda.style.top = `${Math.random() * (areaJogo.clientHeight - 20)}px`
      areaJogo.appendChild(moeda)
  
      const animationDuration = 3000
      let horaInicio
  
      function animacao(tempoAtual) {
        if (!horaInicio) horaInicio = tempoAtual
        const tempoPassado = tempoAtual - horaInicio
  
        if (tempoPassado < animationDuration) {
          const progresso = tempoPassado / animationDuration
          moeda.style.right = `${progresso * 100}%`
  
          const jogadorCerta = jogador.getBoundingClientRect()
          const moedaRect = moeda.getBoundingClientRect()
  
          if (
            jogadorCerta.left < moedaRect.right &&
            jogadorCerta.right > moedaRect.left &&
            jogadorCerta.top < moedaRect.bottom &&
            jogadorCerta.bottom > moedaRect.top
          ) {
            score++
            moeda.remove()
          } else {
            solicitarQuadroAnimacao(animacao)
          }
        } else {
          moeda.remove()
          criarMoeda()
        }
      }
  
      solicitarQuadroAnimacao(animacao)
    }
  
    criarMoeda()
  
    formulario.addEventListener('submit', (e) => {
      e.preventDefault()
      formulario.reset()
    })
  })
  