from flask import Flask, request, jsonify  # Importa o Flask e funções úteis para manipular requisições e respostas JSON.
from models.task import Task  # Importa a classe Task do módulo models, onde cada tarefa será representada como um objeto Task.

# Cria uma instância do Flask para configurar o app
app = Flask(__name__)

# Controle CRUD: Create, Read, Update, Delete (Criar, Ler, Atualizar, Deletar)
# Aqui, estamos manipulando tarefas que serão armazenadas em uma lista para fins de teste.

tasks = []  # Lista que armazenará as tarefas (in-memory storage)
task_id_control = 1  # Variável para controlar o ID único de cada tarefa criada


# Rota para criar uma nova tarefa
@app.route('/tasks', methods=['POST'])
def create_task():
  global task_id_control  # Usa a variável global task_id_control para incrementar o ID das tarefas
  data = request.get_json()  # Recebe dados JSON da requisição e os armazena na variável `data`
  
  # Cria uma nova tarefa usando o ID atual e os dados fornecidos
  new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))
  task_id_control += 1  # Incrementa o ID para a próxima tarefa
  
  # Adiciona a nova tarefa na lista de tarefas
  tasks.append(new_task)
  
  # Exibe a lista de tarefas atualizada no console para verificação
  print(tasks)
  
  # Retorna uma mensagem de sucesso em formato JSON
  return jsonify({"message": "Nova tarefa criada com sucesso"})


# Rota para listar todas as tarefas
@app.route('/tasks', methods=['GET'])
def get_tasks():
  # Converte cada tarefa em dicionário (utilizando o método to_dict() definido na classe Task)
  task_list = [task.to_dict() for task in tasks]

  # Cria um dicionário com a lista de tarefas e o total de tarefas
  output = {
    "tasks": task_list,
    "total_tasks": len(task_list)
  }
  
  # Retorna o dicionário em formato JSON
  return jsonify(output)


# Rota para obter uma tarefa específica com base no ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  # Procura uma tarefa na lista de tarefas com o ID especificado
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict())  # Se encontrar, retorna a tarefa em formato JSON
  
  # Se a tarefa não for encontrada, retorna uma mensagem de erro e status 404
  return jsonify({"message": "Não foi possível encontrar a atividade"}), 404


# Rota para atualizar uma tarefa específica com base no ID
@app.route('/tasks/<int:id>', methods=["PUT"])
def update_task(id):
  task = None  # Variável para armazenar a tarefa encontrada (se existir)

  # Procura a tarefa com o ID especificado
  for t in tasks:
    if t.id == id:
      task = t
      break
    
  if task == None:
    # Se a tarefa não for encontrada, retorna uma mensagem de erro e status 404
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

  # Obtém os novos dados da requisição
  data = request.get_json()
  
  # Atualiza os atributos da tarefa encontrada com os novos dados
  task.title = data['title']
  task.description = data['description']
  task.completed = data['completed']
  
  # Retorna uma mensagem de sucesso em formato JSON
  return jsonify({"message": "Tarefa atualizada com sucesso"})


# Rota para deletar uma tarefa específica com base no ID
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  task = None  # Variável para armazenar a tarefa encontrada (se existir)

  # Procura a tarefa com o ID especificado
  for t in tasks:
    if t.id == id:
      task = t
      break

  if not task:
    # Se a tarefa não for encontrada, retorna uma mensagem de erro e status 404
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
  # Remove a tarefa da lista de tarefas
  tasks.remove(task)
  
  # Retorna uma mensagem de sucesso em formato JSON
  return jsonify({"message": "Tarefa deletada com sucesso"})


# Inicializa o app Flask se este arquivo for executado como script principal
if __name__ == "__main__":
  app.run(debug=True)  # Inicia o servidor Flask em modo de depuração (debug)
