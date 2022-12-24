# Encryption API

### How to run

1. Install requirements
```
pip install -r requirements.txt
```
2. Run the app
```
python -m flask run
```

### Run tests
```
pytest test.py
```

### Run CLI tool
```
python cli.py --help
```

## API docs
Supports `Content-Type: application/json` only

### Encrypt

```
POST /encrypt
```

Parameters:
- `encryption_key` - Required, must be 16, 24, or 32 bytes length
- `message_body` - Required, text to encrypt
- `algorithm` - Required, AES mode, allowed values are `CBC, CTR`
- `encoding` - Optional, default `utf-8`

Example:

```bash
$ curl -X POST localhost:5000/encrypt \
-H 'Content-Type: application/json' \
-d '{
"encryption_key": "most_secure_key!",
"message_body": "Good morning!",
"algorithm": "CBC"
}'
$ {"enc_message":"6qOQX60JlE3dO8xJHJW6CQ==","iv":"zxyo7yIgGTGP5CH66gksLw=="}
```


### Decrypt

```
POST /decrypt
```

Parameters:
- `encryption_key` - Required, must be 16, 24, or 32 bytes length
- `enc_message` - Required, text to dencrypt
- `algorithm` - Required, AES mode, allowed values are `CBC, CTR`
- `encoding` - Optional, default `utf-8`
- `iv` - Required if algorithm is `CBC`
- `nonce` - Required if algorithm is `CTR`

Example:
```bash
$ curl -X POST localhost:5000/decrypt \
-H 'Content-Type: application/json' \
-d '{
"encryption_key": "most_secure_key!",
"enc_message":"6qOQX60JlE3dO8xJHJW6CQ==",
"iv":"zxyo7yIgGTGP5CH66gksLw==",
"algorithm": "CBC"
}'
$ {"message":"Good morning!"}
```

### Version
```
GET /version
```

Example:
```bash
$ curl -X POST localhost:5000/version
$ {"version":"0.0.1"}
```