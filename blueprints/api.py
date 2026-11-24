from flask import Blueprint, current_app, jsonify, request

from models.conn import db
from models.model import Summary
from modules.auth import api_login_required, get_current_user
from modules.summarizer import summarize_text

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/summaries', methods=['GET'])
@api_login_required
def list_summaries():
    user = get_current_user()
    summaries = Summary.query.filter_by(user_id=user.id).order_by(Summary.created_at.desc()).all()
    return jsonify([summary.to_dict() for summary in summaries])


@api_bp.route('/summaries', methods=['POST'])
@api_login_required
def create_summary():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'JSON object required'}), 400

    if not isinstance(data.get('title'), str) or not isinstance(data.get('text'), str):
        return jsonify({'error': 'title and text must be strings'}), 400

    title = data['title'].strip()
    original_text = data['text'].strip()
    if not title:
        return jsonify({'error': 'title is required'}), 400
    if len(title) > 150:
        return jsonify({'error': 'title must be 150 characters or fewer'}), 400
    if not original_text:
        return jsonify({'error': 'text is required'}), 400
    if len(original_text) > 30000:
        return jsonify({'error': 'text must be 30000 characters or fewer'}), 400

    user = get_current_user()
    try:
        result = summarize_text(original_text, current_app.config['SBERT_MODEL'])
        summary = Summary(
            user_id=user.id,
            title=title,
            original_text=original_text,
            summary_text=result
        )
        db.session.add(summary)
        db.session.commit()
        return jsonify(summary.to_dict()), 201
    except Exception:
        db.session.rollback()
        current_app.logger.exception('API summary generation failed')
        return jsonify({'error': 'summary generation failed'}), 500
