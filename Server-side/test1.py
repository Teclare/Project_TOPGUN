from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    devID = db.Column(db.String, nullable=False)
    contID = db.Column(db.String, nullable=False)
    SN = db.Column(db.String, nullable=False)
    humanInfo = db.Column(db.String, nullable=False)
    cadaInfo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<DeviceData {self.id} - devID: {self.devID}, contID: {self.contID}, SN: {self.SN}, humanInfo: {self.humanInfo}, cadaInfo: {self.cadaInfo}>"

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    new_data = DeviceData(
        devID=data['devID'],
        contID=data['contID'],
        SN=data['SN'],
        humanInfo=data['humanInfo'],
        cadaInfo=data['cadaInfo']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data received and stored."}), 200

#========================================================= Run Code is Here

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    command = int(input('Put the command >>>'))

    with app.app_context():  # 이 블록 내에서 앱 컨텍스트를 설정
        if command == 0:
            all_records = DeviceData.query.all()
            for record in all_records:
                print(record)

        elif command == 1:
            device_id_to_filter = input("Enter the device ID to filter: ")
            filtered_records = DeviceData.query.filter_by(devID=device_id_to_filter).all()
            for record in filtered_records:
                print(record)

        else:
            pass

    app.run(host='143.198.221.64', port=10540)
