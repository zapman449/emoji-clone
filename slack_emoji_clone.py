#!/usr/bin/env python3

import argparse
import os
import typing

import slack_sdk
from slack_sdk.errors import SlackApiError


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="""Clones one emoji from slack team A to slack team B. Presumes
    the existence of environment variables named <SLACK_TEAM_NAME>_SLACK_TOKEN which grants access""")
    parser.add_argument("source_slack", type=str, help="name of a slack to clone from")
    parser.add_argument("emoji", type=str, help="name of the emoji, please do not include colons")
    parser.add_argument("dest_slack", type=str, help="name of the slack to clone to")
    parser.add_argument("--newname", "-n", type=str, help="optional new name of the emoji. Default is to keep same name")
    args = parser.parse_args()
    if args.newname is None:
        args.newname = args.emoji
    return args


class CloneError(Exception):
    def __init__(self, message):
        self.message = message


def find_url(seeking: str, emoji_data: typing.Dict) -> str:
    if seeking not in emoji_data:
        raise CloneError(f"Chasing emoji aliases failed. {seeking} not found in emoji list.")
    data = emoji_data[seeking]
    if data.startswith("alias:"):
        new_target = data.split(":")[1]
        return find_url(new_target, emoji_data)
    return data


def get_current_emoji(slack_name: str, emoji_name: str) -> str:
    client = slack_sdk.WebClient(token=os.environ[f"{slack_name}_SLACK_TOKEN"])
    try:
        response = client.emoji_list()
    except SlackApiError as e:
        print("failed to list emojis")
        print(f"Error listing emojis: {e.response['error']}")
        raise CloneError(f"SlackAPI error: {e.response['error']}")

    if emoji_name not in response['emoji']:
        print(f"requested emoji {emoji_name} not found in emoji list")
        raise CloneError("Failed to find requested emoji in emoji list")

    emoji_url = find_url(emoji_name, response['emoji'])
    # print(f"emoji_url is {emoji_url}")
    return emoji_url


def push_emoji(slack_name: str, emoji_name: str, emoji_url: str) -> None:
    client = slack_sdk.WebClient(token=os.environ[f"{slack_name}_SLACK_TOKEN"])
    try:
        response = client.admin_emoji_add(name=emoji_name, url=emoji_url)
    except SlackApiError as e:
        print("failed to add new emoji")
        print(f"Error adding new emoji: {e.response['error']}")
        raise CloneError(f"SlackAPI error: {e.response['error']}")


def main() -> None:
    args = parse_cli()
    emoji_url = get_current_emoji(args.source_slack, args.emoji)
    push_emoji(args.dest_slack, args.newname, emoji_url)


if __name__ == "__main__":
    main()