export default class Player {
  WALK_ANIMATION_TIMER = 200;
  walkAnimationTimer = this.WALK_ANIMATION_TIMER;
  dinoRunImages = [];

  jumpPressed = false;
  jumpInProgress = false;
  falling = false;
  JUMP_SPEED = 0.6;
  GRAVITY = 0.4;
  score = 0; // Variável para contar os pontos

  constructor(ctx, width, height, minJumpHeight, maxJumpHeight, scaleRatio) {
    this.ctx = ctx;
    this.canvas = ctx.canvas;
    this.width = width;
    this.height = height;
    this.minJumpHeight = minJumpHeight;
    this.maxJumpHeight = maxJumpHeight;
    this.scaleRatio = scaleRatio;

    this.x = 10 * scaleRatio;
    this.y = this.canvas.height - this.height - 1.5 * scaleRatio;
    this.yStandingPosition = this.y;

    this.standingStillImage = new Image();
    this.standingStillImage.src = "./img/standing_still.png";
    this.image = this.standingStillImage;

    const dinoRunImage1 = new Image();
    dinoRunImage1.src = "./img/dino_run1.png";

    const dinoRunImage2 = new Image();
    dinoRunImage2.src = "./img/dino_run2.png";

    this.dinoRunImages.push(dinoRunImage1);
    this.dinoRunImages.push(dinoRunImage2);

    // Carregando os sons com os nomes corretos
    this.jumpSound = new Audio("./audio/jump_sound.wav"); // Som do pulo
    this.scoreSound = new Audio("./audio/score_sound.wav"); // Som da pontuação (100 pontos)
    this.deathSound = new Audio("./audio/death_sound.wav"); // Som da morte

    // Verificação de carregamento de sons (opcional)
    this.jumpSound.oncanplaythrough = () => console.log("Jump sound loaded");
    this.scoreSound.oncanplaythrough = () => console.log("Score sound loaded");
    this.deathSound.oncanplaythrough = () => console.log("Death sound loaded");

    // Adicionando e removendo eventos
    window.removeEventListener("keydown", this.keydown);
    window.removeEventListener("keyup", this.keyup);

    window.addEventListener("keydown", this.keydown);
    window.addEventListener("keyup", this.keyup);

    window.removeEventListener("touchstart", this.touchstart);
    window.removeEventListener("touchend", this.touchend);

    window.addEventListener("touchstart", this.touchstart);
    window.addEventListener("touchend", this.touchend);
  }

  touchstart = () => {
    this.jumpPressed = true;
  };

  touchend = () => {
    this.jumpPressed = false;
  };

  keydown = (event) => {
    if (event.code === "Space") {
      this.jumpPressed = true;
    }
  };

  keyup = (event) => {
    if (event.code === "Space") {
      this.jumpPressed = false;
    }
  };

  update(gameSpeed, frameTimeDelta, currentScore) {
    this.run(gameSpeed, frameTimeDelta);

    if (this.jumpInProgress) {
      this.image = this.standingStillImage;
    }

    this.jump(frameTimeDelta);
    this.checkScore(currentScore); // Checa se a pontuação atingiu 100
  }

  jump(frameTimeDelta) {
    if (this.jumpPressed && !this.jumpInProgress && !this.falling) {
      console.log("Starting jump");
      // Reproduz o som do pulo
      this.jumpSound.play();
      this.jumpInProgress = true;
    }

    if (this.jumpInProgress && !this.falling) {
      if (
        this.y > this.canvas.height - this.minJumpHeight ||
        (this.y > this.canvas.height - this.maxJumpHeight && this.jumpPressed)
      ) {
        this.y -= this.JUMP_SPEED * frameTimeDelta * this.scaleRatio;
      } else {
        this.falling = true;
      }
    } else {
      if (this.y < this.yStandingPosition) {
        this.y += this.GRAVITY * frameTimeDelta * this.scaleRatio;
        if (this.y + this.height > this.canvas.height) {
          this.y = this.yStandingPosition;
        }
      } else {
        this.falling = false;
        this.jumpInProgress = false;
      }
    }
  }

  run(gameSpeed, frameTimeDelta) {
    if (this.walkAnimationTimer <= 0) {
      if (this.image === this.dinoRunImages[0]) {
        this.image = this.dinoRunImages[1];
      } else {
        this.image = this.dinoRunImages[0];
      }
      this.walkAnimationTimer = this.WALK_ANIMATION_TIMER;
    }
    this.walkAnimationTimer -= frameTimeDelta * gameSpeed;
  }

  draw() {
    this.ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
  }

  checkScore(currentScore) {
    // Reproduz o som ao atingir múltiplos de 100 pontos
    if (currentScore > 0 && currentScore % 100 === 0 && currentScore !== this.score) {
      console.log("Score sound should play");
      this.scoreSound.play();
      this.score = currentScore; // Atualiza a pontuação
    }
  }

  die() {
    // Reproduz o som da morte
    console.log("Playing death sound");
    this.deathSound.play();
  }
}
