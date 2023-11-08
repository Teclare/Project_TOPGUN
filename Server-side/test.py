#devID, contID, SN, humanInfo, cadaInfo

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

int command = 0

command = input('Put the command >>>')

if command == 0:
    all_records = SensorData.query.all()
    for record in all_records:
        print(record)

elif command == 1:
    filtered_records = SensorData.query.filter_by(device_id=" ").all()
    for record in filtered_records:
        print(record)
        
else:
    pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<DeviceData {self.id} - devID: {self.devid}, contID: {self.contid}, SN: {self.sn}, humanInfo: {self.humaninfo}, cadaInfo: {self.cadainfo}, >"

db.create_all()

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    new_data = DeviceData(
        devID=data['devid'],
        contID=data['contid'],
        SN=data['sn'],
        humanInfo=data['humaninfo'],
        cadaInfo=data['cadainfo']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data received and stored."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10540)
