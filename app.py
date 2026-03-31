from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
import requests
import os
from datetime import datetime

app = Flask(__name__)

# ─── Configuration de la base de données ──────────────────────────────────────
DB_TYPE = os.getenv('DB_TYPE', 'xampp')

if DB_TYPE == 'docker':
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://chatuser:password@db:3306/chatdb'
else:
    # XAMPP / WampServer  →  root sans mot de passe par défaut
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:@localhost:3306/chat_distribue'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SERVICE_NAME      = os.getenv('SERVICE_NAME',      'service_1')
SERVICE_PORT      = int(os.getenv('SERVICE_PORT',  '5000'))
OTHER_SERVICE_URL = os.getenv('OTHER_SERVICE_URL', 'http://localhost:5001')


# ═══════════════════════════════════════════════════════
# MODÈLES
# ═══════════════════════════════════════════════════════

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(50), unique=True, nullable=False)
    service_name = db.Column(db.String(50), nullable=True)
    port         = db.Column(db.Integer, nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'username':     self.username,
            'service_name': self.service_name,
            'port':         self.port,
            'created_at':   self.created_at.isoformat()
        }


class Message(db.Model):
    __tablename__ = 'messages'
    id                 = db.Column(db.Integer, primary_key=True)
    content            = db.Column(db.Text, nullable=False)
    sender_id          = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    receiver_id        = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    service_expediteur = db.Column(db.String(50), nullable=False)
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)

    sender   = db.relationship('Utilisateur', foreign_keys=[sender_id],  backref='messages_envoyes')
    receiver = db.relationship('Utilisateur', foreign_keys=[receiver_id], backref='messages_recus')

    def to_dict(self):
        return {
            'id':                self.id,
            'content':           self.content,
            'sender_id':         self.sender_id,
            'sender_username':   self.sender.username   if self.sender   else 'Inconnu',
            'receiver_id':       self.receiver_id,
            'receiver_username': self.receiver.username if self.receiver else 'All',
            'service_expediteur': self.service_expediteur,
            'created_at':        self.created_at.isoformat()
        }


# ═══════════════════════════════════════════════════════
# ROUTES HTML
# ═══════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('chat.html', service_name=SERVICE_NAME)


# ═══════════════════════════════════════════════════════
# API – MESSAGES
# ═══════════════════════════════════════════════════════

@app.route('/api/messages', methods=['GET'])
def get_messages():
    msgs = Message.query.order_by(Message.created_at.asc()).limit(50).all()
    return jsonify([m.to_dict() for m in msgs])


@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or not data.get('content') or not data.get('sender_id'):
        return jsonify({'error': 'content et sender_id sont requis'}), 400

    message = Message(
        content            = data['content'],
        sender_id          = data['sender_id'],
        receiver_id        = data.get('receiver_id'),
        service_expediteur = SERVICE_NAME
    )
    db.session.add(message)
    db.session.commit()

    try:
        requests.post(f"{OTHER_SERVICE_URL}/api/notify", json=message.to_dict(), timeout=3)
    except Exception as e:
        print(f"Autre service non disponible : {e}")

    return jsonify(message.to_dict()), 201


# ═══════════════════════════════════════════════════════
# API – UTILISATEURS
# ═══════════════════════════════════════════════════════

@app.route('/api/users', methods=['GET'])
def get_users():
    users = Utilisateur.query.order_by(Utilisateur.created_at.asc()).all()
    return jsonify([u.to_dict() for u in users])

@app.route('/api/utilisateurs', methods=['GET'])
def get_utilisateurs():
    return get_users()

@app.route('/api/utilisateurs', methods=['POST'])
def create_utilisateur():
    data = request.get_json()
    if not data or not data.get('username'):
        return jsonify({'error': 'username requis'}), 400

    username = data['username'].strip()
    if Utilisateur.query.filter_by(username=username).first():
        return jsonify({'error': "Ce nom d'utilisateur existe déjà"}), 400

    user = Utilisateur(username=username, service_name=SERVICE_NAME, port=SERVICE_PORT)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


# ═══════════════════════════════════════════════════════
# API – SERVICES / HEALTH / STATS / NOTIFY
# ═══════════════════════════════════════════════════════

@app.route('/api/services', methods=['GET'])
def get_services():
    services = [{'name': SERVICE_NAME, 'port': SERVICE_PORT, 'status': 'active', 'url': f'http://localhost:{SERVICE_PORT}'}]
    try:
        resp = requests.get(f"{OTHER_SERVICE_URL}/api/health", timeout=3)
        other_status = 'active' if resp.status_code == 200 else 'inactive'
    except Exception:
        other_status = 'inactive'

    services.append({
        'name':   'service_2' if SERVICE_NAME == 'service_1' else 'service_1',
        'port':   5001         if SERVICE_PORT  == 5000       else 5000,
        'status': other_status,
        'url':    OTHER_SERVICE_URL
    })
    return jsonify(services)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service_name': SERVICE_NAME,
                    'port': SERVICE_PORT, 'db_type': DB_TYPE,
                    'timestamp': datetime.utcnow().isoformat()})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'total_messages':   Message.query.count(),
        'total_users':      Utilisateur.query.count(),
        'service_messages': Message.query.filter_by(service_expediteur=SERVICE_NAME).count(),
        'service_name':     SERVICE_NAME,
        'db_type':          DB_TYPE
    })


@app.route('/api/notify', methods=['POST'])
def notify_message():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400

    sender = Utilisateur.query.get(data.get('sender_id'))
    if not sender:
        sender = Utilisateur(
            username     = data.get('sender_username', f"user_{data.get('sender_id')}"),
            service_name = data.get('service_expediteur', 'unknown'),
            port         = 0
        )
        db.session.add(sender)
        db.session.flush()

    message = Message(
        content            = data['content'],
        sender_id          = sender.id,
        receiver_id        = data.get('receiver_id'),
        service_expediteur = data.get('service_expediteur', 'unknown')
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({'status': 'received'}), 200


def ensure_schema_compatibility():
    """Met à niveau automatiquement les anciennes colonnes MySQL vers le schéma actuel."""
    if db.engine.dialect.name != 'mysql':
        return

    inspector = inspect(db.engine)
    
    with db.engine.begin() as connection:
        tables = set(inspector.get_table_names())
        
        if 'utilisateurs' in tables:
            user_cols = {col['name'] for col in inspector.get_columns('utilisateurs')}
            if 'service_name' not in user_cols:
                connection.execute(text(
                    "ALTER TABLE utilisateurs ADD COLUMN service_name VARCHAR(50) NOT NULL DEFAULT 'unknown'"
                ))
            if 'port' not in user_cols:
                connection.execute(text(
                    "ALTER TABLE utilisateurs ADD COLUMN port INT NOT NULL DEFAULT 0"
                ))


# ═══════════════════════════════════════════════════════
if __name__ == '__main__':
    with app.app_context():
        ensure_schema_compatibility()
        db.create_all()
        if Utilisateur.query.count() == 0:
            demo = Utilisateur(username=f"User_{SERVICE_PORT}", service_name=SERVICE_NAME, port=SERVICE_PORT)
            db.session.add(demo)
            db.session.commit()
            print(f"Utilisateur de démo créé : {demo.username}")

    print(f"Service : {SERVICE_NAME}  |  Port : {SERVICE_PORT}  |  DB : {DB_TYPE}")
    print(f"URL     : http://localhost:{SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)
