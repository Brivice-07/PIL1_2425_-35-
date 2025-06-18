from flask import Blueprint, request, jsonify
from app.extensions import db # Nécessaire pour les opérations DB
from app.messaging.models import Conversation, Message, ConversationParticipant
from app.auth.models import User # Pour lier les messages et conversations aux utilisateurs
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

bp = Blueprint('messaging', __name__)

# --- API pour les Conversations ---

# GET /api/messaging/conversations
# Récupère toutes les conversations de l'utilisateur actuel
@bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_user_conversations():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Récupère toutes les conversations auxquelles l'utilisateur participe
    conversations = user.conversations.all()
    return jsonify([conv.to_dict() for conv in conversations]), 200

# GET /api/messaging/conversations/<int:conversation_id>
# Récupère une conversation spécifique et ses messages
@bp.route('/conversations/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation_details(conversation_id):
    current_user_id = get_jwt_identity()

    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"msg": "Conversation not found"}), 404

    # Vérifier que l'utilisateur est bien un participant de cette conversation
    if not any(p.id == current_user_id for p in conversation.participants):
        return jsonify({"msg": "Unauthorized access to conversation"}), 403

    # Récupérer les messages triés par timestamp
    messages = conversation.messages.order_by(Message.timestamp).all()

    return jsonify({
        "conversation": conversation.to_dict(),
        "messages": [msg.to_dict() for msg in messages]
    }), 200

# POST /api/messaging/conversations
# Démarre une nouvelle conversation (ex: entre l'utilisateur actuel et un autre utilisateur)
@bp.route('/conversations', methods=['POST'])
@jwt_required()
def start_new_conversation():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    participant_id = data.get('participant_id')
    title = data.get('title') # Optionnel

    if not participant_id or participant_id == current_user_id:
        return jsonify({"msg": "Invalid participant ID"}), 400

    target_user = User.query.get(participant_id)
    if not target_user:
        return jsonify({"msg": "Target user not found"}), 404

    current_user = User.query.get(current_user_id)

    # Optionnel: Vérifier si une conversation existe déjà entre ces deux utilisateurs
    # Ceci est plus complexe et peut nécessiter une requête plus élaborée sur la table d'association
    # Pour l'instant, on permet de créer de nouvelles conversations même si existantes.

    new_conversation = Conversation(title=title)
    new_conversation.participants.append(current_user)
    new_conversation.participants.append(target_user)

    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({"msg": "Conversation created", "conversation": new_conversation.to_dict()}), 201


# --- API pour les Messages ---

# POST /api/messaging/conversations/<int:conversation_id>/messages
# Envoie un message dans une conversation spécifique
@bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"msg": "Message content is required"}), 400

    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"msg": "Conversation not found"}), 404

    # Vérifier que l'utilisateur est bien un participant de cette conversation
    if not any(p.id == current_user_id for p in conversation.participants):
        return jsonify({"msg": "Unauthorized to send message to this conversation"}), 403

    new_message = Message(
        conversation_id=conversation.id,
        sender_id=current_user_id,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()

    # Optionnel: marquer les autres messages comme lus pour l'expéditeur si c'est la dernière réponse
    # ou implémenter une logique de "messages lus" plus sophistiquée

    return jsonify({"msg": "Message sent", "message": new_message.to_dict()}), 201


# PUT /api/messaging/messages/<int:message_id>/read
# Marque un message comme lu
@bp.route('/messages/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_as_read(message_id):
    current_user_id = get_jwt_identity()
    message = Message.query.get(message_id)

    if not message:
        return jsonify({"msg": "Message not found"}), 404

    conversation = Conversation.query.get(message.conversation_id)
    if not conversation or not any(p.id == current_user_id for p in conversation.participants):
        return jsonify({"msg": "Unauthorized to mark this message as read"}), 403

    message.read = True
    db.session.commit()
    return jsonify({"msg": "Message marked as read"}), 200