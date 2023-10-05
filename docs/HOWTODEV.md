### how to dev

- start local server i.e. activate venv then `python manage.py runserver`
- run ngrok locally: `ngrok http 8000`
- note the ngrok address i.e. `SOME-SUBDOMAIN.ngrok-free.app`
- add the ngrok address to your .env var i.e. `ALLOWED_HOSTS='localhost,SOME-SUBDOMAIN.ngrok-free.app'`
- update the recurse cname domain proxy to point to ngrok
  - go [here](https://www.recurse.com/domains)
  - set the destination of `octopass-dev.recurse.com` to your ngrok https url i.e. `https://SOME-SUBDOMAIN.ngrok-free.app`
  - note that if there are multiple developers doing this, you might need to create new octopass-dev-greg, octopass-dev-jane, etc. subdomains
- go to the [recurse oauth apps](https://www.recurse.com/settings/apps). if the oauth app doesn't exist yet, create it:
  - the redirect uri value should be: `https://octopass-dev.recurse.com/oauth_redirect`
  - copy the oauth id, secret, and redirect_uri into the .env file
  - note that if you are deleting/re-creating an oauth app, all past tokens that you may have in your database (from a previous oauth app) will be invalid. just something to watch out for.
- you might need to restart the `python manage.py runserver` to make sure that new .env values have been picked up
- you're ready to test it now!
- go to https://octopass-dev.recurse.com/
  - are you redirected to recurse to login?
  - are you brought back once you do login?
  - are you able to deny the oauth login?
  - can you login in this app, go to your authorized oauth apps at the bottom of [this page](https://www.recurse.com/settings/apps), delete the authorization you gave to the dev oauth app, and reload the app?

### notes

you will have to redo a new oauth app every time you start ngrok, since the free ngrok gives you a different domain every time you use it...! it's annoying!
