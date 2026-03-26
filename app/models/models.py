from typing import Optional
import datetime
from sqlalchemy import ForeignKey, String, TIMESTAMP, func, DateTime, Integer, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.db.conexion import engine


class Base(DeclarativeBase):
    pass


# ================= USER =================
class User(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    clave: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(
        Enum("activo", "inactivo", name="estado_usuario"),
        nullable=False,
        default="activo",
    )
    ultimo_ingreso: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, default=func.now()
    )

    perfil = relationship("UserProfile", back_populates="usuario")

    def __repr__(self):
        return f"User(id={self.id}, nombre={self.nombre}, email={self.email})"


# ================= PROFILE =================
class Profile(Base):
    __tablename__ = "perfiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    usuario = relationship("UserProfile", back_populates="perfil")


# =============== TABLA PUENTE ===============
class UserProfile(Base):
    __tablename__ = "perfil_usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    id_perfil: Mapped[int] = mapped_column(ForeignKey("perfiles.id"))

    usuario = relationship("User", back_populates="perfil")
    perfil = relationship("Profile", back_populates="usuario")


# ================= AUTO =====================
class Auto(Base):
    __tablename__ = "auto"

    id: Mapped[int] = mapped_column(primary_key=True)
    patente: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    fecha_creación: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    ticket = relationship("Ticket", back_populates="auto")


# ================= TICKET ===================
class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_auto: Mapped[int] = mapped_column(ForeignKey("auto.id"))

    fecha_ingreso: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    fecha_salida: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    estado: Mapped[str] = mapped_column(
        Enum("abierto", "pagado", "cerrado", name="estado_ticket"),
        nullable=False,
        default="abierto",
    )

    fecha_creacion: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )

    boleta = relationship("Boleta", back_populates="ticket", uselist=False)
    auto = relationship("Auto", back_populates="ticket")


# ================= TARIFA ===================


class Tarifa(Base):
    __tablename__ = "tarifa"

    id: Mapped[int] = mapped_column(primary_key=True)
    precio_por_minuto: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_inicio: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    boleta = relationship("Boleta", back_populates="tarifa")


# ================= BOLETA ===================
class Boleta(Base):
    __tablename__ = "boleta"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_ticket: Mapped[int] = mapped_column(ForeignKey("ticket.id"), unique=True)
    id_tarifa: Mapped[int] = mapped_column(ForeignKey("tarifa.id"))

    monto_total: Mapped[int] = mapped_column(Integer, nullable=False)
    metodo_pago: Mapped[str] = mapped_column(
        Enum("efectivo", "debito", "credito", "transferencia", name="metodo_pago"),
        nullable=False,
        default="efectivo",
    )
    fecha_pago: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    ticket = relationship("Ticket", back_populates="boleta")
    tarifa = relationship("Tarifa", back_populates="boleta")


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
