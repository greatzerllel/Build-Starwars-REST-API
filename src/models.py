from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
""" Usuarios """
class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=False, nullable=True)
    name= db.Column(db.String(80), unique=False, nullable=True)
    lastname = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    personajes_favoritos = db.relationship('Favorite_Characters')
    planetas_favoritos = db.relationship('Favorite_Planets')
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "nickname" : self.nickname,
            "name" :self.name,
            "lastname": self.lastname,
            "email": self.email,
          
        }
    """ funcion que serializa con favoritos """
    def serialize_with_favoritos(self):
        personajes_favoritos = [personaje.serialize() for personaje in self.personajes_favoritos]
        planetas_favoritos= [planeta.serialize() for planeta in self.planetas_favoritos]
        
        return {
            "id": self.id,
            "nickname" : self.nickname,
            "name" :self.name,
            "lastname": self.lastname,
            "email": self.email,
            "lista_favoritos" : personajes_favoritos+planetas_favoritos
        }

    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

""" Personas """
class People (db.Model):
    __tablename__="people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    especie = db.Column(db.String(50))
    lugarNacimiento= db.Column(db.String(50))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "edad": self.edad,
            "especie": self.especie,
            "lugarNacimiento" : self.lugarNacimiento
        }
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

""" Planetas """
class Planets (db.Model):
    __tablename__="planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    galaxia = db.Column(db.String(50))
   

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "galaxia": self.galaxia
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

""" personajes favoritos """
class Favorite_Characters (db.Model):
    __tablename__="favoritos_personajes"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    personaje_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    personaje = db.relationship('People')

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "nombre": self.personaje.name
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
""" planets favoritos """
class Favorite_Planets (db.Model):
    __tablename__="favoritos_planetas"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    planeta = db.relationship('Planets')

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "nombre": self.planeta.name
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    