# LittleLemonApi
Welcome to the Little Lemon Restaurant API! This fully functioning API for a restaurant was created as part of a course on backend web development. Developers can use these APIs to develop web and mobile applications for browsing menus, placing orders, managing deliveries, and more.
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Installation

To set up and run the Little Lemon restaurant API project on your local machine, follow these steps:

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```
git clone https://github.com/Expasil/LittleLemonApi.git
```
### 2. Navigate to the Project Directory and install project dependencies
If you don't have pipenv installed, you need to install pipenv using pip:


```
pip install pipenv
```
and then install project dependencies:
```
pipenv install
```

After that use:
```
pipenv shell
```
to inter virtal envirement 

## Usage
### Capabilities
#### Admin
* The admin can assign users to the manager group
* You can access the manager group with an admin token
* The admin can add menu items
* The admin can add categories
#### Manager
* Managers can log in
* Managers can update the item of the day
* Managers can assign users to the delivery crew
* Managers can assign orders to the delivery crew
#### Delivery crew
* The delivery crew can access orders assigned to them
* The delivery crew can update an order as delivered
#### Customer
* Customers can register
* Customers can log in using their username and password and get access tokens
* Customers can browse all categories
* Customers can browse all the menu items at once
* Customers can browse menu items by category
* Customers can paginate menu items
* Customers can sort menu items by price
* Customers can add menu items to the cart
* Customers can access previously added items in the cart
* Customers can place orders
* Customers can browse their own orders

## API Endpoints:

### User Registration and Token Generation Endpoints:

* /api/users 
* /api/users/users/me/  
* /token/login/
  
### Menu Item Endpoints:

* /api/menu-items
* /api/menu-items
* /api/menu-items/{menuItem}
* /api/menu-items/{menuItem}
* /api/menu-items
* /api/menu-items
* /api/menu-items/{menuItem}
* /api/menu-items/{menuItem}
* /api/menu-items/{menuItem}

### User group management endpoints:

* /api/groups/manager/users
* /api/groups/manager/users
* /api/groups/manager/users/{userId}
* /api/groups/delivery-crew/users
* /api/groups/delivery-crew/users
* /api/groups/delivery-crew/users/{userId}

### Cart management endpoints:

* /api/cart/menu-items
* /api/cart/menu-items
* /api/cart/menu-items

### Order management endpoints:

* /api/orders
* /api/orders
* /api/orders/{orderId}
* /api/orders
* /api/orders/{orderId}
* /api/orders/{orderId}
* /api/orders
* /api/orders/{orderId}
