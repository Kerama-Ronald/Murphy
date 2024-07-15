from flask import Blueprint, request, jsonify
from models.models import User, AuctionItem, Bid
from db.database import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@main_bp.route('/auction-items', methods=['POST'])
def create_auction_item():
    data = request.get_json()
    new_item = AuctionItem(
        title=data['title'],
        description=data['description'],
        starting_price=data['starting_price'],
        current_price=data['starting_price']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Auction item created successfully'}), 201

@main_bp.route('/bids', methods=['POST'])
def create_bid():
    data = request.get_json()
    auction_item = AuctionItem.query.get(data['auction_item_id'])
    if not auction_item:
        return jsonify({'message': 'Auction item not found'}), 404
    new_bid = Bid(
        amount=data['amount'],
        user_id=data['user_id'],
        auction_item_id=data['auction_item_id']
    )
    auction_item.current_price = data['amount']
    db.session.add(new_bid)
    db.session.commit()
    return jsonify({'message': 'Bid placed successfully'}), 201

@main_bp.route('/auction-items/<int:item_id>', methods=['GET'])
def get_auction_item(item_id):
    auction_item = AuctionItem.query.get_or_404(item_id)
    return jsonify({
        'id': auction_item.id,
        'title': auction_item.title,
        'description': auction_item.description,
        'starting_price': auction_item.starting_price,
        'current_price': auction_item.current_price
    })

@main_bp.route('/users/<int:user_id>/bids', methods=['GET'])
def get_user_bids(user_id):
    user = User.query.get_or_404(user_id)
    bids = [{'id': bid.id, 'amount': bid.amount, 'auction_item_id': bid.auction_item_id} for bid in user.bids]
    return jsonify(bids)
