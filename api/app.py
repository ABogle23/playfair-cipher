from flask import Flask, render_template, request

app = Flask(__name__)




@app.route("/")
def playfair():
    return render_template("index.html")


@app.route("/encoded", methods=["POST"])
def encoded():
    input_codeword = request.form.get("codeword")
    input_word = request.form.get("word")
    output_encoded_word = playfairCipher(input_codeword, input_word)
    return render_template(
        "encoded.html", codeword=input_codeword, word=input_word, encoded_word=output_encoded_word)


def playfairCipher(codeword,word):

    # if not codeword or not word:
    #     return "Error"

    def create_grid(codeword):
        grid = []
        letters = [c for c in codeword.upper() if c.isalpha()]
        seen = set()
        for letter in letters:
            if letter not in seen and letter != 'J':
                seen.add(letter)
                grid.append(letter)
        for ch in range(65, 91):
            if chr(ch) not in seen and chr(ch) != 'J':
                seen.add(chr(ch))
                grid.append(chr(ch))
        return [grid[i:i + 5] for i in range(0, 25, 5)]

    def process_text(word):
        processed = ""
        word = word.upper().replace("J", "I")
        i = 0
        while i < len(word):
            a = word[i]
            b = ''
            if i + 1 < len(word):
                b = word[i + 1]
            if a == b or b == '':
                processed += a + 'X'
                i += 1
            else:
                processed += a + b
                i += 2
        return processed

    def playfair_encode(grid, word):
        def find_position(letter):
            for i, row in enumerate(grid):
                for j, val in enumerate(row):
                    if val == letter:
                        return i, j

        encoded = ""
        for i in range(0, len(word), 2):
            a, b = word[i], word[i + 1]
            ax, ay = find_position(a)
            bx, by = find_position(b)

            if ax == bx:
                encoded += grid[ax][(ay + 1) % 5] + grid[bx][(by + 1) % 5]
            elif ay == by:
                encoded += grid[(ax + 1) % 5][ay] + grid[(bx + 1) % 5][by]
            else:
                encoded += grid[ax][by] + grid[bx][ay]

        return encoded

    grid = create_grid(codeword)
    processed_word = process_text(word)
    encoded_word = playfair_encode(grid, processed_word)

    return encoded_word
