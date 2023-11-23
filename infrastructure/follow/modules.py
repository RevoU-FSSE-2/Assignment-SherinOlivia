from injector import Module, singleton, Binder
from core.follow.ports import IFollowAccessor
from infrastructure.follow.adapters import FollowAccessor

class FollowModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(IFollowAccessor, to=FollowAccessor, scope=singleton)