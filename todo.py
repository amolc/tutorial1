from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory storage
todos = []
id_counter = 1

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    global id_counter
    if not request.json or 'title' not in request.json:
        abort(400, description="Title is required")
    
    todo = {
        'id': id_counter,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'completed': request.json.get('completed', False)
    }
    todos.append(todo)
    id_counter += 1
    return jsonify(todo), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo not found")
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing todo"""
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo not found")
    
    if not request.json:
        abort(400, description="Invalid request body")
        
    todo['title'] = request.json.get('title', todo['title'])
    todo['description'] = request.json.get('description', todo['description'])
    todo['completed'] = request.json.get('completed', todo['completed'])
    
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo not found")
    
    todos = [item for item in todos if item['id'] != todo_id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
