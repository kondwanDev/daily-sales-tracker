# Database Design

## Overview

The Daily Sales Tracker system uses a relational database to store users, products, sales transactions, and sale details.

The database design is based on the real workflow of the shop:

1. Products are registered in the system.
2. The shop operator records customer purchases.
3. Each sale can contain multiple products.
4. The actual negotiated selling price is stored for each sale.
5. Sales history is preserved for future reporting and verification.

The first version focuses on sales recording and daily balancing. Advanced features such as inventory management, customer credit, and audit tracking will be introduced in future versions.

---

# Database Entities

The main entities in the first version are:

* Users
* Products
* Sales
* Sale Items

---

# Entity Relationship Diagram

```text
              USERS
                |
                |
             creates
                |
                |
              SALES
                |
                |
            contains
                |
                |
          SALE_ITEMS
                |
                |
           references
                |
                |
            PRODUCTS
```

---

# Tables Design

## 1. Users Table

## Purpose

Stores users who can access the system and perform actions.

The table supports authentication and future role-based access control.

Examples of future users:

* Shop operator
* Shop owner

---

## Attributes

| Column        | Description                |
| ------------- | -------------------------- |
| id            | Unique identifier          |
| full_name     | User's real name           |
| username      | Login username             |
| password_hash | Encrypted password         |
| role          | User role (operator/owner) |
| created_at    | Account creation date      |

---

# 2. Products Table

## Purpose

Stores products available in the shop.

Products contain general information and a default/reference price.

The default price helps the shop operator remember normal prices when recording sales.

---

## Attributes

| Column        | Description                    |
| ------------- | ------------------------------ |
| id            | Unique identifier              |
| name          | Product name                   |
| category      | Product category               |
| default_price | Normal/reference selling price |
| created_at    | Date product was added         |

---

## Pricing Rule

The system separates:

### Default Price

The normal expected price decided by the shop owner.

Example:

```
Product:
T-shirt

Default price:
MWK 8000
```

### Selling Price

The actual price agreed with the customer.

Example:

```
Customer negotiated price:
MWK 7000
```

The selling price must not overwrite the default price.

The database stores:

```
products

T-shirt
Default price: 8000
```

and:

```
sale_items

T-shirt
Selling price: 7000
```

This preserves the history of what actually happened.

---

# 3. Sales Table

## Purpose

Represents one customer transaction.

A sale acts like a receipt header containing general transaction information.

---

## Attributes

| Column       | Description                    |
| ------------ | ------------------------------ |
| id           | Unique identifier              |
| user_id      | User who created the sale      |
| total_amount | Total value of the transaction |
| sale_date    | Date and time of sale          |

---

## Example

A customer buys:

```
T-shirt
Plate
Cup
```

The sales table stores:

```
Sale ID:
001

Recorded by:
John

Total:
MWK 12000
```

The individual products are stored in the sale_items table.

---

# 4. Sale Items Table

## Purpose

Stores the products included in a specific sale.

This table connects products and sales while storing transaction-specific information.

---

## Attributes

| Column        | Description                       |
| ------------- | --------------------------------- |
| id            | Unique identifier                 |
| sale_id       | Related sale                      |
| product_id    | Related product                   |
| quantity      | Number of items sold              |
| selling_price | Actual price used during the sale |

---

## Example

Customer purchase:

```
1 T-shirt at MWK 7000
2 Plates at MWK 1500 each
1 Cup at MWK 2000
```

Database:

```
sale_items

sale_id | product_id | quantity | selling_price
------------------------------------------------
1       | T-shirt    | 1        | 7000
1       | Plate      | 2        | 1500
1       | Cup        | 1        | 2000
```

---

# Handling Bargaining

Because customers may negotiate prices, the same product may appear multiple times in one sale.

Example:

A customer buys two T-shirts:

```
T-shirt 1:
MWK 7000

T-shirt 2:
MWK 6500
```

The system stores:

```
sale_items

sale_id | product | quantity | selling_price
---------------------------------------------
1       | T-shirt | 1        | 7000
1       | T-shirt | 1        | 6500
```

This prevents losing important pricing information.

---

# Relationships

## User - Sales

Relationship:

```
One User can create many Sales
```

Database relationship:

```
USERS (1) -------- (Many) SALES
```

Example:

```
Operator John

    |
    +--- Sale 001
    +--- Sale 002
    +--- Sale 003
```

---

## Sales - Sale Items

Relationship:

```
One Sale can contain many Sale Items
```

Database relationship:

```
SALES (1) -------- (Many) SALE_ITEMS
```

Example:

```
Sale 001

- T-shirt
- Plate
- Cup
```

---

## Products - Sale Items

Relationship:

```
One Product can appear in many Sale Items
```

Database relationship:

```
PRODUCTS (1) -------- (Many) SALE_ITEMS
```

Example:

```
T-shirt

Appears in:
Sale 001
Sale 005
Sale 020
```

---

# Important Design Decisions

## 1. Flexible Pricing

The system does not assume products always sell at one fixed price.

The default price is only a reference.

The actual selling price is stored in sale_items.

---

## 2. No Customer Required for Normal Sales

Most shop transactions are completed immediately.

Customer information is not required for normal sales.

Customer management will be introduced later for:

* Layby purchases
* Installment payments
* Credit sales

---

## 3. Inventory Management

Inventory tracking is not included in the first version.

The main goal of the MVP is:

* Record sales.
* Reduce manual balancing work.
* Improve accuracy.

Inventory management will be added as a future feature.

---

## 4. Product Categories

Categories will initially be stored as text.

Example:

```
Clothes
Kitchen
Shoes
```

A separate category table can be introduced if the system grows.

---

## 5. Sales Total

The total amount will be stored in the sales table.

The system will calculate the total automatically from sale items when creating a sale.

Users will not manually enter totals.

---

## 6. Sales Integrity

To improve trust:

* Sales should not be permanently deleted.
* Important actions should be traceable.
* User identity should be linked to sales.

Future versions may include:

* Audit logs.
* Sales approval.
* Owner verification.

---

# Future Tables

The following entities may be added in future versions:

## Inventory

Tracks:

* Available stock.
* Stock additions.
* Stock reductions.

---

## Customers

Used for:

* Layby.
* Credit sales.
* Installment payments.

---

## Payments

Tracks:

* Amount paid.
* Remaining balance.
* Payment history.

---

## Audit Logs

Tracks:

* Changes made by users.
* Deleted or modified records.
* Security events.
