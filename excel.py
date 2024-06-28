from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        try:
            # Lee el archivo HTML con codificación explícita
            dfs = pd.read_html(file_path, encoding='utf-8')
            
            if dfs:
                df = dfs[0]  # Tomamos la primera tabla encontrada, puedes ajustar esto según tus necesidades
                
                # Depuración: Imprime las primeras filas del DataFrame
                print(df.head())
                
                excel_path = os.path.splitext(file_path)[0] + '.xlsx'
                df.to_excel(excel_path, index=False)
                
                return send_file(excel_path, as_attachment=True)
            else:
                return 'No tables found in HTML file'
        
        except Exception as e:
            return f'Error processing file: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
