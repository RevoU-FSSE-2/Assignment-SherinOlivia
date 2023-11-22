from injector import Injector
from infrastructure.user.modules import UserModule


injector = Injector([
    UserModule
])