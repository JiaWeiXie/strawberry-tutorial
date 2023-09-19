import typing
import strawberry

from strawberry.field_extensions import InputMutationExtension

from app import services, types


@strawberry.type
class Mutation:
    update_user: typing.Optional[types.User] = strawberry.mutation(
        resolver=services.user_service.update_user,
        description="Update user",
        extensions=[InputMutationExtension()],
    )   