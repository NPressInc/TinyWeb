from nacl.signing import SignedMessage
import base64

class Signature(SignedMessage):

    def __init__(self, signed_message: SignedMessage):
        self.signed_message = signed_message
        self.serialized = self.serialize_to_string()

    def serialize_to_bytes(self):
        return base64.b64encode(self.signed_message.message + self.signed_message.signature)
    
    @staticmethod
    def deserialize_from_string(signedMessageb64String) -> [bytes, bytes]:
        signedMessageBytes = base64.b64decode(signedMessageb64String.encode())
        serialized_message = signedMessageBytes[:-64]
        signature = signedMessageBytes[-64:]
        return serialized_message, signature

    def serialize_to_string(self):
        return base64.b64encode(self.serialize_to_bytes()).decode()
        