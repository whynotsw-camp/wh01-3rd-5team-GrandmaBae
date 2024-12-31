import os
from flask import Flask, render_template, send_from_directory, request

# Flask 애플리케이션
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

# 정적 파일 처리
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# 홈 경로 (main1.html 렌더링)
@app.route('/')
def home():
    return render_template("homeshop/main1.html")

# 상품 상세 페이지 경로
@app.route('/clothes')
def clothes():
    # URL 쿼리 매개변수에서 상품 정보 받기
    product_name = request.args.get('name', '상품 이름 없음')
    product_price = request.args.get('price', '가격 정보 없음')
    product_image = request.args.get('image', '이미지 없음')

    # clothes.html로 상품 정보 전달
    return render_template(
        'homeshop/clothes.html',
        name=product_name,
        price=product_price,
        image=product_image
    )

# Flask 앱 실행
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5020, debug=True)
