from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

IVA_RATES = {
    'cafe': 0.05,
    'harina': 0.05,
    'pastas': 0.05,
    'embutidos': 0.05,
    'licores': 0.19,
    'cereales': 0.19,
    'aceites': 0.19,
    'condimentos': 0.19,
    'carne': 0.0,
    'pescado': 0.0,
    'leche': 0.0,
    'queso': 0.0
}

def calcular_iva(tipo_producto, valor_sin_iva):

    tipo_producto_lower = tipo_producto.lower().strip()
    
    if tipo_producto_lower not in IVA_RATES:
        return None
    
    porcentaje_iva = IVA_RATES[tipo_producto_lower]
    valor_iva = valor_sin_iva * porcentaje_iva
    valor_total = valor_sin_iva + valor_iva
    
    return {
        'nombreProducto': tipo_producto,
        'tipoProducto': tipo_producto_lower,
        'valorSinIVA': round(valor_sin_iva, 2),
        'porcentajeIVA': int(porcentaje_iva * 100),
        'valorIVA': round(valor_iva, 2),
        'valorTotal': round(valor_total, 2),
        'timestamp': datetime.now().isoformat()
    }

@app.route('/calcular-iva', methods=['POST'])
def endpoint_calcular_iva():

    try:
        # Validar que el request tenga JSON
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        
        # Validar valores requeridos
        required_fields = ['nombreProducto', 'tipoProducto', 'valorSinIVA']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}',
                'campos_requeridos': required_fields
            }), 400
        
        # Obtener valores
        nombre_producto = data['nombreProducto']
        tipo_producto = data['tipoProducto']
        valor_sin_iva = data['valorSinIVA']
        
        # Validar valores
        if not isinstance(nombre_producto, str) or not nombre_producto.strip():
            return jsonify({
                'error': 'nombreProducto debe ser una cadena no vacía'
            }), 400
        
        if not isinstance(tipo_producto, str) or not tipo_producto.strip():
            return jsonify({
                'error': 'tipoProducto debe ser una cadena no vacía'
            }), 400
        
        try:
            valor_sin_iva = float(valor_sin_iva)
            if valor_sin_iva < 0:
                raise ValueError("El valor no puede ser negativo")
        except (ValueError, TypeError):
            return jsonify({
                'error': 'valorSinIVA debe ser un número positivo'
            }), 400
        
        # Calculo del iva
        resultado = calcular_iva(tipo_producto, valor_sin_iva)
        
        if resultado is None:
            tipos_disponibles = list(IVA_RATES.keys())
            return jsonify({
                'error': f'Tipo de producto "{tipo_producto}" no encontrado',
                'tipos_disponibles': tipos_disponibles
            }), 400
        
        resultado['nombreProducto'] = nombre_producto
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/tipos-productos', methods=['GET'])
def obtener_tipos_productos():

    productos_info = []
    for tipo, tasa in IVA_RATES.items():
        productos_info.append({
            'tipoProducto': tipo,
            'porcentajeIVA': int(tasa * 100)
        })
    
    return jsonify({
        'success': True,
        'data': productos_info,
        'total_productos': len(productos_info)
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

# Manejo de errores:

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint no encontrado',
        'endpoints_disponibles': [
            'POST /calcular-iva',
            'GET /tipos-productos',
            'GET /health'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Método no permitido para este endpoint'
    }), 405

if __name__ == '__main__':
    import os
    
    # Definir puerto:
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Iniciando API de IVA Colombia...")
    print("📋 Endpoints disponibles:")
    print("   POST /calcular-iva - Calcula IVA para productos")
    print("   GET /tipos-productos - Lista productos disponibles")
    print("   GET /health - Estado de la API")
    print(f"Corriendo en: http://0.0.0.0:{port}")
    

    app.run(
        debug=False,  
        host='0.0.0.0',  
        port=port,
        threaded=True  
    )
