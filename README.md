# Off-white Dunk Tracker

There are 50 offwhite dunk lows, called "lots" that are basically the same shoe with different colored accents.

They are each sold as seperate products on stockx, so there is no good way to track the lowest price of all the lots combined.
That is the problem this app solves.

## Development

### Startup
Once cloned:
- in `remote_state`, run `terraform init`, `terraform plan`, and `terraform apply` to stand up the remote state infrastrucuture. This should stay deployed for the entirety of your development life
- in src, run `pip install --target ./package requests` to package requests for lambda deploy.
    - NOTE: see [here](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) for more information
- in the root, run `terraform init`, `terraform plan`, and `terraform apply` to deploy the app.

## TODO:
[ ] run.sh to init everything for initial deployment
[ ] switch to algolia because bot defenses on stockx wont let me hit the api from a lambda

## Credit
stockx-sdk is taken from [nikevp](https://github.com/nikevp/stockx-py-sdk)
