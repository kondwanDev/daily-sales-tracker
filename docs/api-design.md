# API Design

## Overview

This document describes the REST API for the Daily Sales Tracker system.

The API enables authenticated users to manage products, record sales, and generate sales reports.

All endpoints return JSON responses.

---

# Authentication

## Login

**POST** `/login`

Authenticates a user and returns an access token.

Example Request

```json
{
  "username": "john",
  "password": "password123"
}
```

Example Response

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

# Products

## Get All Products

**GET** `/products`

Returns all products.

---

## Get Product

**GET** `/products/{id}`

Returns details for a single product.

---

## Create Product

**POST** `/products`

Creates a new product.

Example Request

```json
{
  "name": "T-shirt",
  "category": "Clothes",
  "default_price": 8000
}
```

---

## Update Product

**PUT** `/products/{id}`

Updates product information.

---

## Delete Product

**DELETE** `/products/{id}`

Removes a product from the system.

> Note: This endpoint may later be replaced with a soft delete if products should be preserved for historical reporting.

---

# Sales

## Create Sale

**POST** `/sales`

Creates a new sale containing one or more products.

Example Request

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 1,
      "selling_price": 7000
    },
    {
      "product_id": 2,
      "quantity": 2,
      "selling_price": 1800
    }
  ]
}
```

The backend automatically:

* Creates the sale.
* Stores all sale items.
* Calculates the total amount.
* Saves the transaction.

---

## Get Sale

**GET** `/sales/{id}`

Returns the details of a single sale.

---

## Get Sales History

**GET** `/sales`

Returns all recorded sales.

Optional filters may include:

* Date
* Operator
* Date range

---

# Reports

## Daily Sales Summary

**GET** `/reports/daily`

Returns:

* Number of sales
* Total revenue
* Products sold

---

## Product Sales Report

**GET** `/reports/products`

Returns sales grouped by product.

---

# Response Status Codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Resource created      |
| 400  | Bad request           |
| 401  | Unauthorized          |
| 404  | Resource not found    |
| 500  | Internal server error |

---

# Future Endpoints

The following endpoints may be introduced in future versions:

* Customer management
* Inventory management
* Stock adjustments
* Expenses
* Installment payments
* Audit logs
* Owner dashboard
* Sales verification
