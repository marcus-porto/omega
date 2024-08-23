from flask import jsonify, request

def init_routes(app, celery):

    @celery.task
    def process_data(data):
        print(f"Processando: {data}")
        return f"Processado: {data}"

    @app.route('/create_task', methods=['POST'])
    def create_task():
        data = request.json.get('data')
        task = process_data.apply_async(args=[data])
        return jsonify({'task_id': task.id}), 202

    @app.route('/get_task/<task_id>', methods=['GET'])
    def get_task(task_id):
        task = process_data.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Aguardando processamento...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'result': task.result,
            }
        else:
            response = {
                'state': task.state,
                'status': str(task.info),
            }
        return jsonify(response)

    @app.route('/process_task/<task_id>', methods=['POST'])
    def process_task(task_id):
        task = process_data.AsyncResult(task_id)
        if task.state == 'PENDING':
            task_result = task.get()
            return jsonify({'task_id': task_id, 'status': 'Processed', 'result': task_result}), 200
        return jsonify({'status': 'Task already processed or failed'}), 400
