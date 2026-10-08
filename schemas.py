from marshmallow import Schema, fields


class ClienteSchema(Schema):
	id_cliente = fields.Integer(dump_only=True)
	nombre = fields.String(required=True)
	email = fields.Email(required=True)
	ciudad = fields.String(required=True)
	fecha_registro = fields.DateTime(allow_none=True)


class ClienteCreateSchema(ClienteSchema):
	pass


class ClienteUpdateSchema(Schema):
	nombre = fields.String(required=True)
	email = fields.Email(required=True)
	ciudad = fields.String(required=True)


class ProductoSchema(Schema):
	id_producto = fields.Integer(dump_only=True)
	nombre_producto = fields.String(required=True)
	categoria = fields.String(required=True)
	precio = fields.String(required=True)
	stock = fields.Integer(required=True)


class PedidoSchema(Schema):
	id_pedido = fields.Integer(dump_only=True)
	id_cliente = fields.Integer(required=True)
	fecha_pedido = fields.DateTime(allow_none=True)
	total = fields.Float(required=True)
	estado = fields.String(required=True)


class PedidoCreateSchema(PedidoSchema):
	pass


class PedidoUpdateSchema(Schema):
	id_cliente = fields.Integer(required=True)
	total = fields.Float(required=True)
	estado = fields.String(required=True)


class DetallePedidoSchema(Schema):
	id_detalle = fields.Integer(dump_only=True)
	id_pedido = fields.Integer(required=True)
	id_producto = fields.Integer(required=True)
	cantidad = fields.Integer(required=True)
	precio_unitario = fields.Float(required=True)

