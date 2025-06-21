from flask import Flask, jsonify , request 
from flask_sqlalchemy import SQLAlchemy
import configparser
import DateTime
# import os
app = Flask(__name__)

def read_file_for_database_conn(filepath = 'config.properties'):
    config = configparser.ConfigParser()
    config.read(filepath)
    return config['Database']

config = read_file_for_database_conn()
dbname  = config.get('db_name')
db_port  = config.getint('port')
db_user = config.get('db_user')
db_pass = config.get('db_pass')
host = config.get('host')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{db_user}:{db_pass}@{host}:{db_port}/{dbname}"
)

db = SQLAlchemy(app)

class table_submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False )
    message = db.Column(db.String)
    # subbmitted_at = db.Column(db.DateTime, default = db.func.now())

    def __returnname__(self):
        return f'(table_submission {self.name})'
    
    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'email':self.email,
            'message':self.message,
            # 'submitted_at':self.subbmitted_at.is_format() 
        }

# -------THIS IS THE HOME PAGE-----------
@app.route('/')
def home():
    return "welcome"


# --------CREATE THE ITME FOR THE DATABASE--------
@app.route('/create' , methods=['POST'])
def create_item():
    data = request.get_json()
    
    new_item = table_submission(
        id=data.get('id'),
        name=data.get('name'),
        email=data.get('email'),
        message=data.get('message')
    )

    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"itme_saved" : new_item.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


#--------FETCH ALL THE DATA  
@app.route('/all' , methods=['GET'])
def select_all_items():
    item = table_submission.query.all()
    return jsonify([submissions.to_dict() for submissions in item])

# -------FETCH DATA BY THEIR ID----------- 
@app.route('/all/<int:id>' , methods=['GET'])
def select_by_id(id):
    
    item = table_submission.query.get(id)
    if item: 
        return jsonify(item.to_dict())
    return jsonify({f"error: item id {id}not found "})

# ------DELETE THE ITEM BY THEIR ID ---------
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = db.session.get(table_submission , id)
    if not id:
        return jsonify({f"error message that item id {id} not found"})
    else:
        try:
            db.session.delete(id)
            db.session.commit()
            return jsonify({f"message : item deleted successfully"})
        except Exception as  e:
            return jsonify({f"erroe occured": str(e)})
        
# ---- RUN THE MAIN APP ------
if __name__ == '__main__':
    app.run(debug = True , port = 5000 , host='0.0.0.0')