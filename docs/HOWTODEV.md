### how to dev

- start local server i.e. activate venv then `python manage.py runserver`
- run ngrok locally: `ngrok http 8000`
- note the ngrok address i.e. `SOME-SUBDOMAIN.ngrok-free.app`
- add the ngrok address to your .env var i.e. `ALLOWED_HOSTS='localhost,SOME-SUBDOMAIN.ngrok-free.app'`
- update the recurse cname domain proxy to point to ngrok

  - go [here](https://www.recurse.com/domains)
  - set the destination of checkintopus-dev.recurse.com to your ngrok https url
  - note that if there are multiple developers doing this, you might need to create new checkintopus-dev-greg, checkintopus-greg-jane, etc. subdomains

- TODO document how to create/edit/update the oauth app...??
