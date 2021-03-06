# junior.guru

## Status of the README

This README is missing a lot of information. Honza didn't have time yet to add a proper, nice README. The file currently only includes documentation of the hard parts of the development process, which would be easy to forget and difficult to learn again.

## Contributions

Don't panic, failing build under your PR is unrelated to your changes. Contributions are welcome, but Honza didn't have much time yet to make the repo very friendly to contributors. Very likely, your PR fixing a typo in the text will get merged regardless the failing checks.

## Installation on M1

```
$ brew install openblas gfortran
$ export OPENBLAS=$(/usr/local/bin/brew --prefix openblas)
$ export CFLAGS="-falign-functions=8 ${CFLAGS}"
```

Thanks [@lutzroeder](https://github.com/scipy/scipy/issues/13409#issuecomment-774640468), no thanks SciPy.

## Setting up email address

According to [spectrum.chat/zeit](https://spectrum.chat/zeit/now/redirection-email-domain~b5e1b613-ae92-42f9-bc49-e8c824a8a7f2?m=MTUzNDE5OTg3MzMwMw==):

1.  Run following:

    ```
    $ now dns add junior.guru '@' MX mx1.improvmx.com 10
    $ now dns add junior.guru '@' MX mx2.improvmx.com 20
    $ now dns add junior.guru '@' TXT 'v=spf1 include:spf.improvmx.com include:_spf.google.com ~all'
    ```
1.  Fill the form at [ImprovMX](https://improvmx.com/)
1.  Setup and verify the address in [MailChimp](https://mailchimp.com/)
1.  [Authenticate in MailChimp](https://mailchimp.com/help/verify-a-domain/) and add respective DNS records:

    ```
    $ now dns add k2._domainkey.junior.guru '@' CNAME 'dkim2.mcsv.net'
    $ now dns add k3._domainkey.junior.guru '@' CNAME 'dkim3.mcsv.net'
    ```

## Setting up Google Drive credentials

1.  Follow the steps in the [gspread guide](https://gspread.readthedocs.io/en/latest/oauth2.html). Instead of Google Drive API, enable Google Sheets API.
1.  Save the obtained JSON file into the `juniorguru/sync` directory as `google_service_account.json`
1.  Make sure it is ignored by Git
1.  Run `cat juniorguru/sync/google_service_account.json | pbcopy` to copy the JSON into your clipboard (macOS)
1.  Go to CircleCI project settings, page Environment Variables
1.  Add `GOOGLE_SERVICE_ACCOUNT` variable and paste the JSON from your clipboard as a value

The service account's email address needs to be manually invited wherever it should have access. If it should be able to access Google Analytics, go there and invite it as if it was a user.

## Setting up MailChimp credentials

1. Follow [MailChimp's own guide](https://mailchimp.com/help/about-api-keys/) on how to create an API key
1. Set it as `MAILCHIMP_API_KEY` environment variable for both local devlopment and production

## Setting up SMTP credentials

1.  If using Gmail for sending e-mails, [create an app password](https://security.google.com/settings/security/apppasswords).
1.  Set the following environment variables:

    ```bash
    export SMTP_HOST='smtp.example.com'
    export SMTP_PORT='587'
    export SMTP_USERNAME='example@example.com'
    export SMTP_PASSWORD='abc...xyz'
    ```

By default, sending is not enabled. On production or when trying to send e-mails from localhost an environment variable `SMTP_ENABLED` needs to be set to something truthy.

## Setting up logo.junior.guru

The [logo.junior.guru](https://logo.junior.guru/) has [it's own repo](https://github.com/honzajavorek/logo.junior.guru/) and runs on GitHub Pages. Set it up in DNS:

```
$ now dns add logo.junior.guru '@' CNAME 'honzajavorek.github.io'
```

## Verify Google Search Console

In [Google Search Console](https://support.google.com/webmasters/answer/9008080?hl=en) click verify and set a TXT DNS record.

## Logging

The environment variable `LOG_LEVEL` affects what gets filtered out. It's set to `info` by default.
