import flask
from flask_cors import CORS
import os
from flask import jsonify, request
from werkzeug.utils import secure_filename
import extract_text
import open_ai_response_shop

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to New OCR service</h1><p>Prototype for a new OCR service, which is super accurate. </p>"


@app.route("/make_ocr_request", methods=["POST"])
def understand_the_document():

    print(request)
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    filename = secure_filename(file.filename)

    print(filename)
    file_path = os.path.join('../../documents', filename)
    file.save(os.path.join('../../documents', filename))

    print(filename)

    request_dict = request.form.to_dict()


    fileType = filename.rsplit('.', 1)[1].lower()
    result = {}
    text = ""
    if fileType=="pdf":
        text = extract_text.cleaned_text_from_pdf(file_path)
    else:
        text = extract_text.cleaned_text_from_image(file_path)

    doc_type = request_dict.get("document_type", None)
    if doc_type is not None:
        if doc_type == "shop_establishment":
            result = open_ai_response_shop.generate_ocr_result_for_shop(text)
            print(result)
            return result
        if doc_type == "partnership_deed":
            result = open_ai_response_shop.generate_ocr_result_for_partnership(text)
            print(result)
            return result
        if doc_type == "unknown":
            questions = request_dict.get("questions", None)
            print(questions)
            arr = questions.split(",")
            result = open_ai_response_shop.generate_ocr_result_for_unknown(text, arr)
            print(result)
            return result


app.run(port=8000)
