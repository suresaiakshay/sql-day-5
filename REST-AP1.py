from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
users = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
    2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
}
next_id = 3  # Tracks the next available ID

@app.route('/')
def home():
    return "User Management API - Use /users endpoints"

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

# GET single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        return jsonify({"error": "Bad request, name and email are required"}), 400
    
    user = {
        "id": next_id,
        "name": request.json['name'],
        "email": request.json['email']
    }
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201

# PUT - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Bad request, no data provided"}), 400
    
    user = users[user_id]
    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    
    return jsonify(user)

# DELETE - Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    del users[user_id]
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)