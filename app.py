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

@app.route('/consultar', methods=['POST'])
def consultar():
    req_data = request.json
    dado_consulta = req_data['dadoConsulta']
    tipo_consulta = req_data['tipoConsulta']
    data = ler_dados()  # Ler os dados toda vez que a função é chamada
    resultados = consulta(data, dado_consulta, tipo_consulta)
    return jsonify(resultados)

# Função para atualizar um dado
def atualizaDado(csv_file, dadoAtualizacao, tipoAtualizacao, novoValor):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)
    linhas[dadoAtualizacao][tipoAtualizacao] = novoValor
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

@app.route('/atualizar-dado', methods=['POST'])
def atualizar_dado():
    data = request.json
    atualizaDado('smoking.csv', int(data['dadoAtualizacao']), int(data['tipoAtualizacao']), data['novoValor'])
    return jsonify({"message": "Dado atualizado com sucesso"})

# Função para inserir uma nova linha
def inserirNovaLinha(novaLinha):
    with open('smoking.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(novaLinha)

@app.route('/inserir-nova-linha', methods=['POST'])
def inserir_nova_linha_route():
    data = request.json['novaLinha']
    inserirNovaLinha(data)
    return jsonify({"message": "Nova linha inserida com sucesso"})

# Função para deletar uma linha
def deletaLinha(idLinha):
    linhas = []
    with open('smoking.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            linhas.append(row)
    with open('smoking.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas[:idLinha] + linhas[idLinha+1:])

@app.route('/deletar-linha', methods=['POST'])
def deletar_linha_route():
    id_linha = request.json['idLinha']
    deletaLinha(int(id_linha))
    return jsonify({"message": "Linha deletada com sucesso"})


@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

if __name__ == '__main__':
    app.run(debug=True, port=8000)


