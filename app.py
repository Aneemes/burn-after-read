import os
import uuid
import bcrypt
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy.pool import NullPool  # recommended for serverless (e.g., Vercel)

from utils import get_or_create_key

load_dotenv()

app = Flask(__name__)

# Use NeonDB URI from environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "poolclass": NullPool  # For serverless environments like Vercel
}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', get_or_create_key())
fernet = Fernet(ENCRYPTION_KEY)

class Note(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.LargeBinary, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    read_at = db.Column(db.DateTime, nullable=True)

@app.route('/', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        raw_content = request.form['content'].encode()
        password = request.form.get('password', '').strip()

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) if password else None
        encrypted_content = fernet.encrypt(raw_content)
        
        note_id = str(uuid.uuid4())
        note = Note(id=note_id, content=encrypted_content, password_hash=password_hash)
        db.session.add(note)
        db.session.commit()
        return render_template('create_note.html', note_link=url_for('view_note', note_id=note_id, _external=True))
    return render_template('create_note.html')

@app.route('/note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.is_read:
        return render_template('view_note.html', message="❌ This note has already been read and is no longer available.")
    
    if note.password_hash:
        if request.method == 'POST':
            password_input = request.form.get('password', '').encode()
            password_hash = note.password_hash.encode() if isinstance(note.password_hash, str) else note.password_hash

            try:
                if bcrypt.checkpw(password_input, password_hash):
                    try:
                        decrypted_content = fernet.decrypt(note.content).decode()
                    except InvalidToken:
                        flash("Invalid or corrupted content.")
                        return redirect(url_for('create_note'))
                    note.is_read = True
                    note.read_at = db.func.current_timestamp()
                    db.session.commit()
                    return render_template('view_note.html', content=decrypted_content)
                else:
                    return render_template('password_prompt.html', error="Incorrect password.", note_id=note_id)
            except ValueError:
                # This is where the "Invalid salt" error would be caught
                return render_template('password_prompt.html', error="Corrupted password hash.", note_id=note_id)

        return render_template('password_prompt.html', note_id=note_id)

    # No password protection, just decrypt and show
    try:
        decrypted_content = fernet.decrypt(note.content).decode()
    except InvalidToken:
        flash("Invalid or corrupted content.")
        return redirect(url_for('create_note'))
    note.is_read = True
    note.read_at = db.func.current_timestamp()
    db.session.commit()
    return render_template('view_note.html', content=decrypted_content)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

