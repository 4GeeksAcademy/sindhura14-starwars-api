import os
from flask_admin import Admin
from backend.models import db, User, Favorites, Characters, Planets
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'slate'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap4')

    class UserView(ModelView):
        column_list = [
            'id', 'email', 'favorites'
        ]

    # Add your models here, for example this is how we add a the User model to the admin

    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(Favorites, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))




    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
