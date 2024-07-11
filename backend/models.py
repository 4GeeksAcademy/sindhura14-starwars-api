from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
     


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    favorites = db.relationship("Favorites", backref="user", lazy=True)


    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active,
            "favorites": [fav.serialize() for fav in self.favorites]
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    character = db.relationship("Characters", backref="favorites")
    planet = db.relationship("Planets", backref="favorites")

    def __repr__(self) -> str:
        # name = getattr(self.character, "__repr__", False) or getattr(self.planet, "__repr__", False)
        # return name()
        name = getattr(self.character, "name", False) or getattr(self.planet, "name", False)
        fav_type = "Planet" if self.planet_id else "Character"
        return f"<{fav_type} {name}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            # "character": self.character.serialize(),
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }   

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    gender = db.Column(db.String)
    eye_color = db.Column(db.String)
    hair_color=db.Column(db.String)
    is_fav = db.Column(db.Boolean,default=False)
    details = db.Column(db.String(128))
    birth_year=db.Column(db.String)
    height=db.Column(db.Integer)
    image_url=db.Column(db.String(128))

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color":self.eye_color,
            "hair_color":self.hair_color,
            "is_fav":self.is_fav,
            "details":self.details,
            "birth_year":self.birth_year,
            "height":self.height,
            "url":self.image_url
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    diameter = db.Column(db.Numeric(5,0))
    rotation_period=db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity= db.Column(db.String)
    population = db.Column(db.Integer)
    climate= db.Column(db.String)
    terrain = db.Column(db.String)
    surface_water = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    image_url = db.Column(db.String(128))
    is_fav = db.Column(db.Boolean,default=False)

 
    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "is_fav":self.is_fav,
            "diameter": self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "gravity":self.gravity,
            "population":self.population,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
            "created":self.created,
            "edited":self.edited,
            "url":self.image_url
        }





