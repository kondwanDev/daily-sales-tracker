# Requirements Document

## 1. User

The primary user of the system is a shopkeeper who records daily sales and manages shop activities.

---

# User Requirements

The system should allow the shopkeeper to:

- Record sales digitally instead of using paper.
- Record the products sold.
- Record the quantity sold.
- Record the actual selling price of each item.
- View the total sales amount for a selected day.
- View previous sales records.
- Reduce mistakes caused by manual recording and calculations.

---

# Functional Requirements

## Sales Management

The system shall:

- Allow users to create a new sale.
- Allow users to add multiple products to one sale.
- Store the quantity of each product sold.
- Store the actual selling price at the time of sale.
- Calculate the total amount automatically.

## Sales Pricing

The system shall:

- Allow the user to enter the actual selling price during each sale.
- Not assume that products always have a fixed selling price.
- Preserve the selling price used at the time of the transaction.

## Product Management

The system shall:

- Allow users to add products.
- Allow users to view available products.
- Allow users to update product information.

## Reports

The system shall:

- Display daily sales totals.
- Display sales history.
- Allow users to search sales by date.

---

# Product and Pricing Requirements

The system shall:

- Allow products to have a default/reference price.
- Allow the shop operator to view the default price when recording a sale.
- Allow the operator to enter the actual selling price during each transaction.
- Store the actual selling price separately from the default product price.
- Preserve historical selling prices even if the default product price changes in the future.

Example:

Product:
T-shirt

Default price:
MWK 8,000

Customer negotiated price:
MWK 7,000

The system should store the selling price of MWK 7,000 for that specific sale while keeping the default price of MWK 8,000.

---

# User Roles and Permissions (Future)

The system may support different users in future versions.

## Shop Owner

Possible responsibilities:

- Add new products.
- Set and update default prices.
- View sales reports.
- Verify daily sales.
- Manage shop operators.

## Shop Operator

Possible responsibilities:

- Record sales.
- Search and select products.
- View product information.
- Complete daily sales activities.

---

# Data Integrity Requirements

The system should:

- Maintain accurate sales records.
- Store the user responsible for creating sales.
- Preserve sales history.
- Prevent unauthorized modification of important records.

# Non-Functional Requirements

The system should:

- Be simple and easy for shopkeepers to use.
- Store data securely.
- Provide fast responses.
- Prevent unauthorized access.

# additional stuff

- No customer required for normal sales.
- Customer data only for future installment/layby.
- Product prices are not fixed.
- Sales store actual selling prices

The system should allow the shop operator to search and select products quickly when recording sales.

# Future User Roles

## Shop Owner

The shop owner may be added as a user in future versions.

Possible abilities:

- View all sales records.
- Verify daily sales.
- Monitor shop performance.
- View reports.
- Manage shop operators.

## Sales Pricing Rules

The system should allow the same product to appear multiple times in one sale when the items have different selling prices due to bargaining.