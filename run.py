# from application import create_app

# app, jwt = create_app()
# def main():
#     app.run(debug=True, port=9098, host="localhost")

# if __name__ == '__main__':
#     main()



# class User():
#     def __init__(self, name, username):
#         self.name = name
#         self.username = username
#     def __init__(self, name):
#         self.name = name
#         self.username = "NONE"
#     # def __init__(self, username):
#     #     self.name = "NONE"
#     #     self.username = username

import json

def add_element(j, name, value):
    j[name] = value

j1 = json.loads(
"""
{
"username": "jhon"
}
""")

print(j1)
add_element(j1, "name", "jhonatan")
print(j1)
