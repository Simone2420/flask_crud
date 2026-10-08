from sqlalchemy import (
    create_engine,
    MetaData,
    select,
    insert,
    update,
    delete
)

# ============================================================
# CONEXIÓN
# ============================================================

engine = create_engine(
    "mysql+pymysql://root:Blass1.2@localhost/tienda"
)


# ============================================================
# CARGAR ESTRUCTURA DE LA BASE DE DATOS
# ============================================================

metadata = MetaData()

metadata.reflect(bind=engine)

clientes = metadata.tables["clientes"]


# ============================================================
# READ - LISTAR CLIENTES
# ============================================================

def listar_clientes():

    consulta = (
        select(
            clientes.c.id_cliente,
            clientes.c.nombre,
            clientes.c.email,
            clientes.c.ciudad
        )
        .order_by(clientes.c.id_cliente)
    )

    try:

        with engine.connect() as conexion:

            resultado = conexion.execute(consulta)

            filas = resultado.fetchall()

        print("\n" + "=" * 90)
        print("LISTA DE CLIENTES")
        print("=" * 90)

        if len(filas) == 0:

            print("No hay clientes registrados.")

        else:

            print(
                f"{'ID':<5}"
                f"{'NOMBRE':<25}"
                f"{'EMAIL':<35}"
                f"{'CIUDAD':<15}"
            )

            print("-" * 90)

            for fila in filas:

                print(
                    f"{fila.id_cliente:<5}"
                    f"{str(fila.nombre):<25}"
                    f"{str(fila.email):<35}"
                    f"{str(fila.ciudad):<15}"
                )

        print("=" * 90)

    except Exception as e:

        print("\nError al listar los clientes:")
        print(e)


# ============================================================
# CREATE - CREAR CLIENTE
# ============================================================

def crear_cliente():

    print("\n" + "=" * 40)
    print("CREAR CLIENTE")
    print("=" * 40)

    nombre = input("Nombre: ")
    email = input("Email: ")
    ciudad = input("Ciudad: ")

    consulta = (
        insert(clientes)
        .values(
            nombre=nombre,
            email=email,
            ciudad=ciudad
        )
    )

    try:

        with engine.begin() as conexion:

            resultado = conexion.execute(consulta)

        print("\nCliente creado correctamente.")
        print("ID:", resultado.lastrowid)

    except Exception as e:

        print("\nError al crear el cliente:")
        print(e)


# ============================================================
# UPDATE - ACTUALIZAR CLIENTE
# ============================================================

def actualizar_cliente():

    print("\n" + "=" * 40)
    print("ACTUALIZAR CLIENTE")
    print("=" * 40)

    try:

        id_cliente = int(
            input("ID del cliente: ")
        )

    except ValueError:

        print("El ID debe ser un número.")

        return

    nombre = input("Nuevo nombre: ")
    ciudad = input("Nueva ciudad: ")

    consulta = (
        update(clientes)
        .where(
            clientes.c.id_cliente == id_cliente
        )
        .values(
            nombre=nombre,
            ciudad=ciudad
        )
    )

    try:

        with engine.begin() as conexion:

            resultado = conexion.execute(consulta)

        if resultado.rowcount == 0:

            print("\nNo existe un cliente con ese ID.")

        else:

            print("\nCliente actualizado correctamente.")
            for fila in resultado:
                print(f"ID: {fila.id_cliente}, Nombre: {fila.nombre}, Ciudad: {fila.ciudad}")

    except Exception as e:

        print("\nError al actualizar el cliente:")
        print(e)


# ============================================================
# DELETE - ELIMINAR CLIENTE
# ============================================================

def eliminar_cliente():

    print("\n" + "=" * 40)
    print("ELIMINAR CLIENTE")
    print("=" * 40)

    try:

        id_cliente = int(
            input("ID del cliente: ")
        )

    except ValueError:

        print("El ID debe ser un número.")

        return

    # Confirmación antes de eliminar
    confirmacion = input(
        f"¿Está seguro de eliminar el cliente {id_cliente}? (s/n): "
    )

    if confirmacion.lower() != "s":

        print("Operación cancelada.")

        return

    consulta = (
        delete(clientes)
        .where(
            clientes.c.id_cliente == id_cliente
        )
    )

    try:

        with engine.begin() as conexion:

            resultado = conexion.execute(consulta)

        if resultado.rowcount == 0:

            print("\nNo existe un cliente con ese ID.")

        else:

            print("\nCliente eliminado correctamente.")

    except Exception as e:

        print("\nError al eliminar el cliente:")
        print(e)


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

while True:

    print("\n")
    print("=" * 40)
    print("        CRUD DE CLIENTES")
    print("=" * 40)

    print("1. Listar clientes")
    print("2. Crear cliente")
    print("3. Actualizar cliente")
    print("4. Eliminar cliente")
    print("5. Salir")

    print("=" * 40)

    opcion = input("Seleccione una opción: ").strip()

    match opcion:
        case "1":
            listar_clientes()
        case "2":
            crear_cliente()
        case "3":
            actualizar_cliente()
        case "4":
            eliminar_cliente()
        case "5":
            print("\nPrograma finalizado.")
            break
        case _:
            print("\nOpción no válida.")