## checkintopus

### what

this is the software/web/UI/oauth-y counterpart of the octopus sign in project. the hardware repo is [here](https://github.com/gregsadetsky/recurse-rfid-visits/).

### TODO

- re-record all sounds
- rename .recurse.com subdomains once project name has been decided
- render:
  - enable database backups
  - connect papertrail
- auth token vs refresh token - what is it
- rename this project/repo/deployment/render domain/oauth dev&prod apps based on the [poll in zulip](https://recurse.zulipchat.com/#narrow/stream/19042-.F0.9F.A7.91.E2.80.8D.F0.9F.92.BB-current-batches/topic/naming.20suggestion/near/394473437)
  - probs just redeploy on render after name change here to simplify things
  - rename local db too

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

- create a local superuser using our own `python manage.py create_oauth_superuser <email> <username> <password>`
  - this is necessary instead of the usual `python manage.py createsuperuser` because our `User` model includes oauth & rfid card infos that "regular" django superusers wouldn't have by default...!
- check [HOWTODEV.md](./docs/HOWTODEV.md) for more specific oauth/domain setup details

### huh

- [powered by minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter)
- this project was done during my time at the [Recurse Center](https://recurse.com/)
