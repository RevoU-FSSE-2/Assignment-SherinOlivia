from injector import Module, singleton, Binder
from core.auth.ports import IHashingAccessor
from infrastructure.auth.adapters import HashingAccessor

class HashingModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(IHashingAccessor, to=HashingAccessor, scope=singleton)