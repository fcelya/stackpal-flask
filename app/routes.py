from app import app

@app.route('/api/optimizer')
def optimizer():
    return "Hello, World!"