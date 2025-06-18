from app.extensions import db
from datetime import datetime
from sqlalchemy.schema import UniqueConstraint

# Optionnel: Importez le modèle User si vous ne l'avez pas déjà fait dans app.auth.models
# from app.auth.models import User # Assurez-vous que User est importable ici si besoin


class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    # Titre de la conversation (optionnel, utile pour les listes de conversations)
    title = db.Column(db.String(255), nullable=True)

    # Date de création et de mise à jour de la conversation
    # Ces champs sont automatiquement gérés par SQLAlchemy

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relation avec les messages de cette conversation
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade="all, delete-orphan")
    # Relation avec les participants (via la table d'association ConversationParticipant)
    participants = db.relationship('User', secondary='conversation_participants', back_populates='conversations')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'participants_ids': [p.id for p in self.participants],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_message_preview': self.messages.order_by(Message.timestamp.desc()).first().content if self.messages.first() else None
        }

# Table d'association pour la relation Many-to-Many entre User et Conversation
# Un utilisateur peut participer à plusieurs conversations, une conversation a plusieurs participants
class ConversationParticipant(db.Model):
    __tablename__ = 'conversation_participants'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), primary_key=True)

    # Pour s'assurer qu'un même utilisateur n'est pas ajouté deux fois à la même conversation
    __table_args__ = (UniqueConstraint('user_id', 'conversation_id', name='_user_conversation_uc'),)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    # Permet d'accéder à l'objet Conversation ou User directement depuis un Message
    sender_relationship = db.relationship('User', back_populates='sent_messages', lazy=True, foreign_keys=[sender_id])

    recipient_relationship = db.relationship('User', back_populates='received_messages', lazy=True, foreign_keys=[recipient_id])
    
    conversation = db.relationship('Conversation', back_populates='messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'is_read': self.is_read
        }