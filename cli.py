from app import app
from cypher_mode_operator import modes_list
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("method", choices=['encrypt', 'decrypt'])
parser.add_argument("--message_body")
parser.add_argument("--enc_message")
parser.add_argument("--iv")
parser.add_argument("--nonce")
parser.add_argument("--encryption_key", required=True)
parser.add_argument("--algorithm", required=True, choices=modes_list)
args = vars(parser.parse_args())
print(args)

with app.test_client() as test_client:
    resp = test_client.post(args['method'], json=args)
    print(resp.get_json())

