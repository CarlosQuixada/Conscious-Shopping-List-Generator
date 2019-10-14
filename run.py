import json

from flask import Flask, request, jsonify

from app.genetic_algorithm import GeneticAlgorithm

api = Flask('CSLG')


@api.route('/')
def heath_check():
    """
        Health check method
    :return: message and status 200 to confirm API is standing
    """

    return "Faaaaaalllaaaa Galera blz?", 200


@api.route('/generate-list', methods=['POST'])
def generate_list():
    """
        Method responsible for generating the purchase suggestion, based on past parameters
    :return: list with suggestions
    """

    try:
        dreams_string = json.dumps(request.json, ensure_ascii=False)
        dreams = json.loads(dreams_string)

        genetic_algorithm = GeneticAlgorithm(dreams['limit'], dreams['dreams'])
        response = genetic_algorithm.generate_list()

        return response

    except Exception as e:
        return jsonify({"Exception": str(e)})


@api.errorhandler(404)
def page_not_found(e):
    """
        Método responsável pelo tratamento do erro 404 de acesso
    :param e: Exceção ocorrida
    :return: predição vazia
    """
    pred = {"predictions": [None, None, None], "complain": None, "Exception": e}
    return json.dumps(pred), 404


@api.errorhandler(500)
def page_not_found(e):
    """
        Método responsável pelo tratamento do erro 500 de acesso
    :param e: Exceção ocorrida
    :return: predição vazia
    """
    pred = {"predictions": [None, None, None], "complain": None, "Exception": e}
    return json.dumps(pred), 500


@api.errorhandler(400)
def page_not_found(e):
    """
        Método responsável pelo tratamento do erro 400 de acesso
    :param e: Exceção ocorrida
    :return: predição vazia
    """
    pred = {"predictions": [None, None, None], "complain": None, "Exception": e}
    return json.dumps(pred), 400


if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=False)
