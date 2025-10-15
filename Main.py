from flask import Flask, request, send_file, jsonify
import qrcode
from io import BytesIO
import base64
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/generar-qr', methods=['POST'])
def generar_qr():
    try:
        datos = request.get_json()
        
        if not datos or 'data' not in datos:
            return jsonify({'error': 'Se requiere el campo "data"'}), 400
        
        contenido = datos['data']
        size_param = datos.get('size', 10)
        border = datos.get('border', 1)
        formato = datos.get('formato', 'archivo')
        
        width = None
        height = None
        box_size = 10
        
        if isinstance(size_param, str) and ('x' in size_param.lower() or '_' in size_param):
            try:
                separator = 'x' if 'x' in size_param.lower() else '_'
                dimensions = size_param.lower().split(separator)
                width = int(dimensions[0])
                height = int(dimensions[1])
            except:
                return jsonify({'error': 'Formato de size inválido. Use formato: 300x300 o 300_300'}), 400
        else:
            box_size = int(size_param)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        
        qr.add_data(contenido)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if width and height:
            from PIL import Image
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        if formato == 'base64':
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return jsonify({
                'success': True,
                'imagen': f'data:image/png;base64,{img_base64}'
            })
        else:
            return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generar-qr-get', methods=['GET'])
def generar_qr_get():
    try:
        contenido = request.args.get('data')
        
        if not contenido:
            return jsonify({'error': 'Se requiere el parámetro "data"'}), 400
        
        size_param = request.args.get('size', '10')
        border = int(request.args.get('border', 1))
        
        width = None
        height = None
        box_size = 10
        
        if 'x' in size_param.lower() or '_' in size_param:
            try:
                separator = 'x' if 'x' in size_param.lower() else '_'
                dimensions = size_param.lower().split(separator)
                width = int(dimensions[0])
                height = int(dimensions[1])
            except:
                return jsonify({'error': 'Formato de size inválido. Use formato: 300x300 o 300_300'}), 400
        else:
            box_size = int(size_param)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        
        qr.add_data(contenido)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if width and height:
            from PIL import Image
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return send_file(buffer, mimetype='image/png')
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API funcionando correctamente'})

if __name__ == '__main__':
    import socket
    
    def encontrar_puerto_disponible(puerto_inicial=5000, puerto_maximo=5100):
        for puerto in range(puerto_inicial, puerto_maximo):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('0.0.0.0', puerto))
                sock.close()
                return puerto
            except OSError:
                continue
        raise RuntimeError(f"No se encontró un puerto disponible entre {puerto_inicial} y {puerto_maximo}")
    
    puerto = encontrar_puerto_disponible()
    print(f"Servidor iniciado en http://127.0.0.1:{puerto}")
    app.run(host='0.0.0.0', port=puerto)