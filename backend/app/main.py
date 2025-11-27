from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # 启用CORS
    CORS(app)
    
    @app.route('/')
    def index():
        return jsonify({
            "message": "115文件整理工具API", 
            "version": "1.0.0",
            "status": "running"
        })
    
    @app.route('/api/health')
    def health():
        return jsonify({"status": "healthy"})
    
    @app.route('/api/test')
    def test():
        return jsonify({"message": "后端服务运行正常"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8947, debug=True)
