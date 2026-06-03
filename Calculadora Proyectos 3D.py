import ipywidgets as widgets
from IPython.display import display

#ENTRADAS DE USUARIO
horas = widgets.FloatText(value=1.0, description="Cuantas horas de impresión tomo:")
watts = widgets.FloatText(value=150.0, description="Cuantos Watts consume la impresora por hora:")
gramos = widgets.FloatText(value=10.0, description="Cuantos Gramos de filamento se utilizaron:")
diseno = widgets.FloatText(value=1.0, description="Cuantas Horas te tomo diseñar el modelo:")
complejidad = widgets.Dropdown(options=[(1, 1), (2, 2), (3, 3)], description="Complejidad del modelo:")
urgente = widgets.Checkbox(value=False, description="¿Pedido urgente?")
usa_iva = widgets.Checkbox(value=False, description="¿Requiere Factura?")
usa_tarjeta = widgets.Checkbox(value=False, description="¿Pago Tarjeta?")
boton = widgets.Button(description="Generar Cotización", button_style='success')
output = widgets.Output()

def calcular_cotizacion(b):
    output.clear_output()
    with output:
        #Constantes y Variables Base
        PRECIO_KWH, PRECIO_GRAMO, DEPRECIACION, TASA_FALLO = 2.30, 0.23, 2.00, 0.15
        MANTENIMIENTO = 0.50
        
        #Calculos 
        factor_post_proc = 1 + (complejidad.value * 0.1)
        costo_energia = (((watts.value / 1000) * horas.value) + ((95 / 1000) * diseno.value)) * PRECIO_KWH
        costo_material = gramos.value * PRECIO_GRAMO
        costo_maquina = horas.value * (DEPRECIACION + MANTENIMIENTO)
        costo_tiempo = (diseno.value * 10) * factor_post_proc
        
        costo_total = (costo_energia + costo_material + costo_maquina + costo_tiempo) * (1 + TASA_FALLO)
        
        precio_est = costo_total * 1.25
        precio_pub = costo_total * 1.60
        
        if urgente.value:
            precio_est *= 1.5
            precio_pub *= 1.5
            
        def final(p):
            if usa_iva.value: p += (p * 0.16)
            if usa_tarjeta.value: p += (p * 0.035)
            return p

        #REPORTE DETALLADO 
        print("COTIZACIÓN DE IMPRESIÓN 3D - PROTOTIPA3D")
        print("\n   Precio BASE")
        print(f"Precio solo luz y material: ${costo_energia + costo_material:.2f}mxn")
        print(f"Precio con máquina y tiempo: ${costo_maquina + costo_tiempo:.2f}mxn")
        print("Nota: El costo total incluye un margen para imprevistos y fallos, así como los costos logísticos si se aplican.")
        print(f"\n   Reporte Final PROTOTIPA3D")
        print(f"Costo operativo total: ${costo_total:.2f}mxn")
        print(f"Precio para Estudiante: ${final(precio_est):.2f}mxn")
        print(f"Precio Público General: ${final(precio_pub):.2f}mxn")

boton.on_click(calcular_cotizacion)
display(horas, watts, gramos, diseno, complejidad, urgente, usa_iva, usa_tarjeta, boton, output)