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


def atualizaLinha(csv_file, linha, novosValores):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    if 0 <= linha < len(linhas):
        # Atualize a linha inteira
        linhas[linha] = novosValores
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(linhas)
    else:
        return False  # Linha não encontrada
    return True


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


@app.route('/pessoas', methods=['GET'])
def obter_todas_as_pessoas():
    data = ler_dados()
    return jsonify(data)


@app.route('/pessoas/<int:id_pessoa>', methods=['GET'])
def obter_pessoa(id_pessoa):
    data = ler_dados()
    pessoa = next((item for item in data if int(item['id']) == id_pessoa), None)
    if pessoa:
        return jsonify(pessoa)
    else:
        return jsonify({"error": "Pessoa não encontrada"}), 404


@app.route('/consultar', methods=['GET'])
def consultar():
    dado_consulta = request.json.get('dadoConsulta')
    tipo_consulta = request.json.get('tipoConsulta')

    if not dado_consulta or not tipo_consulta:
        return jsonify({"error": "Parâmetros insuficientes"}), 400

    data = ler_dados()
    resultados = consulta(data, dado_consulta, tipo_consulta)
    return jsonify(resultados)

@app.route('/atualizar-dado/<int:linha>', methods=['PUT'])
def atualizar_dado(linha):
    novosValores = request.json.get('novosValores')
    if not novosValores:
        return jsonify({"error": "Novos valores não fornecidos"}), 400


    if atualizaLinha('smoking.csv', linha, novosValores):
        return jsonify({"message": "Linha atualizada com sucesso"})
    else:
        return jsonify({"error": "Linha não encontrada"}), 404



@app.route('/inserir-nova-linha', methods=['POST'])
def inserir_nova_linha_route():
    novaLinha = request.json['novaLinha']
    inserirNovaLinha(novaLinha)
    return jsonify({"message": "Nova linha inserida com sucesso"})

@app.route('/deletar-linha', methods=['DELETE'])
def deletar_linha_route():
    id_linha = request.json['idLinha']
    deletaLinha(int(id_linha))
    return jsonify({"message": "Linha deletada com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
