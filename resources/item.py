from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        request_data = parse_request(["price", float, True], ["store_id", int, True])
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}
        else:
            return {"message": "This item doesn't exist"}
            

    def put(self, name):
        request_data = parse_request(["price", float, True], ["store_id", int, True])

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price =  request_data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


def match_name(name, iterable):
    return next(filter(lambda x: x["name"] == name, iterable), None)


def parse_request(*list_of_args):
    parser = reqparse.RequestParser()
    for arg in list_of_args:
        parser.add_argument(arg[0],  # ! todo request que não for [arg[0]] vai ser descartado
                            type=arg[1],  # ! [arg[0]] tem que ser float
                            required=arg[2],  # ! Tu nao pode deixar de por um [arg[0]]
                            help="{} cannot be left blank".format(arg[0]) if (arg[2] == True) else None,  # ! msg se tu deixar de por [arg[0]]
                            )
    return parser.parse_args()
