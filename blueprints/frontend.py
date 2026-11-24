from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from models.conn import db
from models.model import Summary, User
from modules.auth import get_current_user, login_required
from modules.forms import LoginForm, RegisterForm, SummaryForm
from modules.summarizer import summarize_text

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def home():
    form = SummaryForm() if get_current_user() else None
    return render_template('index.html', form=form)


@frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    if get_current_user() is not None:
        return redirect(url_for('frontend.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Account creato. Ora puoi accedere.', 'success')
            return redirect(url_for('frontend.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email già in uso.', 'danger')

    return render_template('register.html', form=form)


@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if get_current_user() is not None:
        return redirect(url_for('frontend.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user and user.check_password(form.password.data):
            session.clear()
            session['user_id'] = user.id
            flash(f'Accesso effettuato con successo.', 'success')
            return redirect(url_for('frontend.home'))
        flash('Email o password non corretti.', 'danger')

    return render_template('login.html', form=form)


@frontend_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Hai effettuato la disconnessione.', 'info')
    return redirect(url_for('frontend.home'))


@frontend_bp.route('/summarize', methods=['POST'])
@login_required
def summarize():
    form = SummaryForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form), 400

    user = get_current_user()
    try:
        result = summarize_text(form.original_text.data, current_app.config['SBERT_MODEL'])
        summary = Summary(
            user_id=user.id,
            title=form.title.data.strip(),
            original_text=form.original_text.data.strip(),
            summary_text=result
        )
        db.session.add(summary)
        db.session.commit()
        return redirect(url_for('frontend.summary_detail', summary_id=summary.id))
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Summary generation failed')
        flash('Non è stato possibile generare il riassunto. Controlla la configurazione del modello.', 'danger')
        return render_template('index.html', form=form), 500


@frontend_bp.route('/archive')
@login_required
def archive():
    user = get_current_user()
    summaries = Summary.query.filter_by(user_id=user.id).order_by(Summary.created_at.desc()).all()
    return render_template('archive.html', summaries=summaries)


@frontend_bp.route('/archive/<int:summary_id>')
@login_required
def summary_detail(summary_id):
    user = get_current_user()
    summary = Summary.query.filter_by(id=summary_id, user_id=user.id).first_or_404()
    return render_template('summary_detail.html', summary=summary)
