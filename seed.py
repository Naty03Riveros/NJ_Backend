from app import create_app
from models import db, Vino

app = create_app()

with app.app_context():
    # Lista de vinos
    wine1 = Vino(nombre='Cabernet Sauvignon', tipo='Tinto', precio=29.99, cantidad=50, descripcion='Vino tinto robusto con aromas a frutas rojas.', imagen_url='cabernet_sauvignon.jpg')
    wine2 = Vino(nombre='Chardonnay', tipo='Blanco', precio=19.99, cantidad=60, descripcion='Vino blanco con notas a manzana y mantequilla.', imagen_url='chardonnay.jpg')
    wine3 = Vino(nombre='Merlot', tipo='Tinto', precio=25.99, cantidad=40, descripcion='Vino tinto suave y afrutado.', imagen_url='merlot.jpg')

    db.session.add(wine1)
    db.session.add(wine2)
    db.session.add(wine3)
    db.session.commit()
    
    print("Database actualizada!")
