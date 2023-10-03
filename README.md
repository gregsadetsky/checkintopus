## checkintopus

### what

this is the software/web/oauth-y counterpart of the octopus sign in project. the hardware repo is [here](https://github.com/gregsadetsky/recurse-rfid-visits/).

### TODO

- create superuser on prod
  - test upload of community file
- create signed bucket download urls that expire in 1h to send back to raspi
  - working, test again on prod
- enable s3 bucket versioning to not lose any files if a mistake happens
- allow user uploads
- allow deleting audio files
- rename this project/repo/deployment/render domain/oauth dev&prod apps based on the [poll in zulip](https://recurse.zulipchat.com/#narrow/stream/19042-.F0.9F.A7.91.E2.80.8D.F0.9F.92.BB-current-batches/topic/naming.20suggestion/near/394473437)
  - probs just redeploy on render after name change here to simplify things
  - rename local db too
- rename .recurse.com subdomains once project name has been decided
- render:
  - enable database backups
  - connect papertrail
- re-record all sounds
- when deleting a community sound, check that no user have set it as their solo sound -- ask for confirmation, if ok then delete file and set file preference to random community sound
- auth token vs refresh token - what is it

### hosting details

- the main server is deployed / hosted on render.com (ask greg for access)
- audio files are hosted on aws s3 (ditto -- ask greg)

### huh

- [powered by minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter)
- this project was done during my time at the [Recurse Center](https://recurse.com/)
