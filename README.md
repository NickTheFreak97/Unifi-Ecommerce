# Unifi-Ecommerce

## User perspective
A user can browse products. The home page of the shop shows a list of recommended, on sale, for you products, possibly organized by category. 

A **Product** has an ID (SKU), a name, a description, an image, an availability, a users rating, a datasheet. A **Category** is the abstraction used to organize *products* into intuitive, semantically related groups. The purpose of *Category* existing is to help the user navigate to its goal efficiently. A **Category** as a unique name, possibly a position value, and is associated with a list of *products*, where a *product* can be listed under a single category for the sake of simplicity. 

The user can also browse for products via a searchbar. Search results show relevant products grouped by category, and sorted by relevance, lower price, higher price. Unavailable items can either be hidden or shown at the end of the list. Optionally allow the user to be notified by email when the items is available again.

One or more currently available products can be added to a **Cart**. A *cart* has a unique identifier, and is tied to the identity of the user. The user can add/remove *products* from the cart, and can increase/decrease their amount (within availability). When the user is satisfied, they can turn the cart into an **order**. Here two paths are possible:

1. The user is not logged in.
2. The user is logged in.

In the scenario (1), when the user is not logged in, an anonymous identity is created and associated with the cart. In the scenario (2), the cart is associated with the user unique identifier. Ideally, if a user decides to log in, the cart should be moved to be associated with the authenticated identity, without the user needing to populate it from scratch. 

An *order* has a *cart*, a *billing address*, a *shipping address* (optionally matching the *billing* one), *shipping method*, *payment method* and an *identity* associated with it. An order also crosses multiple states. For example: pending → confirmed → shipped → delivered → cancelled. The user has two options.

1. Complete the order (!! still can be canceled later).
2. Abandon the transaction.

- In the scenario (1), the order has been paid and the payment confirmed. The user is presented with a confirmation screen. They see a unique order ID that they can use for reference in case they completed the order anonymously. and a recap of the order. The user possibly received an email confirmation with an invoice of the purchase. 

- In the scenario (2), we can set up an automated email system to try to get the user to complete the purchase (-> there must be a way to unsubscribe by law).

A user can open a **dispute** for an *order*. A *dispute* has a *date*, a *description*, a *state*. A *dispute* crosses states open → refunded, or open → denied. When a *dispute* is completed successfully, a fraction (<= 1) of the paid amount for the order it's associated with it is refunded via the payment processor. When a *dispute* is closed for an order, a new one can't be opened. 

The *user* has a dashboard, that they can use to view their *orders* history, sorted by *recents*. When an *order* is selected, a recap is shown along with few options: *cancel* the *order* (if not shipped yet), *open* a *dispute* (if order is received), *write a review*, *receive support* about the *order*. 

## Admin perspective
An admin panel can be used to create a new *category*, *edit* or *delete* an existing one. The admin can *create*, *update*, *delete* existing *product*s, and can *manage* orders. 

*Managing* an *order* means that they can *cancel* one (issuing a refund), with a *reason*, *update* the current state of the *order*, *mark as shipped*.  

An admin can *inspect* analytics about the platform. For each *product*, the price changes in a set interval of time, return rate, purchases trends, and more.


## Running
Get the server up and running for the first time:

```
docker-compose up --build
```

Move from terminal in the root of this project then run the following command:

```
docker compose --env-file .env.dev up -d
```

From this moment, you will be able to access `web` at port  `:8000`, `pgAdmin` at port `:5050`, `redis` cache at port `:6379`.

To perform migrations (must execute at least the first time after you compose):

```
docker compose exec web python manage.py migrate
```

If hot reload seems broken for some service, you can try

```
docker compose build --no-cache <service_name>
```

## Inspect database

To inspect the database content, connect to `localhost:5050` and register a new server with the following parameters:

- Host name: `db` (or whatever is the registered service name in `docker.compose.yml`)
- Port: `5432` (or the port specified under `db` in `docker.compose.yml`)
- Maintenance database: `unifi_db` (or the value specified in `.env.dev` under `POSTGRES_DB`)
- Username and Password: specified in `.env.dev` under `POSTGRES_USER` / `POSTGRES_PASSWORD`

