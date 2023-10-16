## octopass

### what

this is Octopass, a hardware & software project that lets people attending the Recurse Center to sign in using their door fob.

this is the software/web/UI/front+back-end/oauth-y counterpart of the project. the hardware code repo is [here](https://github.com/gregsadetsky/recurse-rfid-visits/).

### how to dev

- assuming a 'normal' python/venv setup i.e.:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- copy `.env.example` to `.env` and fill out the appropriate values
- create a local superuser using our own `python manage.py create_oauth_superuser <email> <username> <password>`
  - this is necessary instead of the usual `python manage.py createsuperuser` because our `User` model includes oauth & rfid card infos that "regular" django superusers wouldn't have by default...!
- check [HOWTODEV.md](./docs/HOWTODEV.md) for more specific oauth/domain setup details!!

### hosting details

- the main server is deployed / hosted on render.com (ask greg for access)
- audio files are hosted on aws s3 (ditto -- ask greg)

### TODO

- add check if superuser with no token (i.e. admin user...) and don't error 500...
- Make sure that generated random color fruit is unique across last hour!
- add unenroll advanced option on index page - GET page to see what it entails, POST to do it; delete user object, logout, redirect to index
- render:
  - connect papertrail
- rename this project/repo/deployment/render domain/oauth dev&prod apps to octopass
  - probs just redeploy on render after name change here to simplify things
  - https://github.com/gregsadetsky/recurse-rfid-visits/issues/13
- Add way of saying what will be working on through mic on octopass -- speech recognition
- fwup nick re hosting on RC heroku
- better copy for 'view all community sounds'..?
- fwup nick re ipad sign in repo? and make it websocket’y or poll more often?

### huh

- this web backend is powered by [minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter)
- this project was made by <img src="https://eaafa.greg.technology/authors?Itay%20Shoshani,Greg%20Sadetsky" style="height:20px; width: 100px; vertical-align: middle" title="Itay Shoshani, Greg Sadetsky" />[^1]

[^1]: [EAAFA](https://eaafa.greg.technology/)
