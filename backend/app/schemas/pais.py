from pydantic import BaseModel, ConfigDict, field_validator


class PaisBase(BaseModel):
    nombre: str
    codigo_iso: str
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def nombre_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("nombre no puede estar vacío")
        if len(v) > 100:
            raise ValueError("nombre no puede superar 100 caracteres")
        return v

    @field_validator("codigo_iso")
    @classmethod
    def codigo_iso_format(cls, v: str) -> str:
        v = v.strip().upper()
        if not (2 <= len(v) <= 3):
            raise ValueError("codigo_iso debe tener 2 o 3 caracteres (ISO 3166-1)")
        if not v.isalpha():
            raise ValueError("codigo_iso solo puede contener letras")
        return v


class PaisCreate(PaisBase):
    pass


class PaisUpdate(BaseModel):
    nombre: str | None = None
    codigo_iso: str | None = None
    activo: bool | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("nombre no puede estar vacío")
        if len(v) > 100:
            raise ValueError("nombre no puede superar 100 caracteres")
        return v

    @field_validator("codigo_iso")
    @classmethod
    def codigo_iso_format(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().upper()
        if not (2 <= len(v) <= 3):
            raise ValueError("codigo_iso debe tener 2 o 3 caracteres (ISO 3166-1)")
        if not v.isalpha():
            raise ValueError("codigo_iso solo puede contener letras")
        return v


class PaisRead(PaisBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
