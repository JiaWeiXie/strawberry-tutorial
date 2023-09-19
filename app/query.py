import typing
import strawberry

from app import types, services


@strawberry.type
class Query:
    users: typing.List[types.User] = strawberry.field(
        resolver=services.user_service.all_users,
    )
    user: typing.Optional[types.User] = strawberry.field(
        resolver=services.user_service.user,
    )
