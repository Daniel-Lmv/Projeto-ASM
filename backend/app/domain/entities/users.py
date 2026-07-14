import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass
class User:
    name: str
    email: str
    password_hash: str
    is_active: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=lambda: uuid.uuid4())

    def __post_init__(self):
        self._validate_name()
        self._validate_email()
        self._validate_password()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

    def rename_name(self, name: str) -> None:
        self.name = name
        self._validate_name()
        self._touch()

    def change_email(self, nv_email: str) -> None:
        self.email = nv_email
        self._validate_email()
        self._touch()

    def change_password_hash(self, nv_senha: str) -> None:
        self.password_hash = nv_senha
        self._validate_password()
        self._touch()

    def activate_user(self) -> None:
        self.is_active = True
        self._touch()

    def deactivate_user(self) -> None:
        self.is_active = False
        self._touch()

    def _validate_name(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("O nome não pode ser vazio")
        if len(self.name) < 2:
            raise ValueError("O nome deve conter no mínimo 2 letras!")
        self.name = self.name.title()

    def _validate_email(self) -> None:
        self.email = self.email.strip().lower()
        if not self.email:
            raise ValueError("O email não pode ser vazio")
        if "@" not in self.email:
            raise ValueError("O email é invalido, necessita de @")
        if "." not in self.email:
            raise ValueError("O email é invalido, necessita de .")

    def _validate_password(self) -> None:
        self.password_hash = self.password_hash.strip()
        if not self.password_hash:
            raise ValueError("A senha não pode ser vazia")
        if len(self.password_hash) < 6:
            raise ValueError("A senha deve conter no mínimo 5 caracteres")
