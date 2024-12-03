document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('mensagemModal')
  const span = document.getElementsByClassName('fechar')[0]
  const telefoneInput = document.getElementById('telefone')
  const form = document.querySelector('form')

  function mostrarModal(title, message) {
    document.getElementById('modalTitulo').innerHTML = title
    document.getElementById('modalMensagem').innerHTML = message
    modal.style.display = 'block'
  }

  function fecharModal() {
    modal.style.display = 'none'
  }

  function formatarTelefone(value) {
    const valorLimpo = value.replace(/\D/g, '')
    if (valorLimpo.length <= 11) {
      if (valorLimpo.length <= 2) {
        return valorLimpo
      } else if (valorLimpo.length <= 7) {
        return `(${valorLimpo.slice(0, 2)}) ${valorLimpo.slice(2)}`
      } else {
        return `(${valorLimpo.slice(0, 2)}) ${valorLimpo.slice(
          2,
          7
        )}-${valorLimpo.slice(7, 11)}`
      }
    }
    return value
  }

  function validarTelefone(value) {
    const valorLimpo = value.replace(/\D/g, '')
    return valorLimpo.length === 11 || valorLimpo.length === 10
  }

  const mensagem = pegarCookie('mensagem')
  const titulo = pegarCookie('titulo')
  if (mensagem && titulo) {
    mostrarModal(titulo, mensagem)
    document.cookie =
      'mensagem=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
    document.cookie = 'titulo=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
  }

  span.onclick = fecharModal

  window.onclick = function (event) {
    if (event.target == modal) {
      fecharModal()
    }
  }

  telefoneInput.addEventListener('input', function (e) {
    const posicaoPonteiro = e.target.selectionStart
    const valorAnterior = e.target.value
    const valorFormatado = formatarTelefone(e.target.value)
    e.target.value = valorFormatado

    const addedChars = valorFormatado.length - valorAnterior.length
    e.target.setSelectionRange(
      posicaoPonteiro + addedChars,
      posicaoPonteiro + addedChars
    )
  })

  form.addEventListener('submit', function (e) {
    if (telefoneInput.value && !validarTelefone(telefoneInput.value)) {
      e.preventDefault()
      mostrarModal(
        'Erro de Validação',
        'Por favor, insira um número de telefone válido (10 ou 11 dígitos).'
      )
    }
  })

  function pegarCookie(name) {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
  }
})
