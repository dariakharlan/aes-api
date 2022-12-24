from app import app


def test_flow_cbc():
    with app.test_client() as test_client:
        msg = 'Доброго ранку!'
        key = 'most_secure_key!most_secure_key!'
        algorithm = 'CBC'
        resp = test_client.post('/encrypt', json={
            'message_body': msg,
            'encryption_key': key,
            'algorithm': algorithm
        })
        print(resp.get_json())
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'iv' in data
        assert 'enc_message' in data

        resp = test_client.post('/decrypt', json={
            'enc_message': data['enc_message'],
            'encryption_key': key,
            'algorithm': algorithm,
            'iv': data['iv']
        })
        print(resp.text)
        assert resp.status_code == 200
        assert resp.json['message'] == msg


def test_flow_ctr():
    with app.test_client() as test_client:
        msg = 'Доброго ранку!'
        key = 'most_secure_key!'
        algorithm = 'CTR'
        resp = test_client.post('/encrypt', json={
            'message_body': msg,
            'encryption_key': key,
            'algorithm': algorithm
        })
        print(resp.get_json())
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'nonce' in data
        assert 'enc_message' in data

        resp = test_client.post('/decrypt', json={
            'enc_message': data['enc_message'],
            'encryption_key': key,
            'algorithm': algorithm,
            'nonce': data['nonce']
        })
        print(resp.text)
        assert resp.status_code == 200
        assert resp.json['message'] == msg


def test_decrypt_wrong_key():
    with app.test_client() as test_client:
        msg = 'Доброго ранку!'
        key = 'most_secure_key!'
        algorithm = 'CBC'
        resp = test_client.post('/encrypt', json={
            'message_body': msg,
            'encryption_key': key,
            'algorithm': algorithm
        })
        data = resp.get_json()

        resp = test_client.post('/decrypt', json={
            'enc_message': data['enc_message'],
            'encryption_key': 'worng_key',
            'algorithm': algorithm,
            'iv': data['iv']
        })
        print(resp.text)
        assert resp.status_code == 400


def test_encrypt_invalid_key():
    with app.test_client() as test_client:
        msg = 'Доброго ранку!'
        key = 'keyofincorrectlength'
        algorithm = 'CBC'
        resp = test_client.post('/encrypt', json={
            'message_body': msg,
            'encryption_key': key,
            'algorithm': algorithm
        })
        print(resp.text)
        assert resp.status_code == 400
