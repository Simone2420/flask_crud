from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import *

from services import (
	ClientService,
	DetallePedidoService,
	PedidoService,
	ProductoService,
)


blp = Blueprint("api", "api", url_prefix="/api", description="API de la tienda")


def _respuesta(resultado, codigo_exito=200):
	if isinstance(resultado, dict) and "error" in resultado:
		codigo = 404 if resultado["error"].startswith("No existe") else 400
		abort(codigo, message=resultado["error"])
	return resultado, codigo_exito


@blp.route("/clientes")
class ClientesResource(MethodView):
	@blp.response(200)
	def get(self):
		return _respuesta(ClientService.listar_clientes())

	@blp.arguments(ClienteCreateSchema(only=("nombre", "email", "ciudad", "fecha_registro")))
	@blp.response(201)
	def post(self, datos):
		return _respuesta(ClientService.crear_cliente(**datos), 201)


@blp.route("/clientes/<int:id_cliente>")
class ClienteResource(MethodView):
	@blp.arguments(ClienteUpdateSchema)
	@blp.response(200)
	def put(self, datos, id_cliente):
		return _respuesta(ClientService.actualizar_cliente(id_cliente, **datos))

	@blp.response(200)
	def delete(self, id_cliente):
		return _respuesta(ClientService.eliminar_cliente(id_cliente))


@blp.route("/productos")
class ProductosResource(MethodView):
	@blp.response(200)
	def get(self):
		return _respuesta(ProductoService.listar_productos())

	@blp.arguments(ProductoSchema(only=("nombre_producto", "categoria", "precio", "stock")))
	@blp.response(201)
	def post(self, datos):
		return _respuesta(ProductoService.crear_producto(**datos), 201)


@blp.route("/productos/<int:id_producto>")
class ProductoResource(MethodView):
	@blp.arguments(ProductoSchema(only=("nombre_producto", "categoria", "precio", "stock")))
	@blp.response(200)
	def put(self, datos, id_producto):
		return _respuesta(ProductoService.actualizar_producto(id_producto, **datos))

	@blp.response(200)
	def delete(self, id_producto):
		return _respuesta(ProductoService.eliminar_producto(id_producto))


@blp.route("/pedidos")
class PedidosResource(MethodView):
	@blp.response(200)
	def get(self):
		return _respuesta(PedidoService.listar_pedidos())

	@blp.arguments(PedidoCreateSchema(only=("id_cliente", "total", "estado", "fecha_pedido")))
	@blp.response(201)
	def post(self, datos):
		return _respuesta(PedidoService.crear_pedido(**datos), 201)


@blp.route("/pedidos/<int:id_pedido>")
class PedidoResource(MethodView):
	@blp.arguments(PedidoUpdateSchema)
	@blp.response(200)
	def put(self, datos, id_pedido):
		return _respuesta(PedidoService.actualizar_pedido(id_pedido, **datos))

	@blp.response(200)
	def delete(self, id_pedido):
		return _respuesta(PedidoService.eliminar_pedido(id_pedido))


@blp.route("/detalles")
class DetallesResource(MethodView):
	@blp.response(200)
	def get(self):
		return _respuesta(DetallePedidoService.listar_detalles())

	@blp.arguments(DetallePedidoSchema(only=("id_pedido", "id_producto", "cantidad", "precio_unitario")))
	@blp.response(201)
	def post(self, datos):
		return _respuesta(DetallePedidoService.crear_detalle(**datos), 201)


@blp.route("/detalles/<int:id_detalle>")
class DetalleResource(MethodView):
	@blp.arguments(DetallePedidoSchema(only=("id_pedido", "id_producto", "cantidad", "precio_unitario")))
	@blp.response(200)
	def put(self, datos, id_detalle):
		return _respuesta(DetallePedidoService.actualizar_detalle(id_detalle, **datos))

	@blp.response(200)
	def delete(self, id_detalle):
		return _respuesta(DetallePedidoService.eliminar_detalle(id_detalle))
