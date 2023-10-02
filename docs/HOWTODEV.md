### how to dev

- start local server i.e. activate venv then `python manage.py runserver`
- run ngrok locally: `ngrok http 8000`
- note the ngrok address i.e. `SOME-SUBDOMAIN.ngrok-free.app`
- add the ngrok address to your .env var i.e. `ALLOWED_HOSTS='localhost,SOME-SUBDOMAIN.ngrok-free.app'`
- update the recurse cname domain proxy to point to ngrok

  - go [here](https://www.recurse.com/domains)
  - set the destination of checkintopus-dev.recurse.com to your ngrok https url
  - note that if there are multiple developers doing this, you might need to create new checkintopus-dev-greg, checkintopus-greg-jane, etc. subdomains

- go to the [recurse oauth apps](https://www.recurse.com/settings/apps) and create a dev oauth app
  - the redirect uri will be: `https://SOME-SUBDOMAIN.ngrok-free.app/oauth_redirect` i.e. ngrok domain + `/oauth_redirect`
- copy the oauth id, secret, and redirect_uri into the .env file
- you're ready to test it now!
- go to https://SOME-SUBDOMAIN.ngrok-free.app/
  - are you redirected to recurse to login?
  - are you brought back once you do login?
  - are you able to deny the oauth login?
  - can you login in this app, go to your authorized oauth apps at the bottom of [this page](https://www.recurse.com/settings/apps), delete the authorization you gave to the dev oauth app, and reload the app?