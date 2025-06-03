from database.confbd import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM

tipo_documento_pg_enum = ENUM('cc', 'ce', 'ti', 'pp', name='tipo_documento_enum', create_type=False)

class ModificarDis(db.Model):
    __tablename__ = 'modificardis'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo_doc = Column(tipo_documento_pg_enum, nullable=False) 
    numero_doc = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ModificarDis id={self.id}, nombre='{self.nombre}', tipo_doc='{self.tipo_doc}', numero_doc={self.numero_doc}>"
