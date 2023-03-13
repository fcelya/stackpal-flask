from app import app, utils

if __name__ == "__main__":
    utils.load_env()
    app.run(host="0.0.0.0",debug=False,port=5000)