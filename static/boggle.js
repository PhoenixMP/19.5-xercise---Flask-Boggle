const $submitButton = $('#submit-button');
const $form = $('form')
const $guessMessage = $('.guess-message');
const $score = $('.score');
const $timeout = $('<p>You are out of time</p>')
const $restartButton = $('<button class="restart">Play again?</button>')
$score.hide();

class BoggleGame {
    constructor(secs = 60) {
        this.secs = secs
        this.highScore = 0;
        this.score = 0;
        this.yourWords = []

        /* After countdown,emove ability to add words, generate restart button */
        this.setTimer = setTimeout(this.timeout.bind(this), this.secs * 1000)


        $submitButton.on("click", this.submitGuess.bind(this));


    }



    timeout() {
        $form.remove();
        $('main').append($timeout);
        $('main').append($restartButton)
        $restartButton.on("click", this.reload.bind(this));
    }



    /* check server if word is valid. Update the word list and score  */
    async submitGuess(evt) {
        evt.preventDefault();
        const word = $('#guess').val();
        const response = await axios.get(`/guess?guess=${word}`);
        const message = response.data.result;
        this.getMessage(message);
        if (message === "ok" && this.checkForRepeats(word)) {
            this.updateScore(word);
            this.showWords();
        };
    };


    /* Post the score to the serve if it's the new high-score, reload the page */
    async reload(evt) {
        evt.preventDefault();
        console.log('what')
        if (this.score > this.highScore) {
            this.highScore = this.score
            await axios.post("/score", { 'score': this.highScore })
        }
        location.href = '/';


    }



    /* Display a message for player based on server response to word */
    getMessage(message) {
        if (message === "ok") {
            $guessMessage.text(`You guessed right!`);
        } else if (message === "not-word") {
            $guessMessage.text(`Your guess is not a word`);

        } else if (message === "not-on-board") {
            $guessMessage.text(`Your guess is not present`);
        }

    }

    /* Verify that the user has not already used a word */
    checkForRepeats(word) {
        return !this.yourWords.some(val => val === word.toLowerCase())
    }

    /* Update the score with the points from the new word, add valid guess to word list */
    updateScore(word) {
        const newScore = word.length;
        this.score += newScore;
        $score.show()
        $score.text(`Your score: ${this.score} points!`)
        this.yourWords.push(word)
    }

    /* Display the list of valid word guesses */
    showWords() {
        const $yourwords = $('<ul>Your words are:</ul>')
        for (this.word of this.yourWords) {
            $yourwords.append($(`<li>${this.word.toLowerCase()}</li>`))
        }
        $score.append($yourwords)
    }
}