const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const dispositivoMobile = window.innerWidth <= 768;
const tamanhoDivisao = dispositivoMobile ? 20 : 30;
const tamanhoCanvas = dispositivoMobile ? 300 : 600;

canvas.width = tamanhoCanvas;
canvas.height = tamanhoCanvas;

const pontuacao = document.querySelector(".container");
const pontuacaoValor = document.querySelector(".pontuacao--value");
const pontuacaoFinal = document.querySelector(".pontuacao-final > span");
const levelValor = document.querySelector(".level--value");
const maiorPontuacaoValor = document.querySelector(".maiorPontuacao--value");
const nomeJogadorValor = document.querySelector(".nomeJogador--value");
const menu = document.querySelector(".menu");
const botaoPlay = document.querySelector(".btn-play");

const audioComida = new Audio("/static/audio/cobrinha/audio.mp3");
const audioGameOver = new Audio("/static/audio/cobrinha/gameover.mp3");

const posicaoInicial = { x: 9 * tamanhoDivisao, y: 8 * tamanhoDivisao };

let velocidadeInicial = 400;
let velocidade = velocidadeInicial;
let somarLevel = 0;
let level = 0;

let cobra = [posicaoInicial];
let direcao, loopJogo;
let estadoPause = false;
let estadoGameOver = false;
let podeMover = true;

const limparRecorde = () => {
    localStorage.removeItem("maiorPontuacao");
    localStorage.removeItem("nomeJogador");
    maiorPontuacaoValor.innerText = "0";
    nomeJogadorValor.innerText = "-";
};

limparRecorde();

const incrementarPontuacao = () => {
    pontuacaoValor.innerText = +pontuacaoValor.innerText + 10;
};

const incrementarVelocidade = () => {
    velocidade -= 20;
    levelValor.innerText = level;
};

const numeroAleatorio = (min, max) => Math.round(Math.random() * (max - min) + min);

const posicaoAleatoria = () => {
    const num = numeroAleatorio(0, tamanhoCanvas - tamanhoDivisao);
    return Math.round(num / tamanhoDivisao) * tamanhoDivisao;
};

const corAleatoria = () => {
    const vermelho = numeroAleatorio(0, 255);
    const verde = numeroAleatorio(0, 255);
    const azul = numeroAleatorio(0, 255);
    return `rgb(${vermelho}, ${verde}, ${azul})`;
};

const comida = {
    x: posicaoAleatoria(),
    y: posicaoAleatoria(),
    cor: corAleatoria()
};

const desenharComida = () => {
    const { x, y, cor } = comida;
    ctx.shadowColor = cor;
    ctx.shadowBlur = 6;
    ctx.fillStyle = cor;
    ctx.fillRect(x, y, tamanhoDivisao, tamanhoDivisao);
    ctx.shadowBlur = 0;
};

const desenharCobra = () => {
    ctx.fillStyle = "#ddd";
    cobra.forEach((position, index) => {
        ctx.fillStyle = index === cobra.length - 1 ? "white" : "#ddd";
        ctx.fillRect(position.x, position.y, tamanhoDivisao, tamanhoDivisao);
    });
};

const moverCobra = () => {
    if (!direcao || estadoPause || estadoGameOver) return;
    const cabeca = cobra[cobra.length - 1];
    if (direcao === "direita") cobra.push({ x: cabeca.x + tamanhoDivisao, y: cabeca.y });
    if (direcao === "esquerda") cobra.push({ x: cabeca.x - tamanhoDivisao, y: cabeca.y });
    if (direcao === "baixo") cobra.push({ x: cabeca.x, y: cabeca.y + tamanhoDivisao });
    if (direcao === "cima") cobra.push({ x: cabeca.x, y: cabeca.y - tamanhoDivisao });
    cobra.shift();
    podeMover = true;
};

const desenharGrid = () => {
    ctx.lineWidth = 1;
    ctx.strokeStyle = "#454545";
    for (let i = tamanhoDivisao; i < tamanhoCanvas; i += tamanhoDivisao) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, tamanhoCanvas);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(tamanhoCanvas, i);
        ctx.stroke();
    }
};

const checkarComida = () => {
    const cabeca = cobra[cobra.length - 1];
    if (cabeca.x === comida.x && cabeca.y === comida.y) {
        incrementarPontuacao();
        cobra.push(cabeca);
        audioComida.play();
        somarLevel++;
        if (somarLevel === 4) {
            somarLevel = 0;
            level++;
            incrementarVelocidade();
        }
        comida.x = posicaoAleatoria();
        comida.y = posicaoAleatoria();
        comida.cor = corAleatoria();
    }
};

const checkarColisao = () => {
    const cabeca = cobra[cobra.length - 1];
    const corpo = cobra.slice(0, -1);
    const bateuNaParede = cabeca.x < 0 || cabeca.x > tamanhoCanvas - 1 || cabeca.y < 0 || cabeca.y > tamanhoCanvas - 1;
    const bateuNoProprioCorpo = corpo.find((position) => position.x === cabeca.x && position.y === cabeca.y);
    if (bateuNaParede || bateuNoProprioCorpo) {
        audioGameOver.play();
        estadoGameOver = true;
        clearInterval(loopJogo);
        const recorde = +maiorPontuacaoValor.innerText;
        const recordeAtual = +pontuacaoValor.innerText;
        if (recordeAtual > recorde) {
            const nomeJogador = prompt("Novo recorde! Qual o seu nome?") || "Jogador Anônimo";
            maiorPontuacaoValor.innerText = recordeAtual;
            nomeJogadorValor.innerText = nomeJogador;
            localStorage.setItem("maiorPontuacao", recordeAtual);
            localStorage.setItem("nomeJogador", nomeJogador);
        }
        menu.style.display = "flex";
        pontuacao.style.display = "none";
        pontuacaoFinal.innerText = recordeAtual;
    }
};

const setarDirecao = (event) => {
    if (estadoPause || estadoGameOver) return;
    if (!podeMover) return;
    if (event.key.includes("Arrow")) podeMover = false;
    if (event.key === "ArrowRight" && direcao !== "esquerda") direcao = "direita";
    if (event.key === "ArrowLeft" && direcao !== "direita") direcao = "esquerda";
    if (event.key === "ArrowDown" && direcao !== "cima") direcao = "baixo";
    if (event.key === "ArrowUp" && direcao !== "baixo") direcao = "cima";
};

const desenhar = () => {
    ctx.clearRect(0, 0, tamanhoCanvas, tamanhoCanvas);
    desenharGrid();
    desenharComida();
    moverCobra();
    desenharCobra();
    checkarComida();
    checkarColisao();
};

const iniciarJogo = () => {
    menu.style.display = "none";
    pontuacao.style.display = "flex";
    levelValor.innerText = "0";
    cobra = [posicaoInicial];
    direcao = undefined;
    pontuacaoValor.innerText = "0";
    velocidade = velocidadeInicial;
    level = 0;
    somarLevel = 0;
    estadoGameOver = false;
    loopJogo = setInterval(desenhar, velocidade);
};

botaoPlay.addEventListener("click", iniciarJogo);
window.addEventListener("keydown", setarDirecao);
