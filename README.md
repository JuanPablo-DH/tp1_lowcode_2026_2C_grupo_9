# Integrantes del Grupo 9  
*Camila Zarza*  
*Elmer Baltazar Llusco*  
*Federico Colombo*  
*Juan Pablo Dongo Huaman*  
*Tomás Ezequiel Nobile*  

# Docente  
*Dr. Esteban Calcagno*  

# Sistema de Gestión de Inventario y Control de Stock - LowCode TP1

## 📌 Descripción del Proyecto
Aplicación de consola (CLI) desarrollada en Python para la gestión integral de inventarios informáticos, seguimiento de stock crítico, registro de transacciones comerciales y análisis de datos financieros. El sistema incluye integración con la API pública de DolarApi.com para valuación en divisas y un módulo de análisis de datos mediante Jupyter Notebook (`analisis.ipynb`) con generación automatizada de gráficos en formato `.png` (Pandas y Matplotlib).

## 📁 Estructura del Proyecto
```text
.
├── data/
│   ├── productos.json                # Persistencia del catálogo de productos
│   ├── transacciones.json            # Historial auditable de transacciones
│   ├── grafico_stock_productos.png   # Gráfico generado de stock por producto
│   └── grafico_ventas_categoria.png  # Gráfico generado de ventas por categoría
│
├── src/
│   ├── models/
│   │   ├── informe.py                # Clase Informe (reportes formateados y conversión USD)
│   │   ├── inventario.py             # Clase Inventario (gestión de catálogo, CRUD y persistencia)
│   │   ├── producto.py               # Clase Producto (encapsulamiento, setters y validaciones)
│   │   └── transaccion.py            # Clase Transaccion (registro de operaciones)
│   │
│   └── services/
│       ├── archivador.py             # Servicio genérico de lectura/escritura JSON
│       ├── dolar_api.py              # Servicio de consumo de API externa (DolarApi.com)
│       └── graficador.py             # Servicio de generación de gráficos analíticos (.png)
│
├── .gitignore                        # Reglas de exclusión para Git (entorno virtual venv y temporales)
├── analisis.ipynb                    # Notebook de exploración visual con Pandas y Matplotlib
├── main.py                           # Punto de entrada principal y menú CLI categorizado
├── README.md                         # Documentación general y registro de prompts de IA
└── requirements.txt                  # Archivo de dependencias del proyecto
```

---

## 🚀 Requisitos e Instalación

### Requisitos Previos
* Python 3.10 o superior.

### Instalación
1. Clonar o descargar el repositorio del proyecto.
2. Crear y activar un entorno virtual (`venv`):
   * **En Linux / macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   * **En Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
3. Instalar las dependencias listadas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Instrucciones de Ejecución

### Ejecutar la Aplicación CLI
```bash
python main.py
```

---

## 🛠️ Funcionalidades Principales

1. **Gestión de Inventario (CRUD y Reabastecimiento)**:
   * **1.1 Ver catálogo completo**: Listado formateado en tablas con detalles de stock y precios.
   * **1.2 Registrar nuevo producto**: Alta de ítems con validación de tipos y montos no negativos.
   * **1.3 Modificar producto**: Edición interactiva de atributos existentes.
   * **1.4 Eliminar producto**: Baja por ID con verificación previa.
   * **1.5 Buscar productos**: Filtrado dinámico por categoría o proveedor.
   * **1.6 Reabastecer producto**: Incorporación de stock a un producto existente.
   * **1.7 Desabastecer producto**: Retiro de stock a un producto existente.
2. **Control de Stock y Alertas**:
   * **2.1 Ver alertas de stock crítico**: Identificación de productos cuyo stock actual está por debajo del mínimo.
   * **2.2 Ver costo de reposición**: Cálculo del presupuesto necesario para nivelar el stock al umbral recomendado.
3. **Informes Financieros y Transaccionales**:
   * **3.1 Ver reporte financiero**: Capital invertido, margen de ganancia proyectado y totales del catálogo.
   * **3.2 Ver reporte transaccional**: Historial auditado de movimientos (`ACTUALIZACION`, `VENTA`, `REABASTECER` y `DESABASTECER`).
   * **3.3 Ver valuación en dólares (U$D)**: Conversión financiera en tiempo real consumiendo DolarApi.com.
   * **3.4 Exportar gráficos de análisis (.png)**: Generación automática de imágenes estadísticas en la carpeta `data/`.
4. **Simular ventas**: Proceso interactivo de ventas con descuento de stock.
5. **Guardar y salir**: Almacenamiento persistente en `productos.json` y `transacciones.json`.

## 🤖 Registro Obligatorio de Uso de Inteligencia Artificial (Prompts)
En cumplimiento con la consigna del Trabajo Práctico 1, se documenta el uso de herramientas de Asistencia de IA durante el ciclo de desarrollo:

| # | Prompt / Solicitud enviada a la IA | Herramienta | Resultado Generado | Validación / Modificación Realizada por el Grupo |
|---|-----------------------------------|-------------|--------------------|--------------------------------------------------|
| 1 | "Generar dataset de prueba en formato JSON con productos de tecnología (procesadores, placas de video, RAM, discos) y transacciones variadas." | Gemini | Estructura JSON con campos e IDs coherentes. | Se verificaron los tipos de datos y se ajustaron los precios y nombres para reflejar el mercado informático local. |
| 2 | "Cómo realizar un gráfico de barras horizontales dobles en Pandas/Matplotlib mostrando Stock Actual vs Stock Mínimo con etiquetas numéricas al final de cada barra." | Gemini | Código con `df.plot.barh` y bucle `ax.bar_label(container)`. | Se refinó la estética ocultando los ejes Y/X innecesarios y configurando `matplotlib.use('Agg')` para el servicio CLI. |
| 3 | "Refactorizar la función de guardado en `main.py` para encapsularla dentro de un método en la clase `Inventario`." | Gemini | Método `inventario.guardar_datos(...)` retornando tupla de cantidades. | Se validó la encapsulación y la correcta delegación al servicio `Archivador`. |
| 4 | "Cómo manejar la respuesta de DolarApi.com ante caídas de red o timeouts usando `urllib.request`." | Gemini | Bloque `try/except` con `timeout=5` retornando `None` ante fallas. | Se testeó desconectando la red para asegurar que la aplicación continúe funcionando sin interrupciones. |
| 5 | "Cómo estructurar el método de reabastecimiento en dos bucles while para validar el ID existente y la cantidad ingresada sin reiniciar el pedido de ID." | Gemini | Estructura de dos bucles `while` secuenciales usando `pedir_y_asignar(...)`. | Se probó el flujo interactivo asegurando que no se pierda el ID ingresado si la cantidad ingresada es errónea. |
| 6 | "Cómo refactorizar los métodos de carga y guardado en `Inventario` aplicando el principio DRY mediante un método auxiliar genérico." | Gemini | Implementación de `_cargar_lista` y `_guardar_lista` recibiendo métodos de conversión (`from_dict` / `to_dict`). | Se validó el paso de funciones como parámetros de primera clase y se mantuvieron los bloques `try/except` independientes en `main.py` para aislar fallos de archivos. |
| 7 | "Explicación y funcionamiento de la función incorporada `getattr()` para el acceso dinámico a atributos de un objeto." | Gemini | Explicación del funcionamiento de `getattr(objeto, atributo, valor_defecto)`. | Se verificó su aplicación en `filtrar_por_criterio()` para evitar código repetitivo de tipo `if/elif` al buscar por categoría o proveedor. |
| 8 | "Cómo estructurar el método `desabastecer_producto` en `Inventario` para registrar retiros/mermas de stock validando la cantidad disponible." | Gemini | Implementación del método de ajuste con registro automático de transacción tipo `"DESABASTECER"`. | Se validó que la cantidad a retirar no supere el stock actual y se integró en `main.py` mediante bucles interactivos de validación. |
| 9 | "Cómo formatear cadenas con anchos fijos (`f-strings`) en Python para alinear reportes financieros y tablas tabuladas en la consola." | Gemini | Uso de especificadores `:<` (izquierda) y `:>` (derecha) con inclusión de prefijos `AR$` dentro del ancho de columna. | Se ajustó la estética a 88 caracteres en los reportes de inventario y se corrigieron los desfasajes en las barras separadoras de la tabla de transacciones. |
