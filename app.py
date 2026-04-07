from flask import Flask, request, jsonify
from models.task import Task


app = Flask(__name__)

tasks = []
task_id_control = 1
#crud = create, read, update, delete

@app.route('/tasks', methods=['POST'])
def create_task():
  global task_id_control
  data = request.get_json()
  new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
  task_id_control += 1
  tasks.append(new_task)
  print(tasks)

  return {
    'message': 'Task created successfully', 'id': new_task.id
  }, 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
  task_list = []
  # ou task_list = [task.to_dict() for task in tasks]
  for task in tasks:
    task_list.append(task.to_dict())

  output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
          }
  return jsonify(output), 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict()), 200
  
  return {
    'message': 'Task not found'
  }, 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
  task = None
  for t in tasks:
    if t.id == id:
      task = t
      break

  print(task)
  if tasks == None:
    return {
      'message': 'Task not found'
    }, 404
  
  data = request.get_json()
  task.title = data['title']
  task.description = data['description']
  task.completed = data['completed']
  print(task)

  return {
    'message': 'Task updated successfully'
  }, 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  task = None
  for t in tasks:
    if t.id == id:
      task = t
      break
  
  if task == None:
    return {
      'message': 'Task not found'
    }, 404

  tasks.remove(task)
  return {
    'message': 'Task deleted successfully'
  }, 200

if __name__ == '__main__':
  app.run(debug=True)