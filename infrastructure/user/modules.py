from injector import Module, singleton, Binder
from core.auth.ports import IUserAccessor
from infrastructure.user.adapters import UserAccessor

class UserModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(IUserAccessor, to=UserAccessor, scope=singleton)