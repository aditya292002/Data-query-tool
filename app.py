from flask import Flask, render_template, request, redirect, url_for

import requests
import os
from werkzeug.utils import secure_filename
from typing import Optional  # Now should import correctly

app = Flask(__name__)

BASE_API_URL = "http://3.135.6.212:8889/api/v1/process"
FLOW_ID = "1f25181d-1f64-4620-b1ef-d01d6690bc18"
TWEAKS = {
    "Chroma-xhWQY": {},
    "RetrievalQA-g9nY0": {},
    "CombineDocsChain-6NqDe": {},
    "AzureOpenAI-YfNoC": {},
    "HuggingFaceEmbeddings-myzm9": {},
    "ConversationBufferMemory-GpJtr": {},
    "CSVLoader-t92mU": {},
    "PromptTemplate-edSIU": {},
    "LLMChain-gGsjl": {}
}

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> str:
    api_url = f"{BASE_API_URL}/{flow_id}"
    payload = {"inputs": inputs}
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload)
    return response.json().get('result', {}).get('result', 'No response text available.')

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ''
    query = ''
    if request.method == 'POST':
        query = request.form.get('query')
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputs = {"csv_file_path": os.path.join(app.config['UPLOAD_FOLDER'], filename)}
        else:
            inputs = {"query": query}
        response_text = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    return render_template('index.html', query=query, response_text=response_text)

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
