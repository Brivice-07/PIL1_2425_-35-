# backend/run.py

from app import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    # Permet d'accéder à l'instance de la base de données et aux modèles dans la console Flask
    # Importez vos modèles ici au fur et à mesure que vous les créez
    # from app.auth.models import User # Exemple
    # return {'db': db, 'User': User}
    return {'db': db} # Pour l'instant, juste la DB

if __name__ == '__main__':
    app.run(debug=True) # debug=True pour le développement, à désactiver en production