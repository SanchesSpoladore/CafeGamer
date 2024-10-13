const btnMenu = document.getElementById("menu-btn");
const menuPrincipal = document.getElementById("menu-principal");
const btnPerfil = document.getElementById("perfil-btn");
const menuPerfil = document.getElementById("menu-perfil");

function toggleMenu(menu) {
  if (menu === "principal") {
    menuPrincipal.classList.toggle("ativo");
    if (menuPerfil.classList.contains("ativo")) {
      menuPerfil.classList.remove("ativo");
    }
  } else if (menu === "perfil") {
    menuPerfil.classList.toggle("ativo");
    if (menuPrincipal.classList.contains("ativo")) {
      menuPrincipal.classList.remove("ativo");
    }
  }
}

btnMenu.addEventListener("click", () => toggleMenu("principal"));
btnPerfil.addEventListener("click", () => toggleMenu("perfil"));

// ================================================================

(async () => {
  const interval = 1500;
  const carrosselContainer = document.querySelector(".pontuacoes");
  const items = document.querySelectorAll(".pontuacao");
  const itemWidth = items[0].offsetWidth + 50;
  const totalWidth = items.length * itemWidth;
  let idx = 0;

  carrosselContainer.style.width = `${totalWidth}px`;

  while (true) {
    await new Promise(r => setTimeout(r, interval));
    idx++;
    carrosselContainer.style.transform = `translateX(${-idx * itemWidth}px)`;

    if (idx >= items.length-4) {
      idx = 0;
      carrosselContainer.style.transition = 'none';
      await new Promise(r => setTimeout(r, 50));
      carrosselContainer.style.transform = `translateX(0)`;
      carrosselContainer.style.transition = 'transform 1s';
    }
  }
})();




