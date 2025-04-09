from app import create_app

app = create_app()
app.config['SERVER_NAME'] = 'localhost:5001'  # Force the port

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 