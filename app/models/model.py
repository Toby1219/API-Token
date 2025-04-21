from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    discount_percentage = db.Column(db.Float)
    rating = db.Column(db.Float)
    stock = db.Column(db.Integer)
    sku = db.Column(db.String(50))
    weight = db.Column(db.Float)
    warranty_information = db.Column(db.String(200))
    shipping_information = db.Column(db.String(200))
    availability_status = db.Column(db.String(50))
    return_policy = db.Column(db.String(200))
    minimum_order_quantity = db.Column(db.Integer)
    thumbnail = db.Column(db.String(255))
    
    dimensions = db.relationship("Dimension", backref="product", uselist=False)
    meta = db.relationship("Meta", backref="product", uselist=False)
    reviews = db.relationship("Review", backref="product", lazy=True)
    images = db.relationship("Image", backref="product", lazy=True)
    tags = db.relationship("Tag", backref="product", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "discount_percentage": self.discount_percentage,
            "rating": self.rating,
            "stock": self.stock,
            "sku": self.sku,
            "weight": self.weight,
            "warranty_information": self.warranty_information,
            "shipping_information": self.shipping_information,
            "availability_status": self.availability_status,
            "return_policy": self.return_policy,
            "minimum_order_quantity": self.minimum_order_quantity,
            "thumbnail": self.thumbnail,
            
            "dimensions": {
                "width": self.dimensions.width,
                "height": self.dimensions.height,
                "depth": self.dimensions.depth
            } if self.dimensions else None,

            "meta": {
                "createdAt": self.meta.createdAt,
                "updatedAt": self.meta.updatedAt,
                "barcode": self.meta.barcode,
                "qrCode": self.meta.qrCode
            } if self.meta else None,

            "reviews": [
                {
                    "rating": r.rating,
                    "comment": r.comment,
                    "date": r.date,
                    "reviewerName": r.reviewerName,
                    "reviewerEmail": r.reviewerEmail
                } for r in self.reviews
            ],

            "images": [i.url for i in self.images],
            "tags": [t.name for t in self.tags]
        }

class Dimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    depth = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.String(100))
    updatedAt = db.Column(db.String(100))
    barcode = db.Column(db.String(50))
    qrCode = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    comment = db.Column(db.Text)
    date = db.Column(db.String(100))
    reviewerName = db.Column(db.String(100))
    reviewerEmail = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="guest")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            raise ValueError("Password hash is not set for this user.")
        return check_password_hash(self.password_hash, password)


class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token =  db.Column(db.String(2500), unique=True, nullable=False)
    refresh_token = db.Column(db.String(2500), unique=True, nullable=False)
    issued_date = db.Column(db.String(2500), unique=True, nullable=False)
    expire_date = db.Column(db.String(2500), unique=True, nullable=False)


class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti =  db.Column(db.String(), nullable=True)
    created_at = db.Column(db.String(), default=datetime.now())
    
    def __repr__(self):
        return f'<TOKEN> {self.jti}'