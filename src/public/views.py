"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template, jsonify, request
from .forms import vstupkarty
from ..data.database import db
from ..data.models import LogUser, karty
from sqlalchemy import func

blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = vstupkarty()
    if form.validate_on_submit():
        karty.create(**form.data)
    return render_template("public/karty.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/vystup',methods=['GET'])
def vystup():
    pole = db.session.query(karty.CISLO_KARTY.label("CISLO_KARTY"),func.strftime('%Y-%m-%d %H:%M', karty.TIME).label("time")).group_by(func.strftime('%Y-%m', karty.TIME)).all()
    return render_template("public/vystup.tmpl",data = pole)

@blueprint.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@blueprint.route('/jquery', methods=['GET'])
def jquerylist():
    return render_template('public/jquery.tmpl')

@blueprint.route('/_status', methods= ['GET',  'POST'])
def get_temps():
    #cur_temps = cur.fetchall()
    cur = db.session.query(karty.id).all()
    json_result=[]
    for result in cur:
        d = {
            'id':result.id,

        }
        json_result.append(d)
    return jsonify( data = json_result)


@blueprint.route('/aktivnivypis', methods= ['GET',  'POST'])
def activelist():
    return render_template('public/table.tmpl')