from socket import socket, SOCK_DGRAM, AF_INET
from json import dumps
from enum import Enum
from inspect import getmembers, ismethod

class XSOMessageType(Enum):
    NOTIFICATION = 1
    MEDIA = 2

class XSOMessage(object):
    messageType: XSOMessageType = XSOMessageType.NOTIFICATION
    index: int = 0
    timeout: float = 4.0
    height: int = 150
    opacity: int = 1
    volume: float = 0.7
    audioPath: str = "default"
    useBase64Icon: bool = False
    icon: str = "default"
    sourceApp: str = "pyXSO"

    def __init__(self, title: str, content: str = ""):
        self.title = title
        self.content = content
    
    def _get_payload(self) -> bytes:
        payload_dict = { x[0]:x[1] for x in getmembers(self) if not x[0].startswith('__') and not ismethod(x[1])}
        payload_dict['messageType'] = self.messageType.value
        return payload_dict
    
    def _get_bytes(self) -> bytes:
        payload_dict = self._get_payload()
        payload_str = dumps(payload_dict)
        return payload_str.encode('utf8')

class XSOWarning(XSOMessage):
    audioPath: str = "warning"
    icon: str = "warning"

class XSOError(XSOMessage):
    audioPath:str = "error"
    icon:str = "error"

class XSOMessageSender(object):
    port = 42069
    def send(self, message: XSOMessage) -> None:
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.sendto(message._get_bytes(), ("localhost", self.port))