from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Sample data for food items
food_items = [
    {"id": 1, "name": "Nasi Goreng", "category": "Main Course", "price": 25000, "size": ["Small", "Medium", "Large"], "ingredients": ["Rice", "Egg", "Vegetables"], "spicy_level": "Medium"},
    {"id": 2, "name": "Mie Goreng", "category": "Main Course", "price": 20000, "size": ["Small", "Medium", "Large"], "ingredients": ["Noodles", "Egg", "Vegetables"], "spicy_level": "High"},
    {"id": 3, "name": "Sate Ayam", "category": "Snack", "price": 15000, "size": ["Small", "Medium"], "ingredients": ["Chicken", "Peanut Sauce"], "spicy_level": "Mild"},
    {"id": 4, "name": "Bakso", "category": "Main Course", "price": 22000, "size": ["Small", "Medium", "Large"], "ingredients": ["Meatballs", "Noodles"], "spicy_level": "Low"},
    {"id": 5, "name": "Soto Ayam", "category": "Main Course", "price": 25000, "size": ["Small", "Medium", "Large"], "ingredients": ["Chicken", "Broth", "Vegetables"], "spicy_level": "Low"},
    {"id": 6, "name": "Gado-Gado", "category": "Vegetarian", "price": 18000, "size": ["Small", "Medium"], "ingredients": ["Vegetables", "Peanut Sauce"], "spicy_level": "None"},
    {"id": 7, "name": "Pecel Lele", "category": "Main Course", "price": 27000, "size": ["Small", "Medium"], "ingredients": ["Catfish", "Chili Sauce"], "spicy_level": "Medium"},
    {"id": 8, "name": "Nasi Padang", "category": "Main Course", "price": 30000, "size": ["Medium", "Large"], "ingredients": ["Rice", "Beef Rendang", "Vegetables"], "spicy_level": "High"},
    {"id": 9, "name": "Ayam Geprek", "category": "Main Course", "price": 23000, "size": ["Small", "Medium"], "ingredients": ["Chicken", "Chili Sauce"], "spicy_level": "Very High"},
    {"id": 10, "name": "Es Teler", "category": "Dessert", "price": 15000, "size": ["One Size"], "ingredients": ["Coconut", "Jackfruit", "Avocado"], "spicy_level": "None"},
    {"id": 11, "name": "Rendang", "category": "Main Course", "price": 32000, "size": ["Medium", "Large"], "ingredients": ["Beef", "Spices"], "spicy_level": "High"},
    {"id": 12, "name": "Pempek", "category": "Snack", "price": 12000, "size": ["Small", "Medium"], "ingredients": ["Fish", "Cuka Sauce"], "spicy_level": "Mild"},
    {"id": 13, "name": "Martabak", "category": "Snack", "price": 25000, "size": ["Small", "Medium", "Large"], "ingredients": ["Flour", "Egg", "Vegetables"], "spicy_level": "None"},
    {"id": 14, "name": "Tahu Goreng", "category": "Snack", "price": 10000, "size": ["One Size"], "ingredients": ["Tofu"], "spicy_level": "Low"},
    {"id": 15, "name": "Kerak Telor", "category": "Snack", "price": 20000, "size": ["One Size"], "ingredients": ["Egg", "Rice", "Spices"], "spicy_level": "Mild"}
]

# Helper function to get a new ID
def get_new_id():
    if food_items:
        return max(item["id"] for item in food_items) + 1
    return 1

# Food list endpoint with Create option
class FoodList(Resource):
    def get(self):
        return {"error": False, "message": "success", "count": len(food_items), "items": food_items}
    
    def post(self):
        data = request.json
        new_id = get_new_id()
        
        new_item = {
            "id": new_id,
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "size": data.get("size", ["One Size"]),
            "ingredients": data.get("ingredients", []),
            "spicy_level": data.get("spicy_level", "None")
        }
        food_items.append(new_item)
        
        return {"error": False, "message": "Item created successfully", "item": new_item}, 201

# Food detail endpoint with Read, Update, and Delete options
class FoodDetail(Resource):
    def get(self, item_id):
        item = next((item for item in food_items if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Item not found"}, 404
        return {"error": False, "message": "success", "item": item}
    
    def put(self, item_id):
        data = request.json
        item = next((item for item in food_items if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Item not found"}, 404
        
        # Update item data
        item.update({
            "name": data.get("name", item["name"]),
            "category": data.get("category", item["category"]),
            "price": data.get("price", item["price"]),
            "size": data.get("size", item["size"]),
            "ingredients": data.get("ingredients", item["ingredients"]),
            "spicy_level": data.get("spicy_level", item["spicy_level"])
        })
        
        return {"error": False, "message": "Item updated successfully", "item": item}
    
    def delete(self, item_id):
        global food_items
        food_items = [item for item in food_items if item["id"] != item_id]
        
        return {"error": False, "message": "Item deleted successfully"}

# Registering resources with endpoints
api.add_resource(FoodList, "/food")
api.add_resource(FoodDetail, "/food/<int:item_id>")

if __name__ == "__main__":
    app.run(debug=True)
