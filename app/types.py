import datetime
import enum
import typing
import strawberry

from strawberry import scalars


@strawberry.enum
class UserRole(enum.Enum):
    NORMAL = strawberry.enum_value(
        "normal",
        description="Normal user",
    )
    STAFF = "staff"
    MANAGER = "manager"
    ADMIN = "admin"


@strawberry.interface
class UserProfile:
    phone: str
    birthdate: datetime.date
    address: typing.Optional[str]


@strawberry.type
class NormalUserDetail(UserProfile):
    pass


@strawberry.type
class StaffUserDetail(UserProfile):
    department: str


@strawberry.type
class ManagerUserDetail(StaffUserDetail):
    subordinates: typing.List["User"]


@strawberry.type
class AdminUserDetail:
    system_permissions: typing.List[str]


@strawberry.type
class User:
    id: strawberry.ID
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    avatar: typing.Optional[scalars.Base64] = strawberry.field(
        description="Base64 encoded avatar",
        deprecation_reason="Removed this field.",
        default=None,
    )
    last_login: typing.Optional[datetime.datetime]
    is_active: bool = strawberry.field(
        default=True,
        description="Is the user active?",
    )
    role: UserRole
    detail: typing.Annotated[
        typing.Union[
            NormalUserDetail,
            StaffUserDetail,
            ManagerUserDetail,
            AdminUserDetail,
        ],
        strawberry.union("UserDetail"),
    ]

    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@strawberry.input
class NormalUserInput:
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    phone: str
    birthdate: datetime.date
    address: typing.Optional[str] = None