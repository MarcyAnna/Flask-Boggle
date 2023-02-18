let words = new Set();
let score = document.querySelector('.score');
let addScore = 0;
let gameTimer;
let timer = document.querySelector('.timer');
let timeLeft = 60;
let message = document.querySelector('.message');
const form = document.querySelector('.guess');
let newGame = document.querySelector('.new-game');
let startedTimer = false;

function updateTimer(){
    timeLeft = timeLeft -1;
    if (timeLeft >= 0) {
    timer.innerHTML = timeLeft;
    }
    else {
        gameOver();
    }
}

function startTimer() {
    console.log("startedTimer");
    gameTimer = setInterval(updateTimer, 1000);
    updateTimer();
}

form.addEventListener('submit', handleSubmit);

async function handleSubmit(evt) {
    evt.preventDefault();
    if (!startedTimer) {
        startedTimer = true;
        startTimer();
    }
    const getWord = document.querySelector(".word");
    const addWord = document.querySelector(".add-words");
    let word = getWord.value;

    if (words.has(word)) {
        message.innerHTML = `${word} already found. try again`;
        form.reset();
        getWord.focus();
        return;
    }

    const res = await axios.get("/validate", { params: { word: word } });
    if (res.data.result === "not-word") {
        giveResult(`${word} is not a valid word`);
    }
    else if (res.data.result === "not-on-board") {
        giveResult(`${word} not on board`);
    }
    else {
        addScore += 1;
        score.innerHTML = addScore;
        words.add(word);
        giveResult(`${word} has been added to your score`);
        addWord.append(`${word} `);
    }
    form.reset();
    getWord.focus();

}

function giveResult(msg) {
    message.innerHTML = `${msg}`;
}

async function gameScore(){
    const res = await axios.post("/final-score", { score: score.innerHTML });
    if (res.data.newHighScore){
        message.innerHTML = `New High Score: ${score.innerHTML}`;
    }
    else {
        message.innerHTML = `Final Score: ${score.innerHTML}`;
    }
}

async function gameOver(){
    clearInterval(gameTimer);
    startedTimer = false;
    await gameScore();
}

async function startNewGame(){
    window.location.reload();
}

newGame.addEventListener('click', startNewGame);