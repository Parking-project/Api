from application import create_app

app, jwt = create_app()
def main():
    app.run(debug=True, port=9098, host="localhost")

if __name__ == '__main__':
    main()
