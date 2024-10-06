from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in a real application

# Simple word list suitable for kids
word_list = ["apple", "grape", "peach", "berry", "melon"]

@app.route('/')
def home():
    session['word'] = random.choice(word_list)
    session['attempts'] = 0
    session['guesses'] = []  # Store guesses and feedback
    return render_template('index.html', guesses=session['guesses'])

@app.route('/guess', methods=['POST'])
def guess():
    guess_word = request.form['guess'].lower()
    correct_word = session['word']
    session['attempts'] += 1

    if guess_word == correct_word:
        return render_template('result.html', result='Congratulations! You guessed it!', word=correct_word)

    feedback = []
    for i, letter in enumerate(guess_word):
        if letter == correct_word[i]:
            feedback.append('🟩')  # Green for correct letter in correct place
        elif letter in correct_word:
            feedback.append('🟨')  # Yellow for correct letter in wrong place
        else:
            feedback.append('⬜')  # White for incorrect letter

    # Combine letters and feedback for storage
    combined_feedback = " ".join(f"{letter} {color}" for letter, color in zip(guess_word, feedback))

    # Append the guess and its combined feedback to the session
    session['guesses'].append((guess_word, combined_feedback))
    
    return render_template('index.html', feedback=''.join(feedback), attempts=session['attempts'], guesses=session['guesses'])

@app.route('/reset')
def reset():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
