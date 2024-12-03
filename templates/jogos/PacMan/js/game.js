//Obtém o elemento canvas e o contexto em 2d para desenhar nele
const canvas = document.getElementById("canvas");
const canvasContext = canvas.getContext("2d");

//Obtém os frames do pacman e dos ghosts
const pacmanFrames = document.getElementById("animations");
const ghostFrames = document.getElementById("ghosts");

//função para criar um retânculo no canvas (paredes, comida e etc)
let createRect = (x, y, width, height, color) => {
    canvasContext.fillStyle = color 
    canvasContext.fillRect(x, y, width, height) 
}

//taxa de atualização do jogo
let fps = 30;

//tamanho do bloco no mapa do jogo
let oneBlockSize = 20

//cor do muro
let wallColor = "#342DCA"

//definição de cores e contadores iniciais 
let wallSpaceWidth = oneBlockSize / 1.5
let wallOffset = (oneBlockSize - wallSpaceWidth) / 2
let wallInnerColor = "black"
let foodColor = "#FEB897"
let score = 0
let ghosts = []
let ghostCount = 4
let lives = 3
let foodCount = 0


//Direçõe definidas para controle do movimento
const DIRECTION_RIGHT = 4
const DIRECTION_UP = 3
const DIRECTION_LEFT = 2
const DIRECTION_BOTTOM = 1


//Definição da localização dos fantasmas
let ghostLocations = [
    {x: 0, y: 0},
    {x: 176, y: 0},
    {x: 0, y: 121},
    {x: 176, y: 121},
]


//mapa do jogo (1=parede, 2=comida, 0=espaço vazio)

const initialMap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 0, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
];

// Copia o estado inicial do mapa
let map = JSON.parse(JSON.stringify(initialMap));

//contagem de comida no mapa
for (let i = 0; i < map.length; i++){
    for (let j = 0; j < map[0].length; j++){
        if (map[i][j] == 2) {
            foodCount++
        }
    }
}

//Posições aleatórias para os fantasmas se moverem
let randomTargetsForGhosts = [
    {x: 1 * oneBlockSize, y: 1 * oneBlockSize}, 
    {x: 1 * oneBlockSize, y: (map.length - 2) * oneBlockSize}, 
    {x: (map[0].length - 2) * oneBlockSize, y: oneBlockSize}, 
    {x: (map.length - 2) * oneBlockSize, y:(map.length - 2) * oneBlockSize}, 
]

//Definição do pause
let ispaused = false

let isGameOver = false

//Função principal do loop do jogo
let gameLoop = () => {
    if(!ispaused ){ //executa o jogo somente se não estiver pausado e nem na tela de gameover
        draw()
        update()
    }
    
    
}

//Função de atualização da lógica do jogo
let update = () =>{
    pacman.moveProcess() //movimenta o pacman
    pacman.eat() //pacman come a comida
    for(let i = 0; i<ghosts.length; i++){
        ghosts[i].moveProcess() //move os fantasmas
    }
    if(pacman.checkGhostCollision()){
        restartGame() //reinicia o jogo caso o pacman colide com o fantasma
    }
    if(score >= foodCount){
        drawWin() //desenha a mensagem de vitória
        clearInterval(gameInterval)//Para o loop do jogo
    }
}

//Função para reiniciar o jogo caso perder a vida
let restartGame = () => {
    createNewPacman() //cria um novo pacman
    createGhosts() //cria um novo fanstasma
    lives-- //reduz a quantidade de vida
    if(lives == 0){
        gameOver() //quando a quantidade de vida chegar a zero, o jogo acaba
        
    }
    
}

//Função para reiniciar o jogo depois do gameover
let restartGameAfterGameOver = () => {
    createNewPacman()
    createGhosts()
    map = JSON.parse(JSON.stringify(initialMap));
    score = 0 
    lives = 3
    isGameOver = false
    foodCount = 0
    for(let i = 0; i < map.length; i++){
        for(let j = 0; j < map[0].length; j++){
            if(map[i][j] == 2){
                foodCount++
            }
        }
    }
    clearInterval(gameInterval)
    gameInterval = setInterval(gameLoop, 1080 / fps)
}

//Função para reiniciar o jogo depois de ganhar
let restartGameAfterWin = () => {
    createNewPacman()
    createGhosts()
    map = JSON.parse(JSON.stringify(initialMap));
    score = 0 
    lives = 3
    isGameOver = false
    foodCount = 0
    for(let i = 0; i < map.length; i++){
        for(let j = 0; j < map[0].length; j++){
            if(map[i][j] == 2){
                foodCount++
            }
        }
    }
    clearInterval(gameInterval)
    gameInterval = setInterval(gameLoop, 1080 / fps)

}
//Função para gameover
let gameOver = () => {
    
    drawGameOver() //desenha a mensagem de gameover
    clearInterval(gameInterval) //para o loop do jogo
    window.parent.postMessage({ gameOver: true, score: score }, "*");
    
}

//Função que desenha a mensagem de gameover
let drawGameOver = () => {
    canvasContext.font = "20px 'press start 2p' "
    canvasContext.fillStyle = 'white'
    canvasContext.fillText("Game Over!", 100, 200 )
    canvasContext.font = "10px 'press start 2p' "
    canvasContext.fillText("Clique X para reiniciar",80, 220)
}

//Função que desenha a mensagem de vitória
let drawWin = () => {
    canvasContext.font = "20px 'press start 2p' "
    canvasContext.fillStyle = 'white'
    canvasContext.fillText("Congratulations!", 50, 200 )
    canvasContext.font = "10px 'press start 2p' "
    canvasContext.fillText("Clique em c para reiniciar", 75, 220 )
}
    
//Função que desenha as vidas
let drawLives = () => {
    canvasContext.font = "20px 'press start 2p' "
    canvasContext.fillStyle = 'white'
    canvasContext.fillText("Lives: ", 200, oneBlockSize * (map.length + 1) + 5)
    for(let i = 0; i < lives; i++){
        canvasContext.drawImage(
            pacmanFrames, 
            2 * oneBlockSize, 
            0, 
            oneBlockSize, 
            oneBlockSize, 
            320 + i * oneBlockSize,
            oneBlockSize * map.length + 5, 
            oneBlockSize, 
            oneBlockSize
        )
    }
}

//Função que desenha as comidas
let drawFoods = () => {
    for(let i = 0; i < map.length; i++) {
        for(let j = 0; j < map[0].length; j++){
            if(map[i][j] == 2){
                createRect(
                    j * oneBlockSize + oneBlockSize / 3,
                    i * oneBlockSize + oneBlockSize / 3,
                    oneBlockSize / 3,
                    oneBlockSize / 3,
                    foodColor
                )
            }
        }
    }
}

//Função que desenha a pontuação
let drawScore = () => {
    canvasContext.font = "20px 'press start 2p' "
    canvasContext.fillStyle = "white"
    canvasContext.fillText("Score: " + score, 0, oneBlockSize * (map.length + 1 ) + 5)
}

//Função que desenha os fantasmas
let drawGhosts = () =>{
    for(let i = 0; i < ghosts.length; i++) {
        ghosts[i].draw()
    }
}

//Função para reunir todos os draws
let draw = () => {
    createRect(0,0, canvas.width, canvas.height, "black")
    drawWalls()
    drawFoods()
    pacman.draw()
    drawScore()
    drawGhosts()
    drawLives()
}

//Loop do jogo
let gameInterval = setInterval(gameLoop, 1080/fps)

//Função que desenha as paredes
let drawWalls =() => {
    for(let i = 0; i < map.length; i++){
        for(let j = 0; j < map[0].length; j++){
            if(map[i][j] == 1) { // então é um muro
                createRect(
                    j * oneBlockSize, 
                    i * oneBlockSize, 
                    oneBlockSize, 
                    oneBlockSize, 
                    wallColor);
                    if (j>0 && map[i][j-1] == 1){
                        createRect(
                            j*oneBlockSize, 
                            i*oneBlockSize + wallOffset,
                            wallSpaceWidth + wallOffset, 
                            wallSpaceWidth, 
                            wallInnerColor
                        )
                    }
                    if(j < map[0].length -1 && map[i][j+1]==1){
                        createRect(
                            j*oneBlockSize + wallOffset, 
                            i*oneBlockSize + wallOffset,
                            wallSpaceWidth + wallOffset, 
                            wallSpaceWidth, 
                            wallInnerColor
                        ) 
                    }
                    if(i >0 && map[i-1][j] == 1){
                        createRect(
                            j*oneBlockSize + wallOffset, 
                            i*oneBlockSize, 
                            wallSpaceWidth, 
                            wallSpaceWidth + wallOffset, 
                            wallInnerColor
                        )
                    }
                    if(i < map.length -1 && map[i+1][j]==1){
                        createRect(
                            j*oneBlockSize + wallOffset, 
                            i*oneBlockSize + wallOffset,
                            wallSpaceWidth , 
                            wallSpaceWidth + wallOffset, 
                            wallInnerColor
                        ) 
                    }
            }
        }
    }
}

//Função que desenha o PacMan
let createNewPacman = () =>{
    pacman = new Pacman(
        oneBlockSize,
        oneBlockSize,
        oneBlockSize,
        oneBlockSize,
        oneBlockSize / 5
    
    )
}

//Função que desenha os fantasmas
let createGhosts =() =>{
    ghosts = []
    for(let i = 0; i < ghostCount; i++){
        let newGhost = new Ghost(
            9 * oneBlockSize + (i % 2 == 0 ? 0 : 1) * oneBlockSize, 
            10 * oneBlockSize + (i % 2 == 0 ? 0 : 1) * oneBlockSize,
            oneBlockSize, 
            oneBlockSize, 
            pacman.speed /  2,
            ghostLocations[i % 4].x, 
            ghostLocations[i % 4].y, 
            124, 
            116,
            6 + i

        )
        ghosts.push(newGhost)
    }
}

createNewPacman()
createGhosts()
gameLoop()

//evento para cada botão
window.addEventListener("keydown", (event) => {
    let k = event.keyCode 

    if(event.key === 'c' || event.key === 'C') {
        restartGameAfterWin()
    }


    if(event.key === 'x' || event.key === 'X'){
        restartGameAfterGameOver()
    }

    if(event.key === 'p' || event.key === 'P'){
        ispaused = !ispaused
    }

    setTimeout(() => {
        if(k==37 || k == 65){ 
            //left
            pacman.nextDirection = DIRECTION_LEFT

        } else if (k == 38 || k == 87) { 
            //up
            pacman.nextDirection = DIRECTION_UP

        } else if (k == 39 || k == 68) { 
            //right
            pacman.nextDirection = DIRECTION_RIGHT

        } else if (k == 40 || k == 83){ 
            //bottom
            pacman.nextDirection = DIRECTION_BOTTOM


        }
    },1)
})
