import typing
import strawberry

from app import types, services


user_service = services.UserService()


@strawberry.type
class Query:
    users: typing.List[types.User] = strawberry.field(resolver=user_service.all_users)
    user: typing.Optional[types.User] = strawberry.field(resolver=user_service.user)
