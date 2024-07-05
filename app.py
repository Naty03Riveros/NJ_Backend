from flask import Flask, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Vino

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('Index.html')

    @app.route('/tienda')
    def tienda():
        vinos = Vino.query.all()
        return render_template('Tienda.html', vinos=vinos)

    @app.route('/eventos')
    def eventos():
        return render_template('Eventos.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method = 'sha256')
        new_cliente = Cliente(
            nombre=data['nombre'],
            email=data['email'],
            telefono=data.get('telefono'),
            direccion=data.get('direccion'),
            password = hashed_password
        )
        db.session.add(new_cliente)
        db.session.commit()
        return jsonify({'message':'Cliente registrado exitosamente'})
    
    @app.route('/login', methods=['POST']) #DEBEMOS MODIFICAR PARA GENERAR FACTURA CADA QUE SE REALIZA UN PEDIDO
        data = request.get_json()
        cliente = Cliente.query.filter_by(email=data['email']).first()
        if cliente and check_password_hash(cliente.password, data['password']):
            session['cliente_id'] = cliente.id_cliente
            return jsonify({'message': 'Inicio de sesión exitoso'})
        return jsonify({'message': 'Email o contraseña incorrectos'}), 401
    
    @app.route('/pedido', methods=['POST'])
    def realizar_pedido():
        data = request.get_json()
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'message': 'Debe iniciar sesión para realizar un pedido'}), 401
        
        vinos_pedidos = data.get('vinos', [])
        if not vinos_pedidos:
            return jsonify({'message': 'Debe especificar los vinos a pedir'})
        
        total = 0
        for item in vinos_pedidos:
            vino = Vino.query.get(item['id_vino'])
            if not vino or vino.cantidad < item['cantidad']:
                return jsonify({'message': f'El vino con id {item["id_vino"]} no está disponible en la cantidad solicitada'}), 400
            total+= vino.precio * item['cantidad']
        
        new_pedido = Pedido(id_cliente = cliente_id, total=total, estado='pendiente')
        db.session.add(new_pedido)
        db.session.commit()

        for item in vinos_pedidos:
            detalle = DetallePedido(
                id_pedido = new_pedido.id_pedido,
                id_vino = item['id_vino'],
                cantidad = item['cantidad']
            )
            db.session.add(detalle)
            vino = Vino.query.get(item['id_vino'])
            vino.cantidad -= item['cantidad']   #Aquí reducimos stock
            db.session.commit()
        
        return jsonify({'message': 'Pedido realizado exitosamente'})
    
    @app.route('/wines' methods=['POST'])
    def agregar_vino():
        data = request.get_json()
        new_vino = Vino(
            nombre = data['nombre'],
            tipo = data.get('tipo'),
            precio = data['precio'],
            cantidad = data['cantidad'],
            descripcion = data.get('descripcion'),
            imagen_url = data.get('imagen_url')
        )
        db.session.add(new_vino)
        db.session.commit()
        return jsonify({'message': 'Vino agregado exitosamente'})

    @app.route('/wines/<int:id_vino>' methods=['PUT'])
    def actualizar_vino(id_vino):
        data = request.get_json()
        vino = Vino.query.get_or_404(id_vino)
        if 'nombre' in data:
            vino.nombre = data['nombre']
        if 'tipo' in data:
            vino.tipo = data['tipo']
        if 'precio' in data:
            vino.precio = data['precio']
        if 'cantidad' in data:
            vino.cantidad = data['cantidad']
        if 'descripcion' in data:
            vino.descripcion = data['descripcion']
        if 'imagen_url' in data:
            vino.imagen_url = data['imagen_url']
        
        db.session.commit()
        return jsonify({'message': 'Vino actualizado exitosamente'})
    
    @app.route('/wines/<int:id_vino>/stock' methods=['PUT'])
    def actualizar_stock(id_vino):
        data = request.get_json()
        vino = Vino.query.get_or_404(id_vino)
        if 'cantidad' in data:
            vino.cantidad = data['cantidad']
            db.session.commit()
            return jsonify({'message': 'Stock actualizado exitosamente'})
        return jsonify({'message': 'La cantidad de stock es requerida'}), 400


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
