## checkintopus

### what

this is the software/web/oauth-y counterpart of the octopus sign in project. the hardware repo is [here](https://github.com/gregsadetsky/recurse-rfid-visits/).

### TODO

- model for rfid logins
- log all rfid logins (view->model)
- respond to rfid login with unknown rfid tag: 'welcome, go online, your tag is X (color-fruit)'
- respond to rfid login with known rfid tag: fetch audio preference/audio file url, send back, log user into hub
- document how to dev using dev subdomain in HOWTODEV.md
- create oauth app for prod
- create oauth-views
- write wrapper around recurse API endpoints
  - publish something? are there existing (ruby?) wrappers?
  - include as requirement...??
  - create openapi spec...?? auto gen'd code from spec is usually bad..? so why?
- auth token vs refresh token - what is it
- dev and prod s3 buckets for audio files
- list audio files
- allow user uploads
- allow deleting audio files
- bucket should not be public
- create signed bucket download urls that expire in 1h to send back to raspi
- create management test command to simulate api call from raspi with card
- in s3 bucket have directory for 'own' audio files i.e. setup audio, etc. and UGC audio
- enable s3 bucket versioning to not lose any files if a mistake happens
- connect papertrail
- enable database backups
- rename this project/repo/deployment/render domain based on the [poll in zulip](https://recurse.zulipchat.com/#narrow/stream/19042-.F0.9F.A7.91.E2.80.8D.F0.9F.92.BB-current-batches/topic/naming.20suggestion/near/394473437)
- rename .recurse.com subdomains once project name has been decided
- create superuser on prod
- handle access_denied

### huh

- [powered by minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter)
- this project was done during my time at the [Recurse Center](https://recurse.com/)
