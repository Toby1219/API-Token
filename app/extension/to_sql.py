import json
from ..models.model import db, Product, Dimension, Meta, Review, Image, Tag



def json_to_sql():
    with open('./app/extension/products.json') as f:
        raw_data = json.load(f)
        products = raw_data["products"]

    for item in products:
        existing = Product.query.get(item['id'])
        if not existing:
            product = Product(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                category=item["category"],
                price=item["price"],
                discount_percentage=item["discountPercentage"],
                rating=item["rating"],
                stock=item["stock"],
                sku=item["sku"],
                weight=item["weight"],
                warranty_information=item["warrantyInformation"],
                shipping_information=item["shippingInformation"],
                availability_status=item["availabilityStatus"],
                return_policy=item["returnPolicy"],
                minimum_order_quantity=item["minimumOrderQuantity"],
                thumbnail=item["thumbnail"]
            )

            # Nested: dimensions
            if "dimensions" in item:
                product.dimensions = Dimension(**item["dimensions"])

            # Nested: meta
            if "meta" in item:
                product.meta = Meta(**item["meta"])

            # Nested: reviews
            for rev in item.get("reviews", []):
                product.reviews.append(Review(**rev))

            # Nested: images
            for img in item.get("images", []):
                product.images.append(Image(url=img))

            # Tags
            for tag in item.get("tags", []):
                product.tags.append(Tag(name=tag))

            db.session.add(product)

    db.session.commit()
