from db.database import db

class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = (
    db.UniqueConstraint("name", "category_id", name="uq_product_name_category"),
)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category_id": self.category_id,
            "category": self.category.name if self.category else None
        }