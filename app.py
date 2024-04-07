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


def atualizaDado(csv_file, dadoAtualizacao, tipoAtualizacao, novoValor):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)
    linhas[dadoAtualizacao][tipoAtualizacao] = novoValor
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)


def inserirNovaLinha(novaLinha):
    with open('smoking.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(novaLinha)

def deletaLinha(idLinha):
    linhas = []
    with open('smoking.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            linhas.append(row)
    with open('smoking.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas[:idLinha] + linhas[idLinha+1:])




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

@app.route('/dados/<int:linha>', methods=['PUT'])
def atualizar_dados(linha):
    dados = request.json
    tipoAtualizacao = dados['tipoAtualizacao']
    novoValor = dados['novoValor']
    atualizaDado('smoking.csv', linha, tipoAtualizacao, novoValor)
    return jsonify({"message": "Dado atualizado com sucesso"})

@app.route('/dados/<int:linha>', methods=['DELETE'])
def deletar_dados(linha):
    deletaLinha(linha)
    return jsonify({"message": "Linha deletada com sucesso"})
if __name__ == '__main__':
    app.run(debug=True)


