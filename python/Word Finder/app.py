from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def word_find(name, age):
    return f"Hello, {name}! You are {age} years old."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find', methods=['POST'])
def find():
    data = request.get_json()
    user_name = data['name']
    user_age = data['age']
    message = word_find(user_name, user_age)
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)