# Blueprints con Swagger sin Marshmallow

Esta guía muestra cómo organizar los blueprints de Flask usando Swagger/OpenAPI, pero sin usar Marshmallow.

La idea es separar tres responsabilidades:

- `services.py`: lógica de negocio y acceso a la base de datos.
- `routes.py`: endpoints HTTP organizados en blueprints.
- `openapi.yaml`: documentación de la API para Swagger UI.

> Swagger documenta la API, pero sin Marshmallow no valida automáticamente los datos recibidos. La validación debe hacerse manualmente o mediante funciones auxiliares.

## 1. Dependencias

Para este enfoque se puede usar `flask-swagger-ui`:

```bash
.venv/bin/pip install flask-swagger-ui pyyaml
```

En `requirements.txt`:

```txt
flask-swagger-ui
pyyaml
```

`flask-smorest` y `marshmallow` ya no serían necesarios para este enfoque.

## 2. Estructura recomendada

```text
flask_crud/
├── main.py
├── routes.py
├── services.py
├── database.py
├── openapi.yaml
└── requirements.txt
```

## 3. Blueprint en `routes.py`

Se puede crear un blueprint para cada grupo de recursos. Por ejemplo, un blueprint para clientes:

```python
from flask import Blueprint, jsonify, request

from services import ClientService

clientes_bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")


def validar_cliente(datos, requiere_email=True):
    campos_requeridos = ["nombre", "ciudad"]
    if requiere_email:
        campos_requeridos.append("email")

    if not isinstance(datos, dict):
        return "El cuerpo debe ser un objeto JSON."

    faltantes = [campo for campo in campos_requeridos if not datos.get(campo)]
    if faltantes:
        return f"Faltan campos requeridos: {', '.join(faltantes)}."

    return None


@clientes_bp.get("")
def listar_clientes():
    return jsonify(ClientService.listar_clientes()), 200


@clientes_bp.post("")
def crear_cliente():
    datos = request.get_json(silent=True)
    error = validar_cliente(datos)
    if error:
        return jsonify({"error": error}), 400

    resultado = ClientService.crear_cliente(
        nombre=datos["nombre"],
        email=datos["email"],
        ciudad=datos["ciudad"],
        fecha_registro=datos.get("fecha_registro"),
    )
    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 201


@clientes_bp.put("/<int:id_cliente>")
def actualizar_cliente(id_cliente):
    datos = request.get_json(silent=True)
    error = validar_cliente(datos)
    if error:
        return jsonify({"error": error}), 400

    resultado = ClientService.actualizar_cliente(
        id_cliente=id_cliente,
        nombre=datos["nombre"],
        email=datos["email"],
        ciudad=datos["ciudad"],
    )
    if "error" in resultado:
        codigo = 404 if "No existe" in resultado["error"] else 400
        return jsonify(resultado), codigo

    return jsonify(resultado), 200


@clientes_bp.delete("/<int:id_cliente>")
def eliminar_cliente(id_cliente):
    resultado = ClientService.eliminar_cliente(id_cliente)
    if "error" in resultado:
        codigo = 404 if "No existe" in resultado["error"] else 400
        return jsonify(resultado), codigo

    return jsonify(resultado), 200
```

Los blueprints para productos, pedidos y detalles seguirían el mismo patrón:

```python
productos_bp = Blueprint("productos", __name__, url_prefix="/api/productos")
pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/api/pedidos")
detalles_bp = Blueprint("detalles", __name__, url_prefix="/api/detalles")
```

Después se registrarían en la aplicación principal.

## 4. Configuración de Swagger en `main.py`

```python
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from routes import clientes_bp, detalles_bp, pedidos_bp, productos_bp

app = Flask(__name__)

app.register_blueprint(clientes_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalles_bp)

SWAGGER_URL = "/swagger"
API_URL = "/static/openapi.yaml"

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Tienda CRUD API",
    },
)

app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)


if __name__ == "__main__":
    app.run(debug=True)
```

Con el servidor iniciado, Swagger UI estaría disponible en:

```text
http://127.0.0.1:5000/swagger/
```

## 5. Archivo `openapi.yaml`

Crear `static/openapi.yaml`:

```yaml
openapi: 3.0.3
info:
  title: Tienda CRUD API
  version: 1.0.0
  description: API CRUD para clientes, productos, pedidos y detalles

servers:
  - url: http://127.0.0.1:5000

tags:
  - name: Clientes
  - name: Productos
  - name: Pedidos
  - name: Detalles

paths:
  /api/clientes:
    get:
      tags: [Clientes]
      summary: Listar clientes
      responses:
        "200":
          description: Lista de clientes
          content:
            application/json:
              schema:
                type: object
                properties:
                  clientes:
                    type: array
                    items:
                      $ref: "#/components/schemas/Cliente"

    post:
      tags: [Clientes]
      summary: Crear cliente
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ClienteEntrada"
      responses:
        "201":
          description: Cliente creado
        "400":
          $ref: "#/components/responses/Error"

  /api/clientes/{id_cliente}:
    parameters:
      - $ref: "#/components/parameters/IdCliente"
    put:
      tags: [Clientes]
      summary: Actualizar cliente
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ClienteEntrada"
      responses:
        "200":
          description: Cliente actualizado
        "404":
          $ref: "#/components/responses/Error"

    delete:
      tags: [Clientes]
      summary: Eliminar cliente
      responses:
        "200":
          description: Cliente eliminado
        "404":
          $ref: "#/components/responses/Error"

components:
  parameters:
    IdCliente:
      name: id_cliente
      in: path
      required: true
      schema:
        type: integer
      description: Identificador del cliente

  schemas:
    ClienteEntrada:
      type: object
      required:
        - nombre
        - email
        - ciudad
      properties:
        nombre:
          type: string
          example: Carlos Perez
        email:
          type: string
          format: email
          example: carlos@example.com
        ciudad:
          type: string
          example: Bogota
        fecha_registro:
          type: string
          format: date-time
          nullable: true

    Cliente:
      allOf:
        - $ref: "#/components/schemas/ClienteEntrada"
        - type: object
          properties:
            id_cliente:
              type: integer
              example: 1

  responses:
    Error:
      description: Error de la API
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: No existe cliente con ese ID.
```

El archivo debe contener también las rutas de productos, pedidos y detalles cuando esos endpoints estén listos. Swagger permite copiar el mismo patrón de `paths`, `schemas` y `responses`.

## 6. Validación manual sin Marshmallow

La validación manual debería comprobar como mínimo:

```python
if not isinstance(datos.get("stock"), int):
    return jsonify({"error": "stock debe ser un entero."}), 400

if datos.get("stock", 0) < 0:
    return jsonify({"error": "stock no puede ser negativo."}), 400
```

También conviene validar:

- Que el cuerpo sea JSON.
- Que existan los campos obligatorios.
- Que los identificadores sean enteros positivos.
- Que los emails tengan un formato válido.
- Que los valores numéricos no sean negativos cuando corresponda.
- Que los estados de pedido pertenezcan a los valores permitidos.

## 7. Diferencia entre ambas opciones

### Con Marshmallow

- Valida y deserializa automáticamente.
- Swagger/OpenAPI puede generarse desde los esquemas.
- Hay menos código repetido en las rutas.

### Sin Marshmallow

- El archivo OpenAPI se escribe manualmente.
- La validación se implementa en las rutas o en funciones auxiliares.
- Se tiene más control directo, pero también más responsabilidad.

Para tu proyecto actual, la opción sin Marshmallow sería reemplazar `flask-smorest` por `flask-swagger-ui`, mantener los servicios sin cambios y mover la documentación a `static/openapi.yaml`.
