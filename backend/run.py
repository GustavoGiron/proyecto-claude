from app import create_app

app = create_app()

if __name__ == "__main__":
    # Ya no creamos tablas aquí; asumimos que la base de datos y sus esquemas
    # ya existen y se gestionan con migraciones externas o manualmente.
    app.run(debug=True, port=5000)