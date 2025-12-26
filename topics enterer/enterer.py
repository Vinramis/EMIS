

# WORK IN PROGRESS


# push edit button   button.ant-btn:nth-child(2)
# edit first name   #StudyGuide_data_0_topic_id

# stupid list of topics any button selector   div.ant-select-item-option-content

import time
import json
import os
from playwright.sync_api import sync_playwright

# EDIT_BUTTON_SELECTOR = "button.ant-btn:nth-child(2)"
FIELD_SELECTOR_PART1 = "#StudyGuide_data_"
FIELD_SELECTOR_PART2 = "_topic_id" # must be concatenated with index in the middle (from 0)
# ARROW_SELECTOR = "#StudyGuide > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(3) > div:nth-child(1) > span:nth-child(2)"
VIRTUAL_LIST_SELECTOR = "div.ant-select-item-option-content"
VIRTUAL_LIST_PLACEHOLDER = "" # whatever topic you have, but cut or smth, don't remember