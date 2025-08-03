from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os

# Initialisation de l'app Flask
app = Flask(__name__)
app.secret_key = 'un_mot_de_passe_vraiment_complexe'

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tyfennboulanger2006@gmail.com'  # Adresse Gmail
app.config['MAIL_PASSWORD'] = 'yzmn ztfx cvxs mqgb'             # Mot de passe d'application
app.config['MAIL_DEFAULT_SENDER'] = 'tyfennboulanger2006@gmail.com'
mail = Mail(app)

# Modèle SQLAlchemy
class MessageContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    objet = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Message {self.email} - {self.objet}>"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projet')
def projet():
    return render_template('projet.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        objet = request.form.get('objet')
        message = request.form.get('message')

        # Validation minimale
        if not nom or not prenom or not email or not objet or not message:
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for('contact'))

        # Sauvegarde en base de données
        new_msg = MessageContact(nom=nom, prenom=prenom, email=email, objet=objet, message=message)
        db.session.add(new_msg)
        db.session.commit()

        # Envoi de l'e-mail
        msg = Message(subject=f"Demande de contact : {objet}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['tyfennboulanger2006@gmail.com'],
                      body=f"""
NOM : {nom}
PRÉNOM : {prenom}
EMAIL : {email}

OBJET : {objet}

MESSAGE :
{message}
""")
        try:
            mail.send(msg)
            flash("Votre message a été envoyé avec succès !", "success")
        except Exception as e:
            flash(f"Erreur lors de l'envoi de l'e-mail : {str(e)}", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html')

# Démarrage de l'application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
