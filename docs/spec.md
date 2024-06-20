# SP-ONLINE-SHOP-V+001

## Entity Descriptions

- **Customer**: This entity represents the customers who create an account to place orders on the online shopping platform.
- **Product**: Represents the set of products available for purchase on the platform.
- **Category**: Categories in which the products are grouped.
- **Order**: Product orders placed by customers.
- **Order_Item**: Each item that is part of an order.
- **Payment**: The payment made by the customer once the order is completed.
- **Shipment**: Shipping information associated with an order, including delivery address and tracking information.
- **Cart**: The customer’s virtual basket or shopping cart, which stores items before they are purchased and become part of an order.
- **Wishlist**: Stores items chosen by the customer for possible future purchases.

## Relationships and Dependencies

1. **Customer and Order**
   - **Relationship**: One-to-Many
   - **Description**: A customer can place several orders.

2. **Order and Order_Item**
   - **Dependency**: Order_Item is dependent on Order.
   - **Description**: An order can contain one or several items, each of which represents a single product.

3. **Order_Item and Product**
   - **Relationship**: Many-to-One
   - **Description**: Each Order_Item is related to one Product, and a Product can be related to multiple Order_Items.

4. **Order and Payment**
   - **Relationship**: Many-to-One
   - **Description**: An order is associated with one payment, but each payment can include multiple orders.

5. **Order and Shipment**
   - **Relationship**: Many-to-One
   - **Description**: An order is associated with one shipment, but each shipment can include multiple orders.

6. **Product and Category**
   - **Relationship**: One-to-Many
   - **Description**: A product can belong to a single category.

7. **Customer, Cart, and Wishlist**
   - **Dependency**: Cart and Wishlist are dependent on Customer.
   - **Description**: The shopping cart and the wish list are dependent entities of Customer.

8. **Cart and Product**
   - **Relationship**: Many-to-One
   - **Description**: Each instance of Cart is related to a product.

9. **Wishlist and Product**
   - **Relationship**: Many-to-One
   - **Description**: Each instance of Wishlist is related to a product.

## Entity Relationship Summary

- **Customer** ↔️ **Order**: One-to-Many
- **Order** ↔️ **Order_Item**: One-to-Many (dependent)
- **Order_Item** ↔️ **Product**: Many-to-One
- **Order** ↔️ **Payment**: Many-to-One
- **Order** ↔️ **Shipment**: Many-to-One
- **Product** ↔️ **Category**: One-to-Many
- **Customer** ↔️ **Cart**: One-to-Many (dependent)
- **Customer** ↔️ **Wishlist**: One-to-Many (dependent)
- **Cart** ↔️ **Product**: Many-to-One
- **Wishlist** ↔️ **Product**: Many-to-One

## Entity Construction

### Customer

| Attribute       | Type    |
|-----------------|---------|
| customer_id     | integer |
| first_name      | string  |
| last_name       | string  |
| email           | string  |
| password        | string  |
| address         | string  |
| phone_number    | string  |

### Cart

| Attribute       | Type    |
|-----------------|---------|
| cart_id         | integer |
| quantity        | integer |

### Wishlist

| Attribute       | Type    |
|-----------------|---------|
| wishlist_id     | integer |

### Product

| Attribute       | Type    |
|-----------------|---------|
| product_id      | integer |
| SKU             | string  |
| description     | string  |
| price           | decimal |
| stock           | integer |

### Category

| Attribute       | Type    |
|-----------------|---------|
| category_id     | integer |
| name            | string  |

### Order

| Attribute       | Type    |
|-----------------|---------|
| order_id        | integer |
| order_date      | date/time |
| total_price     | decimal |

### Order_Item

| Attribute       | Type    |
|-----------------|---------|
| order_item_id   | integer |
| quantity        | integer |
| price           | decimal |

### Payment

| Attribute       | Type    |
|-----------------|---------|
| payment_id      | integer |
| payment_date    | date    |
| payment_method  | string  |
| amount          | decimal |

### Shipment

| Attribute       | Type    |
|-----------------|---------|
| shipment_id     | integer |
| shipment_date   | date    |
| address         | string  |
| city            | string  |
| state           | string  |
| country         | string  |
| zip_code        | string  |
