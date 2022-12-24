import jsonschema
import cypher_mode_operator
from flask import Flask, jsonify, request


app = Flask(__name__)

VERSION = '0.0.1'


@app.route('/version', methods=['GET'])
def version():
    return jsonify({'version': '0.0.1'})


@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    schema = {
        "type": "object",
        "properties": {
            "algorithm": {"type": "string", "enum": cypher_mode_operator.modes_list},
            "encryption_key": {"type": "string"},
            "message_body": {"type": "string"},
        },
        "required": ["algorithm", "encryption_key", "message_body"]
    }
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        return jsonify({'error': str(e)}), 400

    try:
        mode_operator = cypher_mode_operator.get(data['algorithm'], data)
        return jsonify(mode_operator.encrypt())
    except (cypher_mode_operator.ValidationError, cypher_mode_operator.EncryptionError, NotImplementedError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    schema = {
        "type": "object",
        "properties": {
            "algorithm": {"type": "string", "enum": cypher_mode_operator.modes_list},
            "encryption_key": {"type": "string"},
            "enc_message": {"type": "string"},
        },
        "required": ["algorithm", "encryption_key", "enc_message"]
    }
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        return jsonify({'error': str(e)}), 400

    try:
        mode_operator = cypher_mode_operator.get(data['algorithm'], data)
        return jsonify(mode_operator.decrypt())
    except (cypher_mode_operator.ValidationError, cypher_mode_operator.DecryptionError, NotImplementedError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
