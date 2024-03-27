from flask import Flask, render_template, request, jsonify
from Task_5.vector_search import find_top_n, read_inverted_index, calculate_vector_for_all_documents

app = Flask(__name__)
inverted_index = None
vectors = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global inverted_index, vectors
    if request.method == 'POST':
        query = request.form['query']
        if inverted_index is None:
            inverted_index = read_inverted_index()
        if vectors is None:
            vectors = calculate_vector_for_all_documents(inverted_index)
        results = find_top_n(query, 10, inverted_index, vectors)
        return jsonify(results=results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
