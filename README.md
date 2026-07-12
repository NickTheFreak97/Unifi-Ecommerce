# Unifi-Ecommerce

## Required fields :

- **Name**: Niccolò Della Rocca
- **Chosen Project Type**: Rest API track: E-Commerce API
- **Test database**: Provided as dump.sql. It comes from PostgreSQL 16 image

    It can be imported in any PostgreSQL instance via this command:
    
    `cat dump.sql | docker exec -i <container_name> psql -U <username> <database_name>`
- **Framework**: Django `rest_framework` with `simplejwt` authentication.
- **Demo accounts**:
    - `username`: johnny | `password`: amosololuca | `role`: customer
    - `username`: lorenzo | `password`: amosololuca | `role`: shop staff
- **online deployment link**:
  -  https://d1079g0dt2da6g.cloudfront.net/ to reach Amazon ECS `web` service via `https`. This is what I use in production as base_url for API.
  - `unifi-ecommerce-alb-1340937549.eu-north-1.elb.amazonaws.com` to reach Amazon EC2 ALB via `http`
  - `unifi-ecommerce-db.chwqs0ukeab3.eu-north-1.rds.amazonaws.com` to reach Amazon RDS hosting PostgreSQL instance
  - `unifi-ecommerce-redis-2.vpw7iq.ng.0001.eun1.cache.amazonaws.com:6379` to reach Amazon Elasticache instance, used as `Celery` broker, tasks beat, and to handle guest flows
  - https://main.dpgvn15ormsvm.amplifyapp.com/ to reach "minimal" front-end and testing. 
- **Documentation**: For most endpoints, my minimal client both serves as a test and as a documentation. As a backup, I also included `drf_spectacular` that auto-generates from code the `OpenAPI 3.0` specification for detected endpoints. I'm so sorry that I didn't manage to document everything, it's just that I work 8 hours shifts and I didn't manage to cover this :( 

## Requirements
This repo runs on `Django 6.0.4` which requires `Python >= 3.12`.
I decided to use `PostgreSQL` as DBMS since I got familiar with it during the Basi di Dati class. Be aware that `pgadmin` image requires PostgreSQL driver to be installed 
because during the setup process it builds from source. If you're on MacOS and don't have it already, and if `brew` is installed, you can get it by running in cli:

```commandline
brew install postgresql
```

## Project
The ecommerce is organized in `Categories`, and every `Category` contains a set of `Product`s. Each product can have `ProductVariant`s, which is where the data such as `stock`, `price`, `currency`, and all of that are placed. 

When a `Product` is created, a base `ProductVariant` referencing such product is created. 

There are two kind of users: `customer`, who can view categories, products, create carts and orders, and `staff` members, who can CRUD categories and products, orders, payment methods and so on.

As a defensive mechanic, deletion is implemented as a soft delete: a `time_of_deletion` field exists on `Product`s, initially `null`. Whem a shop owner wants to delete a `Product` can either set this field to `timezone.now()` or schedule for future deletion.

Queries that browse `Product`s all check that `time_of_deletion < timezone.now()` at the time of querying, so that deletion is effective.

A `customer` can add `ProductVariant`s to cart, increment or decrement their amount, and delete from cart as well. A customer can either be a logged in user (any role is OK), or be a guest. Cart creation is protected by a middleware that, if 
no authentication is detected, creates a new request cookie named `guest_token` that can be used to process the guest user flows. This way, all `Order` and `Cart` endpoint can keep track of the `User`'s identity. 

Authenticated `User`s generate `Cart`s as database records, while `guest` users generate carts as a Redis Hash. 

There are two ways to generate a new `Order`:
- Via `Cart`: In this case the user identity is used to retreive `Cart`. Items in cart are then cloned as `OrderItem` so protect stored records from being affected by `Product` deletion, `price` change, and other events that can impact the `Product`'s identity.
- Via a set of (`ProductVariant.barcode`, `quantity`) tuples, in which case `Cart` didn't exist yet and is created on the moment based on the request body.

When a new order is created, in both cases, a few things happen:

- A check is performed to validate barcodes to existing, non-deleted `ProductVariant`s.
- A check is performed to assert that the order amount isn't bigger than the available stock
- A task is created that after long enough time, checks if the `Order` is "stale" with respect to a criterion based on status, and, if it is, the order is cancelled, and the stock is released.

When a new order is created, the client generates an idempotency key, an `UUIDv4` to prevent duplicate payment attempts.
Django exposes `/payment/stripe/intent/create/` to create an intent. Because I lacked time due to my work shifts, I deviated from my initial design choice,
and integrated `Stripe` to delegate payment processing. Such endpoint uses a secret key to create an intent, and also exposes `webhooks` that `Stripe` uses to automatically
report payment results. When this point is hit, a new `PaymentIntent` instance is created, representing an attempt to pay by the user. I limited the supported methods to `card` only despite initial design due to lack of time.
When /payment/stripe/webhook/ reports `stripe.Webhook.construct_event(payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET')["type"] == "payment_intent.succeeded"`
, a `Payment` instance is created representing the effective settlement of the payment.

When a new user is registered, if `Order`s existed with the same `email` of the created `User`, a merge is performed so that they can see it when querying orders by email or identity.

## Running
Get the server up and running for the first time (after cloning repo, creating virtual environment with Python 3.13.5):


```
docker-compose --env-file .env.dev up --build
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



## Testing payments

### Stripe
Stripe uses the following conventions for testing:

Card number: 
- 4242 4242 4242 4242 --> Successful payment
- 4000 0000 0000 0002 --> Generic decline
- 4000 0000 0000 9995 --> Insufficient funds
- 4000 0000 0000 9987 --> Lost card
- 4000 0000 0000 9979 --> Stolen card
- 4000 0000 0000 0069 --> Expired card
- 4000 0000 0000 0127 --> CVC error

Combine any of the following with: any 3 digits CVC, future expiry date, any Zip code.

## Import dump:
Run the following command:

`docker exec unifi-ecommerce-db-1 pg_dump -U admin unifi_db > dump.sql`
