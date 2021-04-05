# emoji-clone
Process to clone an emoji from one slack workspace to another.

## Requirements:

* Requires python3
* You will need to install the slack_sdk for python: `pip3 install --upgrade slack_sdk`
* You will need a "legacy token" to interact with the source and destination slack teams

## Slack permissions:

At this time, you must be an administrator of the slack team to which you are copying the emoji. 
This is a limitation of the slack API where `admin_emoji_add` is the only API endpoint for uploading
an emoji, and it is restricted to Owner/Admins of the slack team.  

Oddly, users (in general) can upload emoji's through the `Customize` web page.

So, if this is of use to you...

## Usage:

```
./slack_emoji_clone.py <SRC_SLACK_NAME> <EMOJI_NAME> <DEST_SLACK_NAME> [NEW_EMOJI_NAME]
```
If you omit NEW_EMOJI_NAME, the current name will be used.

This process takes slack tokens as environment variables.  Variable names are `slackname_SLACK_TOKEN`
where `slackname` is freeform, but must match what you pass in on the CLI.  See the example:

## Example:

```
source_SLACK_TOKEN=xoxp-11111 dest_SLACK_TOKEN=xoxp-22222 ./slack_emoji_clone.py source yay dest yaynew
```
