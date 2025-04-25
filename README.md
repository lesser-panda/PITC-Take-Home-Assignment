# Zhongyuan's take home assignment for PITC

To build:

`docker build -t pitc_demo .`

To run:

`docker run -p 8000:8000 pitc_demo`

The app can now be accessed at

`localhost:8000`

A demo admin user will be created at startup.
- username: admin
- password: pitc_demo

## User Interface
- A basic frontend (Django Templates) for Customers has been created for customers to create orders and add products/services with their account managers
- Admins, Account Managers and Service Providers will be using the Djang Admin

### Account Manager
1. Log into the Admin interface (localhost:8000/) with an Admin account
2. Create a new User and select "Account Manager" as the role. You now have the first Account Manager!
3. Log into the Admin interface with the new Account Manager account. Account Managers can create Customer accounts in the Admin interface.
4. Create a new User and select "Customer" as the role. You now have the first Customer!
5. Account Managers **can only see their own Customers** in the Admin interface.
6. Create a new Service Provider account in the Admin interface. Similarly, Account Managers **can only see their own Service Providers**
7. Create Products or Services for their Service Providers. Their customers will be able to select these in the Customer Portal (on the frontend, not in Admin)

### Customers
1. Customers can log into the frontend (localhost:8000/) with their account, created by their Account Manager
2. Create order by selecting an Account Manager
3. Add products & services from Service Managers managed by the order's Account Manager. **Customers will NOT see products & services from Service Managers that are not managed by their Account Manager. Doing so will trigger a DB level assertion.**
