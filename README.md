# route5
Distributed Shipping and Address Generation Platform. Highly scalable design repository for cloud and mobile client implementations.

# Current implementation plan

## End user application for usual:

- can register: a unique code5 is generated for him and cannot be changed. Some code5 patterns can be sold. I mean the ones that have a special feature: 0-0-0-0-0, 255-255-255-255-255 and some maybe reserved. A pool of code5 and a promotion code should be managed by the admins and on registration a user that has this promotion code can get the associated code5.

```
After registering user will get random code5 from pull except reserved code5. We can compute entropy and filter out reserved ones as low entropy. If user has promotion code it also count and handled.
```

- can fill profile
- can login and logout
- can create a an address (alias + GPS coordinates) using point on map
- can create a code5 from his current location according to his device
- The two previous one and the two next can be grouped as = can manage shippings: 
-- create a shipping request [The shipping request include shipping private pictures of the content. Only accessible by the user or by the shipper only in the event of a problem and reimbursement is required.]
-- modify the shipping request
-- look for a shipper
-- commit a shipping to a shipper
-- wait for validation from the shipper
-- pay after the validation
-- wait for shipper confirmation
-- able to track a shipping process
-- view the history of his shippings.
-- acknowledge shipping reception so that last shipper can be paid by putting a shipping code that only the sender received at the confirmation of the shipping by the shipper. This is a authentication measure to verify that the package reached a trust person that will give it to the recipient.
-- can see available shippers for order: The list of the shippers may be order by cost or time criteria
-- can choose shippers chains (I don’t know yet how to do it): This is actually not a user function. Look at the previous point for details.
-- can add rating and review for shipper
-- can manage messages with others.

## End user application for a business (or we can call it a developer account - business suits best) A user that can access the:

- can do everything a user can do
-  manage payments for his account.
- Pay for an access to the API:
- can query API to convert a pattern to a 5 numbers
- Can query API to convert 5 numbers to pattern
- Can get all addresses from 5 numbers or pattern
- Can get a specific address by providing associated address.

## End user application for shipper:

- can register
- can fill profile
- can login and logout
- can request certification
- can submit certifications papers
- can check certification process
- can manage shippings:
- create a shipping request (in case user does not have his phone: user have to provide his code5) [The shipping request include shipping private pictures of the content. Only accessible by the user or by the shipper only in the event of a problem and reimbursement is required.]
- wait for user commit (user enter his code5 for verification. Still in the case of user has no phone at that time).
modify the shipping request
- validate a shipping
- wait for user payment
- confirm a shipping and give the reception code to be provided to the receiver for security validation.
- View his shippings (current and history)
- acknowledge a shipping reception so that previous shipper is paid.
- can get address and data from code5:
-- can query API to convert a pattern to a 5 numbers
-- Can query API to convert 5 numbers to pattern
-- Can get all addresses from 5 numbers or pattern
-- Can get a specific address by providing associated address.

```
As an example of a current EC2 test bed for the code5 algo does:
http://52.88.225.214:5000/api/v1/public/uuid/pattern/image/60-71-65-218-253
The code5 pattern image to 5 numbers is still in beta test using scikit-learn so this part will be highly experimental as i am training a model to recognize the pattern as we speak.
can read code5 with reader: This will tap on an endpoint that will do some machine learning and will return a set of match found and the shipper will visually find the one that is correct. To be discussed later. I think that this functionality will take some time to reach maturity and should be iterated: an interface to select each character out of the 256 (the display follow a logic humanly easy).  Then machine learning each pattern part at a time and finally one that take the whole picture.

can answer on review: Can you elaborate on that one. I do not see it clearly.
can add feedback to user: Message i would imagine.
Can manage messages
Can manage payments: Payment for the shipper account, certification process, shipping payment received from the user

End user application for administrator:

can register: Only from the root user can an admin account be created.
can fill profile
can login and logout
can check and verify certification
can moderate users and shippers (maps view to show all shippers and links later on)
can moderate messages (in general) 
can moderate shippings
can produce statistics of users, shippers, shippings and payments.

Billing part
paypall
credit cards with some provider
?


To start I need accounts on: For these no worries.
github with created private repository and then you will add me to it
digitalocean, create instance, and share IP and ssh key with me, for start we need basic plan, more latter, I can help with settings, probably with shared screen if you will have difficulties but it is the easiest cloud
android app developer account (may be latter)
ios developer account  (may be latter)

Probable performance issues:

And about flask scalability:
https://github.com/mitsuhiko/flask/issues/914
I think we safe with it. Before this I have some doubts.

Deployment
Deployment nginx + gunicorn (discussable): Agreed
application as service with start, stop, restart commands
probable packing into docker if we will need scale: Good point.
deployment by git pull from main
development in dev branch from some stage
test app running as usual flask app in debug mode to simplify error catching: OK

Backup:
mongodb backup as is without increments, because mongo sometimes go crazy and broke database without any chance to restore: Totally agree with this for now as i know the behavior too.
the application we will keep in git, so we need backup only database: yes.
currently I don’t see any local files for backup: About that, where will we store files? In AWS i know S3 instances (with possibility to activate backups on files) but in Digital Ocean i do not know how we will handle this. I would like to be able to have S3 storage support. Can you add this later on the v1 release? We will store files in the db using links/locations to the actual file on the server right?
```
