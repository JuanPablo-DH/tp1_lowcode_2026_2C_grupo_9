import matplotlib.pyplot as plt
import pandas as pd
from src.models.producto import Producto
from src.models.transaccion import Transaccion

class Graficador:
    @staticmethod
    def _generar_grafico_stock(df_productos: pd.DataFrame) -> str:
        """
        Método privado: Genera y guarda el gráfico de stock actual vs. stock mínimo por producto.
        """
        ruta_grafico = "data/grafico_stock_productos.png"
        
        ax = df_productos.plot.barh(
            x="nombre", 
            y=["stock_actual", "stock_minimo"], 
            color=["#2b5c8f", "#e74c3c"],
            figsize=(9, 6)
        )

        for container in ax.containers:
            ax.bar_label(container, padding=3, fontsize=8)

        ax.tick_params(bottom=False, labelbottom=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        max_val = df_productos[["stock_actual", "stock_minimo"]].values.max()
        ax.set(title="Stock actual vs. stock mínimo por producto", ylabel="", xlim=(0, max_val * 1.35))
        
        plt.tight_layout()
        plt.savefig(ruta_grafico, dpi=300)
        plt.close(ax.figure)

        return f"✅ Gráfico de Stock guardado en: '{ruta_grafico}'"

    @staticmethod
    def _generar_grafico_ventas(df_productos: pd.DataFrame, df_tx: pd.DataFrame) -> str:
        """
        Método privado: Genera y guarda el gráfico de ingresos de ventas realizadas por categoría.
        """
        ruta_grafico = "data/grafico_ventas_categoria.png"

        if not df_tx.empty and "tipo" in df_tx.columns and not df_tx[df_tx["tipo"] == "VENTA"].empty:
            df_ventas = df_tx[df_tx["tipo"] == "VENTA"].merge(df_productos[["id_producto", "categoria"]], on="id_producto")
            df_ingresos = df_ventas.groupby("categoria")["monto_total"].sum().reset_index()

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(df_ingresos["categoria"], df_ingresos["monto_total"], color="#27ae60", width=0.45)

            ax.set(title="Ingresos de ventas realizadas por categoría (AR$)", ylim=(0, df_ingresos["monto_total"].max() * 1.15))
            ax.tick_params(left=False, labelleft=False)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

            ax.bar_label(bars, labels=[f"AR$ {v:,.0f}" for v in df_ingresos["monto_total"]], padding=3, fontsize=9)
            
            plt.tight_layout()
            plt.savefig(ruta_grafico, dpi=300)
            plt.close(fig)

            return f"✅ Gráfico de Ventas guardado en: '{ruta_grafico}'"
        else:
            return "⚠️ No se generó el gráfico de ventas: aún no existen transacciones de tipo VENTA."

    @staticmethod
    def generar_graficos_png(lista_productos: list[Producto], lista_transacciones: list[Transaccion]) -> list[str]:
        """
        Transforma las listas de objetos del sistema a DataFrames de Pandas
        y coordina la generación de los archivos .png de los gráficos analíticos.
        Devuelve una lista con los mensajes de los archivos creados o advertencias.
        """
        if not lista_productos:
            raise ValueError("No hay productos en el catálogo para generar gráficos.")

        df_productos = pd.DataFrame([p.to_dict() for p in lista_productos])
        df_tx = pd.DataFrame([t.to_dict() for t in lista_transacciones]) if lista_transacciones else pd.DataFrame()

        archivos_generados = []

        archivos_generados.append(Graficador._generar_grafico_stock(df_productos))
        archivos_generados.append(Graficador._generar_grafico_ventas(df_productos, df_tx))

        return archivos_generados