from flask import Flask, render_template, request
import numpy as np
import matplotlib as mpl

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/frequency', methods=['POST'])
def frequency():
    textChunk = str(request.form.get('textChunk'))
    phrase = str(request.form.get('phrase'))
    letter_frequency = {}
    for i in textChunk:
        for x in i.upper():
            if x in letter_frequency and x != " " and x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ': 
                letter_frequency[x] += 1
            elif x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                letter_frequency[x] = 1
    result = str(sorted(letter_frequency.items(), key=lambda i: i[1]))
    result = result[1:-1]
    entry= f"Your character count totals: {result}"
    phraseCount = f"The phrase '{phrase}' appears {textChunk.count(phrase)} times"
    return render_template('frequency.html', **locals())

@app.route('/strength', methods=['POST'])
def strength():
    password = str(request.form.get('passChunk'))
    A = int(request.form.get('A'))
    N = len(password)
    T = (A**N) #total possibilities
    D = T/((10**9)*3600) #Bruteforce time in years
    X = 2*np.log2(D)
    if X > 0:
        possible = (f"\nTotal possibilities: {T}")
        years = f"Years to Guess: {D}"
        brute = f"Bruteforce hours: {X}"
    else:
        possible = (f"\nTotal possibilities: {T}")
        years = f"Years to Guess: {D}"
        brute = "You may want to change that password..."
    return render_template('strength.html', **locals())

@app.route('/encode', methods=['POST'])
def encode():
    text = str(request.form.get('encryptChunk')).lower()
    subCiph = str(request.form.get('subciphChunk')).lower().strip()
    alph = 'abcdefghijklmnopqrstuvwxyz'
    encrypted = ''
    for i in text:
        if i in alph:
            index = alph.find(i)
            encrypted += subCiph[index]
        else:
            encrypted += i
    return render_template('encode.html', **locals())

@app.route('/decode', methods=['POST'])
def decode():
    text = str(request.form.get('decryptChunk')).lower()
    subCiph = str(request.form.get('subChunk')).lower().strip()
    alph = 'abcdefghijklmnopqrstuvwxyz'
    decrypted = ''
    for i in text:
        if i in alph:
            index = subCiph.find(i)
            decrypted += alph[index]
        else:
            decrypted += i
    return render_template('decode.html', **locals())


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")