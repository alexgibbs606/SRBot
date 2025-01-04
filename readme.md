# SRBot

The SRBot is to assist S1 in interfacing with the SRB as quickly and convinently as possible. As always, the SRB should be considered the authority.

## Contributing

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help for details on contributions.

### Table of Contents

### Authoring code

Before considering contributing code, please make sure that your intended addition matches our [core values](#core-values) and follows our [Roadmap](#roadmap). Any code contributions are willingly given to the project, and on submission you surrender all rights to the code as written.

#### Commit Messages

In general, we attempt to keep commit messages PAST tense, as if you're reading them from a change log. This allows quick generation of change logs. i.e. "Updated reference to S1 role ID in config" as opposed to "S1 role id reference updated"

### Reporting Bugs

Before submitting a bug report, please make sure to collect the nessessary information for a developer to replicate and resolve the report without having to collect additional details from yourself. Following the steps below will help us to fix bugs as fast as possible.

- Check that you're using the latest version
- Check against documentation to confirm the bug is, in fact, a bug
- Search other bug reports to see if your bug has been reported. If so, it's possible that report may benefit from additional information
- Collect information about the bug
    - Stack trace (traceback)
    - OS/platform and version the bot is runing on
    - Version of Python and packages
    - Steps used to reproduce the issue
    - What the anticipated response was

### Submitting a bug

- Open an issue on github
- Provide information collected from [Reporting Bugs](#reporting-bugs)
- Provide as many details as possible to help reproduce the issue

## Setup

To install the SRBot on a server, start by cloning the production branch of the project on github

``` bash
git pull origin git@github.com:alexgibbs606/SRBot.git
git checkout prod
```

Once cloned, install the required packages via pip using the requirements file, or if you prefer pipenv, the appropriate command.

``` bash
pip install -r requirements.txt
```

### tokens

A `.env` file must be created, populating the `DISCORD_TOKEN` variable with the proper bot token.

### Config

A `config.json` file must be created that will contain various structured information about the discord server for the bot to work properly. Below is an example config file populating exactly all the required values.

``` json
{
    "auth_roles": {
        "s1": [1324958350684717077],
        "recruiter": [1324953963082289172, 1324953963082289172]
    },
    "role_assignments": {
        "member": 1324959155177390163,
        "default": 1324959078321229824,
        "recruit": 1324920352823840821
    }
}
```

### Running SRBot

To run the bot, you can run the SRBot directory without any arguments

``` bash
python SRBot
```


## Roadmap
Initially, we'll be focusing only on commands utilized by S1 to prevent the need for accessing google sheet SRB for small alterations.

Current plan is to get SRB temp actions work
- Enlistment
- SRB single user output via DODID or Discord ID
- Promotions

### Core Values

As always, the SRB should be considered the authority. When making changes, we should always assume the SRB is correct and mold information around it to the SRB. Include error checks as only the SRB is protected. i.e. check if someone has a role for a second company and remove it when handling a transfer request.

### Roster interactions
- Transfers
- Roster by unit
    - Should be able to specify unit. Squad will show only squad, platoon will show platoon HQ and squad leaders, company will show company HQ and platoon HQ, batt will show batt. HQ and company HQ.
- Awards

### Additional SRB actions
- Automatically generated promotion and award certs

### Configurability
- Easy ability to add support elements with or without seperate callsigns


We'll be using the google sheet as a SQL alternative that's viewable and alterable online. Below is a general schema idea for the table's we'll need to use.

#### SRB
- DODID
- Discord ID
- Name
- Nickname
- Rank ID
- MOS
- TIS Date
- TIG Date
- Status
- Notes

#### Roster
- DODID
- Billet
- Callsign
- Roster ID
- Direct CoC Roster ID
- OIC Roster ID

#### Activity
- DODID
- Date
- Points awarded
- Activity Description

#### Awards
- DODID
- Award Name
- Date
- OIC DODID
- Description
- Award message