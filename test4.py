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
    try:
        data = request.json
        existing_entry = DeviceData.query.filter_by(devID=data['devID']).first()

        if existing_entry:
            # Update existing entry
            existing_entry.contID = data['contID']
            existing_entry.SN = data['SN']
            existing_entry.humanInfo = data['humanInfo']
            existing_entry.cadaInfo = data['cadaInfo']
        else:
            # Create new entry
            new_data = DeviceData(
                devID=data['devID'],
                contID=data['contID'],
                SN=data['SN'],
                humanInfo=data['humanInfo'],
                cadaInfo=data['cadaInfo']
            )
            db.session.add(new_data)

        db.session.commit()
        return jsonify({"message": "Data received and stored or updated."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    try:
        all_records = DeviceData.query.all()
        result = []

        for record in all_records:
            record_dict = {
                'id': record.id,
                'devID': record.devID,
                'contID': record.contID,
                'SN': record.SN,
                'humanInfo': record.humanInfo,
                'cadaInfo': record.cadaInfo
            }
            result.append(record_dict)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_specific_data', methods=['GET'])
def get_specific_data():
    try:
        devID = request.args.get('devID')
        if not devID:
            return jsonify({"error": "devID parameter is required"}), 400

        record = DeviceData.query.filter_by(devID=devID).first()
        if not record:
            return jsonify({"error": "No record found for the given devID"}), 404

        record_dict = {
            'id': record.id,
            'devID': record.devID,
            'contID': record.contID,
            'SN': record.SN,
            'humanInfo': record.humanInfo,
            'cadaInfo': record.cadaInfo
        }

        return jsonify(record_dict), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

    app.run(host='0.0.0.0', port=10540)