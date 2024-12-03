const hoverAudio = new Audio('/static/audio/hover.mp3');
const clickAudio = new Audio('/static/audio/clique.mp3');
const cardJogos = document.querySelectorAll('.containerJogo');
const caminhoCapa = '/static/img/inicio/';
const toggleSoundCheckbox = document.getElementById('toggleSound')

// SONS DO SITE
let soundEnabled = true;

document.getElementById('toggleSound').addEventListener('change', function(event) {
  soundEnabled = event.target.checked;
});

cardJogos.forEach(cardJogo => {
  cardJogo.addEventListener('mouseenter', () => {
      if (soundEnabled) {
          hoverAudio.currentTime = 0;
          hoverAudio.play();
      }
  });
});

document.addEventListener('click', () => {
  if (soundEnabled) {
      clickAudio.currentTime = 0;
      clickAudio.play();
  }
});


// CARROSSEL
class Pontuacao {
  constructor(nome, nick, jogo, capa, pontuacao, data) {
      this.nome = nome;
      this.nick = nick;
      this.jogo = jogo;
      this.capa = capa;
      this.pontuacao = pontuacao;
      this.data = data;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const carrossel = document.getElementById('carrossel');
  let scrollAmount = 0;
  configurarCarrossel()

  function scrollCarrossel() {
      scrollAmount += 0.4;
      if (scrollAmount >= carrossel.scrollWidth) {
          scrollAmount = 0;
      }
      carrossel.scrollTo({
          left: scrollAmount,
          behavior: "auto"
      });
  }

  setInterval(scrollCarrossel, 1);
});


function obterItensVisiveis() {
const larguraContainer = document.querySelector('.carrossel-container').offsetWidth;
const larguraItem = document.querySelector('.pontuacao').offsetWidth;
return Math.floor(larguraContainer / larguraItem);
}

function configurarCarrossel() {
const carrossel = document.getElementById('carrossel');
let indiceAtual = 0;
let itensVisiveis = obterItensVisiveis();

function moverCarrossel() {
    const larguraItem = carrossel.children[0].offsetWidth;
    const maxIndice = carrossel.children.length - itensVisiveis;

    if (indiceAtual < maxIndice) {
        indiceAtual++;
    } else {
        indiceAtual = 0;
        carrossel.style.transition = 'none';
        carrossel.style.transform = 'translateX(0)';
        setTimeout(() => {
            carrossel.style.transition = 'transform 1s ease-in-out';
        }, 50);
    }

    carrossel.style.transform = `translateX(-${indiceAtual * larguraItem}px)`;
}

setInterval(moverCarrossel, 3000);

window.addEventListener('resize', () => {
    itensVisiveis = obterItensVisiveis();
    indiceAtual = 0;
    carrossel.style.transition = 'none';
    carrossel.style.transform = 'translateX(0)';
    setTimeout(() => {
        carrossel.style.transition = 'transform 1s ease-in-out';
    }, 50);
});
}

document.addEventListener('DOMContentLoaded', () => {
criarItensCarrossel();
configurarCarrossel();
});

const menuBtn = document.getElementById('menu-btn')
const perfilBtn = document.getElementById('perfil-btn')
const botaoMenu = document.getElementById('menu-btn')
const menuPrincipal = document.getElementById('menu-principal')
const botaoPerfil = document.getElementById('perfil-btn')
const menuPerfil = document.getElementById('menu-perfil')


toggleSoundCheckbox.addEventListener('change', (event) => {
  soundEnabled = event.target.checked
})

cardJogos.forEach((cardJogo) => {
  cardJogo.addEventListener('mouseenter', () => {
    if (soundEnabled) {
      hoverAudio.currentTime = 0
      hoverAudio.play()
    }
  })
})

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


function toggleMenu(menu) {
  if (menu === 'principal') {
    menuPrincipal.classList.toggle('active')
    menuPerfil.classList.remove('active')
  } else if (menu === 'perfil') {
    menuPerfil.classList.toggle('active')
    menuPrincipal.classList.remove('active')
  }
}

menuBtn.addEventListener('click', () => toggleMenu('principal'))
perfilBtn.addEventListener('click', () => toggleMenu('perfil'))

document.addEventListener('click', (event) => {
  if (
    !event.target.closest('#menu-btn') &&
    !event.target.closest('#menu-principal')
  ) {
    menuPrincipal.classList.remove('active')
  }
  if (
    !event.target.closest('#perfil-btn') &&
    !event.target.closest('#menu-perfil')
  ) {
    menuPerfil.classList.remove('active')
  }
})


document.getElementById('pesquisaInput').addEventListener('input', async (event) => {
  const query = event.target.value.trim();
  const sugestoesContainer = document.getElementById('sugestoes');
  
  if (query.length > 2) { 
    try {
      const response = await fetch(`/pesquisa?s=${encodeURIComponent(query)}`);
      const resultados = await response.json();
      
      sugestoesContainer.innerHTML = '';
      resultados.forEach((resultado) => {
        const li = document.createElement('li');
        li.textContent = resultado;
        li.addEventListener('click', () => {
          document.getElementById('pesquisaInput').value = resultado;
          sugestoesContainer.style.display = 'none';
        });
        sugestoesContainer.appendChild(li);
      });
      sugestoesContainer.style.display = 'block';
    } catch (error) {
      console.error('Erro ao buscar sugestões:', error);
    }
  } else {
    sugestoesContainer.style.display = 'none';
  }
});








// Função para buscar um cookie pelo nome
function obterCookie(nome) {
  const valor = `; ${document.cookie}`;

  const partes = valor.split(`; ${nome}=`);

  if (partes.length === 2) return partes.pop().split(';').shift();
  return null;
}

async function curtirJogo(nomeJogo) {

  const tokenAutenticacao = obterCookie("email");
  
  if (!tokenAutenticacao) {
      alert("Você precisa estar autenticado para curtir um jogo.");
      return;
  }

  const botaoCurtir = document.getElementById(`curtir_jogos_${nomeJogo}`);

  let curtidasAtuais = parseInt(botaoCurtir.value);
  
  curtidasAtuais += 1;
  botaoCurtir.value = `${curtidasAtuais} 👍`;

  try {
      const response = await fetch(`/jogos/curtir_jogo/${nomeJogo}`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${tokenAutenticacao}` // Envia o token caso ele seja necessário
          },
          body: JSON.stringify({ curtida: curtidasAtuais })
      });
      if (!response.ok) {
          throw new Error("Erro ao curtir o jogo.");
      }
  } catch (error) {
      console.error(error);
      alert("Não foi possível curtir o jogo no momento.");
  }
}


botaoMenu.addEventListener('click', () => alternarMenu('principal'))
botaoPerfil.addEventListener('click', () => alternarMenu('perfil'))

