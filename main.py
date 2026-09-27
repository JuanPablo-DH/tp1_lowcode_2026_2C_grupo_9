from src.models.producto import Producto
from src.models.inventario import Inventario
from src.models.informe import Informe
from src.models.transaccion import Transaccion
from src.services.archivador import Archivador
from src.services.graficador import Graficador

# Ruta hacia el archivo de persistencia JSON
RUTA_PRODUCTOS = "data/productos.json"
RUTA_TRANSACCIONES = "data/transacciones.json"

def pedir_y_asignar(
    objeto, 
    atributo: str,
    prompt: str,
    tipo_dato=str, 
    opcional: bool = False,
    es_moneda: bool = False
):
    """
    Solicita un dato al usuario y lo asigna directamente al @setter del objeto.
    Si opcional=True y se presiona Enter, conserva el valor previo.
    Si es_moneda=True, formatea el valor sugerido como monto (AR$ 1,234.50).
    """
    while True:
        try:
            valor_actual = getattr(objeto, atributo)

            # Formateo visual condicionado explícitamente por es_moneda
            if es_moneda and isinstance(valor_actual, (int, float)):
                fmt_valor = f"AR$ {valor_actual:,.2f}"
            else:
                fmt_valor = valor_actual

            prompt_final = f"{prompt} [{fmt_valor}]: " if opcional else f"{prompt}: "
            entrada = input(prompt_final).strip()

            # Si es opcional y presiona Enter, conserva el valor actual
            if opcional and not entrada:
                break

            # Limpieza de caracteres monetarios por si el usuario ingresa '$' o comas
            if es_moneda or tipo_dato == float:
                entrada = entrada.replace("AR$", "").replace(",", "").strip()

            valor_convertido = tipo_dato(entrada)
            # Ejecuta el @setter correspondiente en la clase Producto
            setattr(objeto, atributo, valor_convertido)
            break
        except ValueError as e:
            if "invalid literal" in str(e) or "could not convert" in str(e):
                print("❌ Debe ingresar un valor numérico válido.")
            else:
                print(f"❌ {e}")



def mostrar_menu():
    """Muestra el menú principal con la interfaz categorizada."""
    print("\n" + "=" * 55)
    print("            SISTEMA DE GESTIÓN DE INVENTARIO")
    print("=" * 55)
    print(" 1. Inventario")
    print("    1.1 Ver catálogo completo")
    print("    1.2 Registrar nuevo producto")
    print("    1.3 Modificar producto")
    print("    1.4 Eliminar producto")
    print("    1.5 Buscar productos (por categoría o proveedor)")
    print("    1.6 Reabastecer producto")
    print(" 2. Alertas")
    print("    2.1 Ver alertas de stock crítico")
    print("    2.2 Ver costo de reposición")
    print(" 3. Informes")
    print("    3.1 Ver reporte financiero")
    print("    3.2 Ver reporte transaccional")
    print("    3.3 Ver valuación en dólares (U$D)")
    print("    3.4 Exportar gráficos de análisis (.png)")
    print(" 4. Simular ventas")
    print(" 5. Guardar y salir")
    print("=" * 55)

def main():
    # -------------------------------------------------------------
    # 1. CARGA INICIAL DE DATOS
    # -------------------------------------------------------------
    print("📦 Cargando base de datos...")

    # Cargar Productos de forma independiente
    try:
        productos = Inventario.cargar_productos(RUTA_PRODUCTOS)
        print(f"✅ Productos cargados: {len(productos)} registro(s).")
    except FileNotFoundError:
        print(f"⚠️ No se encontró '{RUTA_PRODUCTOS}'. Se iniciará catálogo vacío.")
        productos = []
    except Exception as e:
        print(f"❌ Error al cargar productos ({e}). Se iniciará catálogo vacío.")
        productos = []

    # Cargar Transacciones de forma independiente
    try:
        transacciones = Inventario.cargar_transacciones(RUTA_TRANSACCIONES)
        print(f"✅ Transacciones cargadas: {len(transacciones)} registro(s).")
    except FileNotFoundError:
        print(f"ℹ️ No se encontró '{RUTA_TRANSACCIONES}'. Se iniciará historial nuevo.")
        transacciones = []
    except Exception as e:
        print(f"❌ Error al cargar transacciones ({e}). Se iniciará historial nuevo.")
        transacciones = []

    # Instanciamos el inventario con ambas listas resueltas de forma independiente
    inventario = Inventario(productos, transacciones)
    informe = Informe(inventario)

    # -------------------------------------------------------------
    # 2. BUCLE PRINCIPAL DE LA INTERFAZ
    # -------------------------------------------------------------
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        # --- OPCIÓN 1.1: Ver catálogo completo ---
        if opcion == "1.1":
            print("\n--- 📋 CATÁLOGO COMPLETO ---")
            print(informe.generar_reporte_general())

        # --- OPCIÓN 1.2: Registrar nuevo producto ---
        elif opcion == "1.2":
            print("\n--- ➕ REGISTRAR NUEVO PRODUCTO ---")
            while True:
                nuevo_prod = Producto()
                pedir_y_asignar(nuevo_prod, "id_producto", "ID del producto", int)

                if inventario.obtener_producto(nuevo_prod.id_producto) is not None:
                    print(f"❌ Ya existe un producto registrado con el ID {nuevo_prod.id_producto}.")
                    continue

                pedir_y_asignar(nuevo_prod, "nombre", "Nombre del producto", str)
                pedir_y_asignar(nuevo_prod, "categoria", "Categoría", str)
                pedir_y_asignar(nuevo_prod, "stock_actual", "Stock actual", int)
                pedir_y_asignar(nuevo_prod, "stock_minimo", "Stock mínimo", int)
                pedir_y_asignar(nuevo_prod, "precio_costo", "Precio de costo (AR$)", float, es_moneda=True)
                pedir_y_asignar(nuevo_prod, "precio_venta", "Precio de venta (AR$)", float, es_moneda=True)
                pedir_y_asignar(nuevo_prod, "proveedor", "Proveedor", str)

                inventario.agregar_producto(nuevo_prod)
                print(f"\n✅ Producto '{nuevo_prod.nombre}' registrado exitosamente.")
                break

        # --- OPCIÓN 1.3: Modificar producto ---
        elif opcion == "1.3":
            print("\n--- ✏️ MODIFICAR PRODUCTO ---")
            while True:
                aux = Producto()
                pedir_y_asignar(aux, "id_producto", "Ingrese el ID del producto a modificar", int)

                prod_actual = inventario.obtener_producto(aux.id_producto)
                if prod_actual is None:
                    print(f"❌ No existe un producto con el ID {aux.id_producto}.")
                    continue

                print(f"\nProducto seleccionado: {prod_actual}")
                print("Ingrese los nuevos datos (presione Enter para conservar el valor actual):")

                pedir_y_asignar(prod_actual, "nombre", "Nuevo nombre", str, opcional=True)
                pedir_y_asignar(prod_actual, "categoria", "Nueva categoría", str, opcional=True)
                pedir_y_asignar(prod_actual, "stock_actual", "Nuevo stock actual", int, opcional=True)
                pedir_y_asignar(prod_actual, "stock_minimo", "Nuevo stock mínimo", int, opcional=True)
                pedir_y_asignar(prod_actual, "precio_costo", "Nuevo precio costo (AR$)", float, opcional=True, es_moneda=True)
                pedir_y_asignar(prod_actual, "precio_venta", "Nuevo precio venta (AR$)", float, opcional=True, es_moneda=True)
                pedir_y_asignar(prod_actual, "proveedor", "Nuevo proveedor", str, opcional=True)

                inventario.modificar_producto(prod_actual)
                print("\n✅ Producto actualizado correctamente.")
                break

        # --- OPCIÓN 1.4: Eliminar producto ---
        elif opcion == "1.4":
            print("\n--- 🗑️ ELIMINAR PRODUCTO ---")
            while True:
                aux = Producto()
                pedir_y_asignar(aux, "id_producto", "Ingrese el ID del producto a eliminar", int)

                prod_actual = inventario.obtener_producto(aux.id_producto)
                if prod_actual is None:
                    print(f"❌ No existe un producto con el ID {aux.id_producto}.")
                    continue

                try:
                    inventario.eliminar_producto(prod_actual)
                    print(f"✅ Producto '{prod_actual.nombre}' (ID {prod_actual.id_producto}) eliminado exitosamente.")
                except ValueError as e:
                    print(f"❌ {e}")
                break

        # --- OPCIÓN 1.5: Buscar productos ---
        elif opcion == "1.5":
            print("\n--- 🔍 BUSCAR PRODUCTOS ---")
            print("Seleccione el campo de búsqueda:")
            print("1. Categoría")
            print("2. Proveedor")
            
            sub_opcion = input("Opción (1-2): ").strip()

            while True:
                if sub_opcion == "1":
                    criterio = "categoria"
                    break
                elif sub_opcion == "2":
                    criterio = "proveedor"
                    break
                else:
                    criterio = None
                    print("❌ Opción no válida. Debe seleccionar 1 o 2.")

            if criterio:
                valor = input(f"Ingrese el valor a buscar en {criterio}: ").strip()
                if valor:
                    # Informe consulta al inventario y devuelve la tabla formateada
                    print(informe.generar_reporte_busqueda(criterio, valor))
                else:
                    print("⚠️ Debe ingresar un término para buscar.")

        # --- OPCIÓN 1.6: Reabastecer producto ---
        elif opcion == "1.6":
            print("\n--- 📦 REABASTECER PRODUCTO (REPOSICIÓN) ---")
            aux = Producto()

            # 1. Bucle exclusivo para validar e ingresar un ID existente
            while True:
                pedir_y_asignar(aux, "id_producto", "ID del producto a reabastecer", int)
                prod_actual = inventario.obtener_producto(aux.id_producto)

                if prod_actual is None:
                    print(f"❌ No existe un producto registrado con el ID {aux.id_producto}.")
                    continue
                break  # ID correcto, salimos del primer bucle

            # Mostramos la información del producto seleccionado
            print(f"\nProducto seleccionado: {prod_actual.nombre}")
            print(f"Stock actual: {prod_actual.stock_actual} u. | Stock mínimo: {prod_actual.stock_minimo} u.")

            # 2. Bucle exclusivo para validar e ingresar la cantidad a reabastecer
            while True:
                pedir_y_asignar(aux, "stock_actual", "Cantidad de unidades a incorporar", int)
                cantidad = aux.stock_actual

                if cantidad <= 0:
                    print("❌ La cantidad a incorporar debe ser mayor a 0.")
                    continue

                break  # Cantidad válida, salimos del segundo bucle

            # 3. Ejecución de la lógica de negocio
            try:
                inventario.reabastecer_producto(prod_actual.id_producto, cantidad)
                print(f"\n✅ ¡Stock reabastecido con éxito!")
                print(f"   Nuevo stock de '{prod_actual.nombre}': {prod_actual.stock_actual} unidades.")
            except Exception as e:
                print(f"❌ Error al reabastecer el producto: {e}")

        # --- OPCIÓN 2.1: Ver alertas de stock crítico ---
        elif opcion == "2.1":
            print("\n--- ⚠️ ALERTAS DE STOCK CRÍTICO ---")
            print(informe.generar_reporte_alertas())

        # --- OPCIÓN 2.2: Ver costo de reposición ---
        elif opcion == "2.2":
            print("\n--- 💰 COSTO TOTAL DE REPOSICIÓN ---")
            print(informe.generar_reporte_costo_reposicion())

        # --- OPCIÓN 3.1: Ver reporte financiero ---
        elif opcion == "3.1":
            print("\n--- 📊 REPORTE FINANCIERO ---")
            print(informe.generar_reporte_financiero())

        # --- OPCIÓN 3.2: Ver reporte transaccional ---
        elif opcion == "3.2":
            print("\n--- 📊 REPORTE TRANSACCIONAL ---")
            print(informe.generar_reporte_transacciones())

        # --- OPCIÓN 3.3: Ver valuacion en dolares (U$D) ---
        elif opcion == "3.3":
            print("\n--- 💵 VALUACIÓN EN DÓLARES (DolarApi) ---")
            print("Seleccione el tipo de cotización:")
            print("1. Dólar Oficial")
            print("2. Dólar Blue")
            
            sub_opcion = input("Opción (1-2): ").strip()

            while True:
                if sub_opcion == "1":
                    tipo = "oficial"
                    break
                elif sub_opcion == "2":
                    tipo = "blue"
                    break
                else:
                    tipo = None
                    print("❌ Opción no válida. Debe seleccionar 1 o 2.")
            
            print(f"\n📡 Consultando DolarApi ({tipo})...")
            print(informe.generar_reporte_conversion_dolar(tipo))

        # --- OPCIÓN 3.4: Exportar gráficos .png ---
        elif opcion == "3.4":
            print("\n--- 📊 GENERANDO GRÁFICOS ANALÍTICOS (.PNG) ---")
            try:
                resultados = Graficador.generar_graficos_png(
                    inventario.lista_productos, 
                    inventario.lista_transacciones
                )
                for res in resultados:
                    print(res)
            except Exception as e:
                print(f"❌ Error al generar los gráficos: {e}")

        # --- OPCIÓN 4: Simular ventas ---
        elif opcion == "4":
            print("\n--- 🎲 SIMULACIÓN DE VENTA ---")
            tx = inventario.simular_ventas()
            if tx:
                print(f"✅ Venta realizada con éxito:")
                print(f"   • Producto: {tx.nombre_producto}")
                print(f"   • Cantidad vendida: {tx.cantidad} unidad(es)")
                print(f"   • Monto total: ${tx.monto_total:,.2f}")
            else:
                print("❌ No se pudo realizar la venta. No hay productos con stock disponible.")

        # --- OPCIÓN 5: Guardar y salir ---
        elif opcion == "5":
            print("\n💾 Guardando cambios en los archivos JSON...")
            try:
                cant_prod, cant_tx = inventario.guardar_datos(
                    RUTA_PRODUCTOS, 
                    RUTA_TRANSACCIONES
                )

                print(f"✅ Se guardaron {cant_prod} producto(s) en '{RUTA_PRODUCTOS}'.")
                print(f"✅ Se guardaron {cant_tx} transacción(es) en '{RUTA_TRANSACCIONES}'.")
                print("\n👋 ¡Gracias por utilizar el sistema! Hasta luego.\n")
            except Exception as e:
                print(f"❌ Error al guardar los datos: {e}")
            break

        else:
            print("❌ Opción no válida. Por favor, ingrese una opción válida (ej: 1.1, 1.2, 2.1, 3.1, 4, 5).")

if __name__ == "__main__":
    main()