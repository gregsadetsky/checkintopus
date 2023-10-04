## octopass

### what

this is Octopass, a hardware & software project that lets people attending the Recurse Center to sign in using their door fob.

this is the software/web/UI/oauth-y counterpart of the project. the hardware code repo is [here](https://github.com/gregsadetsky/recurse-rfid-visits/).

### TODO

- render:
  - connect papertrail
- auth token vs refresh token - what is it
- rename this project/repo/deployment/render domain/oauth dev&prod apps to octopass
  - probs just redeploy on render after name change here to simplify things

### hosting details

- the main server is deployed / hosted on render.com (ask greg for access)
- audio files are hosted on aws s3 (ditto -- ask greg)

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

### huh

- powered by [minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter)
- this project was done during my time at the [Recurse Center](https://recurse.com/)
