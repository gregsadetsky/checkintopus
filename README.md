## checkintopus

### what

this is the software/web/oauth-y counterpart of the octopus sign in project. the hardware repo is [here](https://github.com/gregsadetsky/recurse-rfid-visits/).

### TODO

- restart this dir from that starter, git push force
- add render deployment-specific files
- separate settings into prod/dev
- deploy to render
- create prod subdomain on recurse.com
- create dev subdomain on recurse.com
- document how to dev using dev subdomain
- create oauth apps for prod and dev
- create oauth-views
- write wrapper around recurse API endpoints
  - publish something? are there existing (ruby?) wrappers?
  - include as requirement...??
  - create openapi spec...?? auto gen'd code from spec is usually bad..? so why?
- base view: check if session exists, if not, redirect to login
  - if session, api request to recurse and get name
- have logout
- auth token vs refresh token - what is it
- auto logout on token not working - show error as well? use messages django package?
- dev and prod s3 buckets for audio files
- list audio files, allow user uploads
- bucket should not be public
- create signed bucket download urls that expire in 1h to send back to raspi
- create management test command to simulate api call from raspi with card
- in s3 bucket have directory for 'own' audio files i.e. setup audio, etc. and UGC audio
- allow anyone to add&delete audio files
- enable s3 bucket versioning to not lose any files if a mistake happens
- connect papertrail
- enable database backups
- rename this project/repo/deployment/domain based on the [poll in zulip](https://recurse.zulipchat.com/#narrow/stream/19042-.F0.9F.A7.91.E2.80.8D.F0.9F.92.BB-current-batches/topic/naming.20suggestion/near/394473437)

### huh

- [powered by minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter)
- this project was done during my time at the [Recurse Center](https://recurse.com/)
