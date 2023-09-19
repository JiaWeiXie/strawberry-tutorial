# app/services.py
import itertools
import typing

from faker import Faker

from app import types


fake = Faker(["zh_TW", "en_US"])


def gen_user_info() -> (
    typing.Tuple[
        typing.Dict[str, typing.Any],
        typing.Dict[str, typing.Any],
    ]
):
    profile = fake.simple_profile()
    user_info = dict(
        id=fake.random_int(min=1),
        username=profile["username"],
        email=fake.ascii_safe_email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password=fake.lexify(text="??????????????????????????????"),
        last_login=fake.date_time_this_century() if fake.random_digit() > 1 else None,
        is_active=bool(fake.random_digit() > 1),
    )
    detail = dict(
        birthdate=profile["birthdate"],
        address=profile["address"],
        phone=fake.phone_number(),
    )
    return user_info, detail


def gen_normal_user() -> types.User:
    user_info, detail = gen_user_info()
    user_info["role"] = types.UserRole.NORMAL
    user_info["detail"] = types.NormalUserDetail(**detail)
    return types.User(**user_info)


def gen_staff_user(department: str) -> types.User:
    user_info, detail = gen_user_info()
    user_info["role"] = types.UserRole.STAFF
    detail["department"] = department
    user_info["detail"] = types.StaffUserDetail(**detail)
    return types.User(**user_info)


def gen_manager_user(
    department: str,
    subordinates: typing.List[types.User],
) -> types.User:
    user_info, detail = gen_user_info()
    user_info["role"] = types.UserRole.MANAGER
    detail["department"] = department
    detail["subordinates"] = subordinates
    user_info["detail"] = types.ManagerUserDetail(**detail)
    return types.User(**user_info)


def gen_admin_user() -> types.User:
    user_info, _ = gen_user_info()
    user_info["role"] = types.UserRole.ADMIN
    user_info["detail"] = types.AdminUserDetail(
        system_permissions=fake.random_choices(
            elements=(
                "read_users",
                "read_user",
                "write_user",
                "update_user",
                "delete_user",
            ),
        )
    )
    return types.User(**user_info)


class UserService:
    def __init__(self) -> None:
        self.normal_users = [gen_normal_user() for _ in range(20)]
        self.staff_users = []
        self.manager_users = []
        self.admin_users = [gen_admin_user() for _ in range(10)]
        self.departments = [
            "Human Resources",
            "IT",
            "Accounting",
            "Finance",
            "Marketing",
            "Research",
            "Development",
            "Production",
        ]
        self._gen_department_users()

    def _gen_department_users(self) -> None:
        for department in fake.random_choices(elements=self.departments):
            staffs = [gen_staff_user(department) for _ in range(fake.random_digit())]
            managers = [
                gen_manager_user(department, staffs)
                for _ in range(fake.random_int(min=0, max=5))
            ]
            self.staff_users.extend(staffs)
            self.manager_users.extend(managers)

    def all_users(
        self,
        role: typing.Optional[types.UserRole] = None,
        role_in: typing.Optional[typing.List[types.UserRole]] = None,
    ) -> typing.List[types.User]:
        role_map = {
            types.UserRole.NORMAL: self.normal_users,
            types.UserRole.STAFF: self.staff_users,
            types.UserRole.MANAGER: self.manager_users,
            types.UserRole.ADMIN: self.admin_users,
        }
        if role:
            return role_map[role]
        elif role_in:
            return list(itertools.chain.from_iterable(role_map[r] for r in role_in))
        return list(itertools.chain.from_iterable(role_map.values()))

    def user(self, id: int) -> typing.Optional[types.User]:
        for user in self.all_users():
            if user.id == id:
                return user
        return None
    
    def update_user(
        self,
        id: int,
        email: str,
        first_name: str,
        last_name: str,
    ) -> typing.Optional[types.User]:
        user = self.user(id)
        if user:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            # Save to database
        return user


user_service = UserService()