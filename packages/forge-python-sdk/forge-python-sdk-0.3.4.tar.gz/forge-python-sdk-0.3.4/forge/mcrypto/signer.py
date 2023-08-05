import ed25519
import secp256k1


class Signer:
    def __init__(self, name='ed25519'):
        self.signer_type = Ed25519Signer
        if name == 'secp256k1':
            self.signer_type = Secp256k1Signer

        self.keypair = self.signer_type.keypair
        self.sk_to_pk = self.signer_type.sk_to_pk
        self.sign = self.signer_type.sign
        self.verify = self.signer_type.verify


class Ed25519Signer:

    @staticmethod
    def keypair():
        sk, pk = ed25519.create_keypair()
        return sk, pk

    @staticmethod
    def sk_to_pk(sk):
        secret_key = ed25519.SigningKey(sk)
        public_key = secret_key.get_verifying_key()
        return public_key

    @staticmethod
    def sign(data, sk):
        secret_key = ed25519.SigningKey(sk)
        signature = secret_key.sign(data)
        return signature

    @staticmethod
    def verify(data, signature, pk):
        public_key = ed25519.VerifyingKey(pk)
        result = public_key.verify(signature, data)
        return result


class Secp256k1Signer:

    @staticmethod
    def keypair():
        sk = secp256k1.PrivateKey()
        return sk, sk.pubkey

    @staticmethod
    def sk_to_pk(sk):
        sk = secp256k1.PrivateKey(sk)
        return sk.pubkey

    @staticmethod
    def sign(data, sk):
        sk = secp256k1.PrivateKey(sk)
        signature = sk.ecdsa_sign(data)
        return signature

    @staticmethod
    def verify(data, signature, pk):
        pk = secp256k1.PublicKey(pk)
        result = pk.ecdsa_verify(data, signature)
        return result
