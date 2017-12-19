#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys

import constants
from workflow import (ICON_INFO, ICON_WARNING, MATCH_STARTSWITH,
                      MATCH_SUBSTRING, Workflow, web)


def get_gitmojis():
    resp = web.get(constants.GITMOJIS_JSON_URL)
    resp.raise_for_status()
    return resp.json()['gitmojis']


def search_key_for_gitmoji(gitmoji):
    return ' '.join([gitmoji['name'], gitmoji['description']])


def check_workflow_update(wf):
    if wf.update_available:
        wf.add_item(
            'New version available',
            'Action this item to install the update',
            autocomplete='workflow:update',
            icon=ICON_INFO)


def main(wf):
    check_workflow_update(wf)
    query = wf.args[0] if len(wf.args) else None
    copy_type = os.getenv(constants.COPY_TYPE_ENV, 'code')
    gitmojis = wf.cached_data(
        'gitmojis', get_gitmojis, max_age=constants.CACHE_TIME)
    gitmojis = wf.filter(
        query,
        gitmojis,
        key=search_key_for_gitmoji,
        min_score=20,
        match_on=MATCH_STARTSWITH | MATCH_SUBSTRING)
    if not gitmojis:
        wf.add_item('Not found', icon=ICON_WARNING)
    for gitmoji in gitmojis:
        wf.add_item(
            title=gitmoji['name'],
            subtitle=gitmoji['description'],
            arg=gitmoji[copy_type],
            valid=True,
            uid=gitmoji['name'],
            icon='emojis/%s.png' % gitmoji['name'],
            largetext=gitmoji['emoji'],
            copytext=gitmoji[copy_type],
            quicklookurl=constants.GITMOJIS_WEBSITE)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(
        update_settings=constants.WORKFLOW_UPDATE_SETTINGS,
        help_url=constants.GITHUB_ISSUE_URL)
    sys.exit(wf.run(main))
