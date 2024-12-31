from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from config import *
from flask_cors import CORS
import requests
import base64
import os
import logging
import json
from s3_utils import S3Manager


# 로깅 설정
logging.basicConfig(level=logging.DEBUG)

# 디렉토리 경로 설정
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
logging.debug(f"Project root: {project_root}")

app.config['SESSION_TYPE'] = 'filesystem'
app.config['VIDEO_PATH'] = VIDEO_PATH
Session(app)

# S3
s3_manager = S3Manager(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME)

app.secret_key = 'your_secret_key'  # 세션을 위한 비밀 키 설정
CORS(app, supports_credentials=True) # CORS 설정
app.secret_key = SECRET_KEY

# static/assets/boxedImg 폴더 경로 설정
BOXED_IMG_DIR = os.path.join(project_root, 'static', 'assets', 'YOLO')
os.makedirs(BOXED_IMG_DIR, exist_ok=True)

# 렌더링
@app.route('/')
def index():
    return render_template('broadcast/tv_broadcast.html', api_server_url=API_SERVER_URL, video_path=app.config['VIDEO_PATH'])

# 방송 캡처 원본 이미지 전송
@app.route('/process_image', methods=['POST'])
def process_image():
    logging.debug(f"API Server URL: {API_SERVER_URL}")  # API 서버 URL 로깅
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:    
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(f"{API_SERVER_URL}/detect/person/", files=files)
        
        if response.status_code == 200:
            result = response.json()
            session['boxes'] = result['boxes']  # 박스 정보를 세션에 저장

            img_data = base64.b64decode(result["annotated_image"])
            img_filename = f"boxed_{file.filename}"
            img_path = os.path.join(BOXED_IMG_DIR, img_filename)
            
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
            
            return jsonify({
                "message": result["message"],
                "annotated_image": result["annotated_image"],
                "image_format": result["image_format"],
                "boxes": result["boxes"]
            })
        else:
            return jsonify({"error": "API server error"}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500



# 선택 객체의 박스 정보 송신 #FastAPI 서버로부터 받은 응답을 그대로 클라이언트에 전달
@app.route('/get_box_coordinates', methods=['POST'])
def get_box_coordinates():
    data = request.json
    button_number = data['button_number']
    boxes = session.get('boxes', [])
    
    logging.debug(f"Button number: {button_number}")
    logging.debug(f"Boxes in session: {boxes}")
    
    if not boxes:
        return jsonify({"error": "No box information available"}), 400
    
    if 0 <= button_number < len(boxes):
        coordinates = boxes[button_number]['coordinates']
        try:
            # 가장 최근에 저장된 boxed 이미지 파일을 찾습니다.
            boxed_files = [f for f in os.listdir(BOXED_IMG_DIR) if f.startswith('boxed_')]
            if not boxed_files:
                return jsonify({"error": "No boxed image found"}), 404
            latest_boxed_file = max(boxed_files, key=lambda f: os.path.getmtime(os.path.join(BOXED_IMG_DIR, f)))
            file_path = os.path.join(BOXED_IMG_DIR, latest_boxed_file)
            
            logging.debug(f"File path: {file_path}")
            if os.path.exists(file_path):
                with open(file_path, 'rb') as image_file:
                    files = {'file': (latest_boxed_file, image_file, 'image/jpeg')}
                    data = {'person_box': json.dumps(coordinates)}
                    logging.debug(f"Sending request to FastAPI: {API_SERVER_URL}/detect-and-search/")
                    response = requests.post(f"{API_SERVER_URL}/detect-and-search/", files=files, data=data)
                    logging.debug(f"FastAPI response status: {response.status_code}")
                    # logging.debug(f"FastAPI response content: {response.text}")
                if response.status_code == 200:
                    api_response = response.json()

                    # 제품 정보에 이미지 URL 추가
                    for product in api_response['products']:
                        product['mainImageURL'] = None
                        product['additionalImagesURL'] = []

                        for image in product['images']:
                            image_url = s3_manager.get_image_url(image)
                            # 이미지 파일명에서 제품 ID와 이미지 번호 추출
                            filename = image.split('/')[-1]
                            product_id, image_number = filename.split('_')


                            if image_number.startswith('0'):
                                product['mainImageURL'] = image_url
                            else:
                                product['additionalImagesURL'].append(image_url)
                        
                        # 메인 이미지가 없는 경우 첫 번째 추가 이미지를 메인으로 설정
                        if not product['mainImageURL'] and product['additionalImagesURL']:
                            product['mainImageURL'] = product['additionalImagesURL'].pop(0)

                        # 기존의 'imageUrl' 키 유지 (첫 번째 이미지 URL)
                        product['imageUrl'] = product['mainImageURL'] or (product['additionalImagesURL'][0] if product['additionalImages'] else None) 

                    return jsonify(api_response)
                
                else:
                    logging.error(f"API server error: {response.status_code}, Content: {response.text}")
                    return jsonify({"error": f"API server error: {response.text}"}), response.status_code
            else:
                logging.error(f"File not found: {file_path}")
                return jsonify({"error": "Image file not found"}), 404
        except requests.RequestException as e:
            logging.error(f"Request exception: {str(e)}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid button number"}), 400



@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('404 error: %s', str(error))
    return jsonify(error="404 Not Found"), 404

app.logger.setLevel(logging.DEBUG)


# 홈쇼핑 화면 전환 render
@app.route('/recommended_clothing')
def recommended_clothing():
    button_number = request.args.get('number')
    return render_template('homeshop/recommended_clothing.html', button_number=button_number, video_path=app.config['VIDEO_PATH'])


@app.route('/detail')
def detail():
    product_id = request.args.get('id')
    return render_template('homeshop/detail.html', product_id=product_id)



if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=5000) # 로컬 네트워크의 다른 기기에서 접근 가능
    # 127.0.0.1은 로컬 머신에서만 접근 가능

