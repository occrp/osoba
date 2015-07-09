from osoba.core import db

OSOBA_ENTITY_TYPES = (
    "Person",
    "Company",
    "Email",
    "PhoneNumber"
)

OSOBA_RELATIONSHIP_TYPES = (
    "owns",
    "lives_at",
    "works_for",
)

####################################################
#
# Core definitions
#
####################################################

class Entity(db.Model):
    __tablename__ = "osoba_entities"

    id      = db.Column(db.Integer, primary_key=True)
    type    = db.Column(db.String, index=True)
    properties = db.relationship('EntityProperty', backref='entity',
                                 lazy='dynamic', cascade="all, delete-orphan")

    def to_json(self):
        return {"id": self.id, "type": self.type, "properties": dict([
            (x.key, x.value) for x in self.properties.all()
            ])}

    def set_prop(self, key, value):
        prop = self.properties.filter_by(key=key).first()
        if prop:
            prop.value = value
        else:
            prop = EntityProperty(eid=self.id, key=key, value=value)
            db.session.add(prop)
        db.session.commit()
        return prop

    def get_prop(self, key):
        pass


class Relationship(db.Model):
    __tablename__ = "osoba_relationships"

    id      = db.Column(db.Integer, primary_key=True)
    _from   = db.Column(db.Integer, db.ForeignKey('osoba_entities.id'))
    to      = db.Column(db.Integer, db.ForeignKey('osoba_entities.id'))
    type    = db.Column(db.String, index=True)
    properties = db.relationship('RelationshipProperty', backref='relationship',
                                 lazy='dynamic')

    def set_prop(self, key, value):
        prop = self.properties.filter_by(key=key).first()
        if prop:
            prop.value = value
        else:
            prop = RelationshipProperty(rid=self.id, key=key, value=value)
            db.session.add(prop)
        db.session.commit()
        return prop

    def get_prop(self, key):
        pass

    def to_json(self):
        return {"id": self.id, "from": self._from, "to": self.to,
                "type": self.type, "properties": dict([
            (x.key, x.value) for x in self.properties.all()
            ])}


####################################################
#
# Arbitrary properties
#
####################################################

class EntityProperty(db.Model):
    __tablename__ = "osoba_entity_property"

    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, db.ForeignKey('osoba_entities.id'))
    key = db.Column(db.String, index=True)
    value = db.Column(db.String)

    def to_json(self):
        return {
            "key": self.key,
            "value": self.value
        }

class RelationshipProperty(db.Model):
    __tablename__ = "osoba_relationship_property"

    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey('osoba_relationships.id'))
    key = db.Column(db.String, index=True)
    value = db.Column(db.String)

    def to_json(self):
        return {
            "key": self.key,
            "value": self.value
        }

####################################################
#
# Node Types
#
####################################################
#
#class NodePerson(db.Model):
#    __tablename__ = "osoba_node_person"
#
#    id = db.Column(db.Integer, primary_key=True)
#    nationality = db.Column(db.String)
#    first_name = db.Column(db.String)
#    middle_names = db.Column(db.String)
#    last_name = db.Column(db.String)
#
#class NodeCompany(db.Model):
#    __tablename__ = "osoba_node_company"
#
#    id = db.Column(db.Integer, primary_key=True)
#    country = db.Column(db.String)
#    incorporated_date = db.Column(db.Date)
#    dissolved_date = db.Column(db.Date)
