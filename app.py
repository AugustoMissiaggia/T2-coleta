import csv
from flask import Flask, jsonify, request
app = Flask(__name__)

# Função para ler dados do arquivo CSV
def ler_dados():
    data = []
    with open('smoking.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(dict(row))
    return data

# Função para consultar dados
def consulta(data, dadoConsulta, tipoConsulta):
    resultados = []
    for item in data:
        if item[tipoConsulta] == dadoConsulta:
            resultados.append(item)
    return resultados

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if request.method == 'POST':
        req_data = request.json
        dado_consulta = req_data['dadoConsulta']
        tipo_consulta = req_data['tipoConsulta']
    else:  # GET
        dado_consulta = request.args.get('dadoConsulta')
        tipo_consulta = request.args.get('tipoConsulta')
    
    if not dado_consulta or not tipo_consulta:
        return jsonify({"error": "Parâmetros insuficientes"}), 400

    data = ler_dados()
    resultados = consulta(data, dado_consulta, tipo_consulta)
    return jsonify(resultados)

@app.route('/atualizar-dado', methods=['GET', 'POST'])
def atualizar_dado():
    if request.method == 'POST':
        data = request.json
    else:  # GET
        data = request.args
    
    atualizaDado('smoking.csv', int(data['dadoAtualizacao']), int(data['tipoAtualizacao']), data['novoValor'])
    return jsonify({"message": "Dado atualizado com sucesso"})

@app.route('/inserir-nova-linha', methods=['GET', 'POST'])
def inserir_nova_linha_route():
    if request.method == 'POST':
        data = request.json['novaLinha']
    else:  # GET
        data = request.args.getlist('novaLinha')
    
    inserirNovaLinha(data)
    return jsonify({"message": "Nova linha inserida com sucesso"})

@app.route('/deletar-linha', methods=['GET', 'POST'])
def deletar_linha_route():
    if request.method == 'POST':
        id_linha = request.json['idLinha']
    else:  # GET
        id_linha = request.args.get('idLinha')
    
    deletaLinha(int(id_linha))
    return jsonify({"message": "Linha deletada com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)


