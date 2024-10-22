# Quiz-Bot
Вот пример MD файла, который описывает основные функции квиз бота:

```md
---
type: game
title: My Quiz Game
---

### Functions

#### StartGame()
This function starts the game by asking the first question.
```javascript
async function StartGame() {
    // Get the first question from the questions array
    const currentQuestion = questions[0];
    
    // Display the question
    await context.sendActivity({
        type: 'message',
        message: currentQuestion.question,
        choices: currentQuestion.choices
    });
}
```

#### CheckAnswer(choice)
This function checks if the given choice is correct for the current question.
```javascript
function CheckAnswer(choice) {
    if (currentQuestion.correctChoice === choice) {
        return true;
    } else {
        return false;
    }
}
```

#### NextQuestion()
This function advances to the next question in the queue.
```javascript
async function NextQuestion() {
    // Remove the current question from the array
    questions.shift();
    
    // If there are no more questions, end the game
    if (!questions.length) {
        await context.sendActivity('There are no more questions. Thanks for playing!');
        return;
    }
    
    // Get the next question from the remaining questions
    const currentQuestion = questions[0];
    
    // Display the question
    await context.sendActivity({
        type: 'message',
        message: currentQuestion.question,
        choices: currentQuestion.choices
    });
}
```

#### ShowResults()
This function displays the final results of the game.
```javascript
async function ShowResults() {
    // Calculate the number of correct answers
    const totalCorrectAnswers = questions.filter((q) => q.correctChoice).length;
    
    // Calculate the percentage of correct answers
    const percentageCorrect = ((totalCorrectAnswers / questions.length) * 100).toFixed(2);
    
    // Send the final result message
    await context.sendActivity(`You answered ${totalCorrectAnswers} out of ${questions.length} questions correctly (${percentageCorrect}%).`);
}
```

### Main Flow

#### OnTurnAsync
The main logic of the bot is handled here.
```javascript
async function OnTurnAsync(context, next) {
    if (!context.responded && context.activity.type === 'message') {
        switch (context.activity.text) {
            case '/start':
                await StartGame();
                break;
            
            default:
                try {
                    const choice = parseInt(context.activity.text);
                    if (CheckAnswer(choice)) {
                        await context.sendActivity('Correct answer! Moving on to the next question...');
                        await NextQuestion();
                    } else {
                        await context.sendActivity('Incorrect answer. Try again!');
                    }
                } catch (error) {
                    await context.sendActivity('Please enter a valid choice.');
                }
                break;
        }
    }

    // By calling next() you ensure that the next BotHandler is run.
    await next();
}
```

### Questions
Here is an example of how your questions can be structured.

#### Question 1
```javascript
const questions = [
    {
        question: 'What is the capital of Russia?',
        choices: ['Moscow', 'Saint Petersburg', 'Novosibirsk'],
        correctChoice: 0
    },
    {
        question: 'Who is the President of Russia?',
        choices: ['Vladimir Putin', 'Dmitry Medvedev', 'Mikhail Gorbachev'],
        correctChoice: 0
    },
    // Add more questions here...
];
```

### Actions
Here are some actions defined to handle various scenarios.

#### HelpAction
```javascript
const helpText = `Welcome to my quiz game! To play, simply send a number corresponding to your choice when asked a question.`;

async function HelpAction(context) {
    await context.sendActivity(helpText);
}
```

### Initialize
Here we initialize our bot with the main handler...
