from abc import ABC, abstractmethod
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class CypherModeOperator(ABC):
    def __init__(self, input_data: dict):
        self.input_data = input_data
        self.encryption_key = input_data['encryption_key'].encode('utf-8')
        self.validate_encryption_key()
        self.encoding = input_data.get('encoding', 'utf-8')

    def validate_encryption_key(self):
        if len(self.encryption_key) not in (16, 24, 32):
            raise ValidationError('Encryption key length must be 16, 24 or 32 bytes')

    def _run_encryption(self, msg: bytes, **kwargs):
        try:
            cipher = AES.new(self.encryption_key, self.get_mode(), *kwargs)
            ct_bytes = cipher.encrypt(msg)
        except (KeyError, ValueError) as e:
            raise EncryptionError(str(e))
        return cipher, ct_bytes

    def _run_decryption(self, msg: bytes, **kwargs) -> bytes:
        try:
            cipher = AES.new(self.encryption_key, self.get_mode(), **kwargs)
            dt = cipher.decrypt(msg)
        except (ValueError, KeyError) as e:
            raise DecryptionError(str(e))

        return dt

    @abstractmethod
    def get_mode(self) -> int:
        pass

    @abstractmethod
    def encrypt(self) -> dict:
        pass

    @abstractmethod
    def decrypt(self) -> dict:
        pass


class CBCOperator(CypherModeOperator):
    def get_mode(self) -> int:
        return AES.MODE_CBC

    def encrypt(self) -> dict:
        msg = pad(self.input_data['message_body'].encode(self.encoding), AES.block_size)
        cipher, ct_bytes = self._run_encryption(msg)

        iv = b64encode(cipher.iv).decode(self.encoding)
        ct = b64encode(ct_bytes).decode(self.encoding)
        return {'iv': iv, 'enc_message': ct}

    def decrypt(self) -> dict:
        try:
            iv = b64decode(self.input_data['iv'])
            ct = b64decode(self.input_data['enc_message'])
        except (KeyError, ValueError, TypeError) as e:
            raise ValidationError(e)

        dt = self._run_decryption(ct, iv=iv)

        return {'message': unpad(dt, AES.block_size).decode(self.encoding)}


class CTROperator(CypherModeOperator):
    def get_mode(self) -> int:
        return AES.MODE_CTR

    def encrypt(self) -> dict:
        msg = self.input_data['message_body'].encode(self.encoding)
        cipher, ct_bytes = self._run_encryption(msg)

        nonce = b64encode(cipher.nonce).decode(self.encoding)
        ct = b64encode(ct_bytes).decode(self.encoding)
        return {'nonce': nonce, 'enc_message': ct}

    def decrypt(self) -> dict:
        try:
            nonce = b64decode(self.input_data['nonce'])
            ct = b64decode(self.input_data['enc_message'])
        except (KeyError, ValueError, TypeError) as e:
            raise ValidationError(e)

        dt = self._run_decryption(ct, nonce=nonce)

        return {'message': dt.decode(self.encoding)}


class CypherModeOperatorException(Exception):
    pass


class ValidationError(CypherModeOperatorException):
    pass


class EncryptionError(CypherModeOperatorException):
    pass


class DecryptionError(CypherModeOperatorException):
    pass


_modes = {
    'CBC': CBCOperator,
    'CTR': CTROperator,
}


modes_list = list(_modes.keys())


def get(aes_mode: str, input_data: dict) -> CypherModeOperator:
    aes_mode_norm = aes_mode.upper()
    if aes_mode_norm not in _modes:
        raise NotImplementedError

    return _modes[aes_mode_norm](input_data)
