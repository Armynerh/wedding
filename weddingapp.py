from weddingapp import app
if __name__== "__main__":
    app.config.from_pyfile('config.py') 
    app.run(port=9091, debug=True)