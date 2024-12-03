export default class Score {
  score = 0;
  HIGH_SCORE_KEY = "highScore";
  
  constructor(ctx, scaleRatio) {
    this.ctx = ctx;
    this.canvas = ctx.canvas;
    this.scaleRatio = scaleRatio;

    // Carregando o som da pontuação (score)
    this.scoreSound = new Audio("./audio/score_sound.wav"); // Caminho do som de pontuação
  }

  update(frameTimeDelta) {
    this.score += frameTimeDelta * 0.01;

    // Checar se a pontuação é múltiplo de 100
    if (Math.floor(this.score) > 0 && Math.floor(this.score) % 100 === 0) {
      this.playScoreSound();
    }
  }

  reset() {
    this.score = 0;
  }

  setHighScore() {
    const highScore = Number(localStorage.getItem(this.HIGH_SCORE_KEY));
    if (this.score > highScore) {
      localStorage.setItem(this.HIGH_SCORE_KEY, Math.floor(this.score));
    }
  }

  draw() {
    const highScore = Number(localStorage.getItem(this.HIGH_SCORE_KEY));
    const y = 20 * this.scaleRatio;

    const fontSize = 20 * this.scaleRatio;
    this.ctx.font = `${fontSize}px serif`;
    this.ctx.fillStyle = "#525250";
    const scoreX = this.canvas.width - 75 * this.scaleRatio;
    const highScoreX = scoreX - 125 * this.scaleRatio;

    const scorePadded = Math.floor(this.score).toString().padStart(6, 0);
    const highScorePadded = highScore.toString().padStart(6, 0);

    this.ctx.fillText(scorePadded, scoreX, y);
    this.ctx.fillText(`HI ${highScorePadded}`, highScoreX, y);
  }

  playScoreSound() {
    // Reproduz o som de pontuação ao alcançar múltiplos de 100
    this.scoreSound.play().catch((error) => {
      console.error("Erro ao reproduzir o som de pontuação:", error);
    });
  }
}
