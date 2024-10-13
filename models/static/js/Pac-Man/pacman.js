class Pacman {
    //início da criação dos parâmetros do pacman
    constructor(x, y, width, height, speed){
        this.x = x
        this.y = y
        this.width = width //largura
        this.heigth = height //altura
        this.speed = speed
        this.direction = DIRECTION_RIGHT //direção inicial 
        this.nextDirection = this.direction
        this.currentFrame = 1 //quadro de animação
        this.frameCount = 7

        //mudança do tempo de animação, 100ms
        setInterval(() => {
            this.changeAnimation()
        }, 100)
    }

    moveProcess(){
        //Se for possível, tenta mudar a direção
        this.changeDirectionIfPossible();
        this.moveForwards()

        //Se houver colisão, move para trás -> em outras palavras, na direção oposta
        if(this.checkCollision()){
            this.moveBackwards()
        }
    }

    eat(){
        //verificando se o pacman está colidindo com a comida (valor 2) e come (valor 3)
        for(let i = 0; i<map.length; i++){
            for(let j=0; j<map[0].length; j++){
                if(
                    map[i][j] == 2 && //verifica a existência de comida no mapa
                    this.getMapX() == j && //verifica se o pacman está na mesma coluna
                    this.getMapY() == i //verifica se o pacman está na mesma linha
                ){
                    map[i][j] = 3 //come a comida
                    score++
                }
            }
        }
    }

    moveBackwards(){ //movimenta o pacman na direção oposta da atual 
        switch(this.direction) {
            case DIRECTION_RIGHT:
                this.x -= this.speed
                break
            case DIRECTION_UP:
                this.y += this.speed
                break
            case DIRECTION_LEFT:
                this.x += this.speed
                break
            case DIRECTION_BOTTOM:
                this.y -= this.speed
                break
        }
    }

    moveForwards(){ //movimento o pacman na direção normal
        switch(this.direction) {
            case DIRECTION_RIGHT:
                this.x += this.speed
                break
            case DIRECTION_UP:
                this.y -= this.speed
                break
            case DIRECTION_LEFT:
                this.x -= this.speed
                break
            case DIRECTION_BOTTOM:
                this.y += this.speed
                break
        }
    }

    checkCollision(){ //verifica se o pacman colidiu com alguma parede (valor 1 no mapa)
        let isCollided = false 
        if(map[this.getMapY()][this.getMapX()] == 1 || //canto superior esquerdo
        map[this.getMapYRightSide()][this.getMapX()] == 1 || //canto inferior esquerdo
        map[this.getMapY()][this.getMapXRightSide()] == 1 || //canto superior direito
        map[this.getMapYRightSide()][this.getMapXRightSide()] == 1 //canto inferior direito
    ){
        return true //houve colisão
        }
    return false //sem colisão
    }

    checkGhostCollision(){ //verifica se o pacman colidiu com algum fantasma
        for(let i = 0; i < ghosts.length; i++){
            let ghost = ghosts[i]
            if( //verifica colisão nos eixos de x e y
                ghost.getMapX() == this.getMapX() && 
                ghost.getMapY() == this.getMapY()
            ) {
                    return true //houve colisão
                }
        }
        return false //não houve colisão
    }

    changeDirectionIfPossible(){
        //se a direção atual for a próxima, nada irá ocorrer
        if(this.direction == this.nextDirection) return 
        
        //tenta mudar a direção atual
        let tempDirection = this.direction //guarda a atual
        this.direction = this.nextDirection //atualiza a nova direção
        this.moveForwards() //move o pacman na nova direção

        //mas se houver colisão, desfaz tudo
        if(this.checkCollision()){
            this.moveBackwards()
            this.direction = tempDirection //restaura a direção anterior
        } else {
            this.moveBackwards()
        }
    }

    changeAnimation(){ //atualiza o quadro de animação, sempre reinicia quando chega no último frame
        this.currentFrame = 
            this.currentFrame == this.frameCount ? 1 : this.currentFrame + 1
    }

    draw(){ //desenha o pacman
     canvasContext.save() //Salva o contexto atual do canvas
     canvasContext.translate(
        this.x + oneBlockSize / 2, 
        this.y + oneBlockSize / 2,

    );

    //rotaciona o pacman com base na direção
    canvasContext.rotate((this.direction * 90 * Math.PI) / 180)

    //restaura a origem da posição
    canvasContext.translate(
        -this.x - oneBlockSize / 2, 
        -this.y - oneBlockSize / 2,
    );

    //desenha o pacman com base no frame atual
    canvasContext.drawImage(
        pacmanFrames, 
        (this.currentFrame - 1) * oneBlockSize,
        0, 
        oneBlockSize, 
        oneBlockSize, 
        this.x, 
        this.y, 
        this.width, 
        this.heigth
    )

    canvasContext.restore() //restaura o estado original do canvas
    }


    //métodos auxiliares para obter as coordenadas do mapa
    getMapX(){
        return parseInt(this.x / oneBlockSize)
    }
    getMapY(){
        return parseInt(this.y / oneBlockSize)
    }
    getMapXRightSide(){
        return parseInt((this.x + 0.9999 * oneBlockSize) / oneBlockSize)
    }
    getMapYRightSide(){
        return parseInt((this.y + 0.9999 * oneBlockSize) / oneBlockSize)
    }
}