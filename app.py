from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = "chave de desencriptar"
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

api = Api(app)


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
    #! Toda vez que escrevemos [from app import *] o python roda [app.py]
    #! Isso faz com que só o arquivo que contém o código [__main__] consiga rodar ele
    #! Se n tivesse isso toda vez que importarmos algo daqui o [app.run()] rodaria - bugando tudo e criando circular import error



# pega as [id] da table [users] => SELECT [id] FROM [users] 
# pega todas as colunas da table [users] => SELECT [*] FROM [users]
# pega todas as colunas da table [items] onde [name] vai ser igual a variável ? => SELECT [*] FROM [items] WHERE [name]=?
# se já n existir, cria a tabela [users] com as colunas: [id](index), [username](string) e [password](string) => CREATE TABLE IF NOT EXISTS [users] ([id] INTEGER PRIMARY KEY, [username] text, [password] text)
# põe 3 variáveis na table [users] => INSERT INTO users VALUES (?, ?, ?)
# da um update no parametro [price] do item que tiver [name] igual a variável ? => UPDATE items SET price=? WHERE name=?

#/***************************************************************************************************

# # 201 -> Item created
# # 200 -> Deu tudo certo
# # 400 -> Sintaxe inválida (user mandou request errada)
# # 403 -> Vc não é autorizado a acessar isso
# # 404 -> Não encontrado
# # 500 -> Server deu erro
