from sqlalchemy import (
    create_engine,
    MetaData,
    select,
    insert,
    update,
    delete
)

from dotenv import load_dotenv
import os
load_dotenv()
# ============================================================
# CONEXIÓN
# ============================================================

engine = create_engine(
    os.getenv("DATABASE_URL")
)


# ============================================================
# CARGAR ESTRUCTURA DE LA BASE DE DATOS
# ============================================================

metadata = MetaData()

metadata.reflect(bind=engine)

clientes = metadata.tables["clientes"]
pedidos = metadata.tables["pedidos"]
detalles_pedido = metadata.tables["detalle_pedidos"]
productos = metadata.tables["productos"]