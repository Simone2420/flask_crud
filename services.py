from datetime import date, datetime
from decimal import Decimal

from database import (
    clientes,
    delete,
    detalles_pedido,
    engine,
    insert,
    pedidos,
    productos,
    select,
    update,
)


def _serializar_fila(fila):
    datos = dict(fila)
    for campo, valor in datos.items():
        if isinstance(valor, (datetime, date)):
            datos[campo] = valor.isoformat()
        elif isinstance(valor, Decimal):
            datos[campo] = float(valor)
    return datos


def _listar(tabla):
    clave = next(iter(tabla.primary_key.columns))
    try:
        with engine.connect() as conexion:
                filas = conexion.execute(select(tabla).order_by(clave)).mappings().all()
        return [_serializar_fila(fila) for fila in filas]
    except Exception as e:
        return {"error": str(e)}


def _eliminar(tabla, nombre, clave_nombre, clave_valor):
    consulta_select = select(tabla).where(tabla.c[clave_nombre] == clave_valor)
    consulta_delete = delete(tabla).where(tabla.c[clave_nombre] == clave_valor)
    try:
        with engine.begin() as conexion:
            fila = conexion.execute(consulta_select).mappings().fetchone()
            if fila is None:
                return {"error": f"No existe {nombre} con ese ID."}
            conexion.execute(consulta_delete)
        return {
            "message": f"{nombre.capitalize()} eliminado correctamente.",
            f"{nombre}_eliminado": _serializar_fila(fila),
        }
    except Exception as e:
        return {"error": str(e)}


def _actualizar(tabla, nombre, clave_nombre, clave_valor, valores):
    consulta = (
        update(tabla)
        .where(tabla.c[clave_nombre] == clave_valor)
        .values(**valores)
    )
    try:
        with engine.begin() as conexion:
            resultado = conexion.execute(consulta)
        if resultado.rowcount == 0:
            return {"error": f"No existe {nombre} con ese ID."}
        return {"message": f"{nombre.capitalize()} actualizado correctamente."}
    except Exception as e:
        return {"error": str(e)}


class ProductoService:
    @staticmethod
    def listar_productos():
        return {"productos": _listar(productos)}

    @staticmethod
    def crear_producto(nombre_producto: str, categoria: str, precio: str, stock: int):
        consulta = insert(productos).values(
            nombre_producto=nombre_producto,
            categoria=categoria,
            precio=precio,
            stock=stock,
        )
        try:
            with engine.begin() as conexion:
                resultado = conexion.execute(consulta)
            return {
                "message": "Producto creado correctamente.",
                "id_producto": resultado.inserted_primary_key[0],
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def actualizar_producto(
        id_producto: int,
        nombre_producto: str,
        categoria: str,
        precio: str,
        stock: int,
    ):
        return _actualizar(
            productos,
            "producto",
            "id_producto",
            id_producto,
            {
                "nombre_producto": nombre_producto,
                "categoria": categoria,
                "precio": precio,
                "stock": stock,
            },
        )

    @staticmethod
    def eliminar_producto(id_producto: int):
        return _eliminar(productos, "producto", "id_producto", id_producto)


class PedidoService:
    @staticmethod
    def listar_pedidos():
        return {"pedidos": _listar(pedidos)}

    @staticmethod
    def crear_pedido(
        id_cliente: int,
        total: float,
        estado: str,
        fecha_pedido=None,
    ):
        valores = {"id_cliente": id_cliente, "total": total, "estado": estado}
        if fecha_pedido is not None:
            valores["fecha_pedido"] = fecha_pedido
        consulta = insert(pedidos).values(**valores)
        try:
            with engine.begin() as conexion:
                resultado = conexion.execute(consulta)
            return {
                "message": "Pedido creado correctamente.",
                "id_pedido": resultado.inserted_primary_key[0],
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def actualizar_pedido(id_pedido: int, id_cliente: int, total: float, estado: str):
        return _actualizar(
            pedidos,
            "pedido",
            "id_pedido",
            id_pedido,
            {"id_cliente": id_cliente, "total": total, "estado": estado},
        )

    @staticmethod
    def eliminar_pedido(id_pedido: int):
        return _eliminar(pedidos, "pedido", "id_pedido", id_pedido)


class DetallePedidoService:
    @staticmethod
    def listar_detalles():
        return {"detalles": _listar(detalles_pedido)}

    @staticmethod
    def crear_detalle(
        id_pedido: int,
        id_producto: int,
        cantidad: int,
        precio_unitario: float,
    ):
        consulta = insert(detalles_pedido).values(
            id_pedido=id_pedido,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )
        try:
            with engine.begin() as conexion:
                resultado = conexion.execute(consulta)
            return {
                "message": "Detalle creado correctamente.",
                "id_detalle": resultado.inserted_primary_key[0],
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def actualizar_detalle(
        id_detalle: int,
        id_pedido: int,
        id_producto: int,
        cantidad: int,
        precio_unitario: float,
    ):
        return _actualizar(
            detalles_pedido,
            "detalle",
            "id_detalle",
            id_detalle,
            {
                "id_pedido": id_pedido,
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
            },
        )

    @staticmethod
    def eliminar_detalle(id_detalle: int):
        return _eliminar(detalles_pedido, "detalle", "id_detalle", id_detalle)


class ClientService:
    @staticmethod
    def listar_clientes():
        resultado = _listar(clientes)
        if isinstance(resultado, dict) and "error" in resultado:
            return resultado
        return {"clientes": resultado}

    @staticmethod
    def crear_cliente(
        nombre: str,
        email: str,
        ciudad: str,
        fecha_registro=None,
    ):
        valores = {
            "nombre": nombre,
            "email": email,
            "ciudad": ciudad,
        }
        if fecha_registro is not None:
            valores["fecha_registro"] = fecha_registro

        consulta = insert(clientes).values(**valores)
        try:
            with engine.begin() as conexion:
                resultado = conexion.execute(consulta)
            return {
                "message": "Cliente creado correctamente.",
                "cliente": {
                    "id_cliente": resultado.inserted_primary_key[0],
                    "nombre": nombre,
                    "email": email,
                    "ciudad": ciudad,
                    "fecha_registro": fecha_registro,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def actualizar_cliente(
        id_cliente: int,
        nombre: str,
        ciudad: str,
        email: str = None,
    ):
        valores = {"nombre": nombre, "ciudad": ciudad}
        if email is not None:
            valores["email"] = email

        return _actualizar(
            clientes,
            "cliente",
            "id_cliente",
            id_cliente,
            valores,
        )

    @staticmethod
    def eliminar_cliente(id_cliente: int):
        return _eliminar(clientes, "cliente", "id_cliente", id_cliente)