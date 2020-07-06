import json

from flask import Blueprint

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Equipment

repair = Blueprint('repair', __name__)


@repair.route('/repair', methods=['GET', 'POST'])
def repairs():
    equipment = db_session.query(Equipment).filter_by(EquipmentCode='LS1').first()
    return json.dumps(equipment, cls=AlchemyEncoder, ensure_ascii=False)
