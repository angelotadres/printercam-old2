from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from printercam.auth import login_required
from printercam.db import get_db

bp = Blueprint('cameras', __name__)


@bp.route('/')
def index():
    db = get_db()
    cameras = db.execute(
        'SELECT c.id, token, fingerprint, created, author_id, username'
        ' FROM camera c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('cameras/index.html', cameras=cameras)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        token = request.form['token']
        fingerprint = request.form['fingerprint']
        error = None

        if not token:
            error = 'token is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO camera (token, fingerprint, author_id)'
                ' VALUES (?, ?, ?)',
                (token, fingerprint, g.user['id'])
            )
            db.commit()
            return redirect(url_for('cameras.index'))

    return render_template('cameras/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    camera = get_camera(id)

    if request.method == 'POST':
        token = request.form['token']
        fingerprint = request.form['fingerprint']
        error = None

        if not token:
            error = 'token is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE camera SET token = ?, fingerprint = ?'
                ' WHERE id = ?',
                (token, fingerprint, id)
            )
            db.commit()
            return redirect(url_for('cameras.index'))

    return render_template('cameras/update.html', camera=camera)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_camera(id)
    db = get_db()
    db.execute('DELETE FROM camera WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('cameras.index'))


def get_camera(id, check_author=True):
    camera = get_db().execute(
        'SELECT p.id, token, fingerprint, created, author_id, username'
        ' FROM camera p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if camera is None:
        abort(404, f"Camera id {id} doesn't exist.")

    if check_author and camera['author_id'] != g.user['id']:
        abort(403)

    return camera
