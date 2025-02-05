from decimal import Decimal
from books.models import Book

class Cart:
    def __init__(self, request):
        """Initialize the cart session"""
        self.session = request.session
        self.cart = self.session.get("cart", {})
        self.session["cart"] = self.cart

    def add(self, book, quantity=1, update_quantity=False):
        """Add or update a book in the cart"""
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {"quantity": 0, "price": float(book.price)}
        
        if update_quantity:
            self.cart[book_id]["quantity"] = max(1, quantity)  # Ensure at least 1
        else:
            self.cart[book_id]["quantity"] += quantity

        self.save()

    def remove(self, book):
        """Remove a book from the cart"""
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def save(self):
        """Mark the session as modified to save changes"""
        self.session.modified = True

    def __iter__(self):
        """Yield cart items with book details"""
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)  # Fetch all books in cart
        book_map = {str(book.id): book for book in books}  # Map book ID to book

        for book_id, item in self.cart.items():
            book = book_map.get(book_id)
            if book:
                yield {
                    "book": {
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "cover_image": book.cover_image
                    },
                    "price": Decimal(str(item["price"])),
                    "quantity": item["quantity"],
                    "total_price": Decimal(str(item["price"])) * item["quantity"]
                }

    def get_total_price(self):
        """Calculate total cart price"""
        total =  sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
        return Decimal(total).quantize(Decimal("0.01"))

    def clear(self):
        """Clear the cart session"""
        self.session["cart"] = {}
        self.save()
