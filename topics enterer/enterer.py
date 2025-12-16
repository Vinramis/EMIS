

# WORK IN PROGRESS


# push edit button   button.ant-btn:nth-child(2)
# edit first name   #StudyGuide_data_0_topic_id

# edit third name   .ant-select-status-success > div:nth-child(1) > span:nth-child(2)

import time
import json
import os
from playwright.sync_api import sync_playwright
import pandas as pd

EDIT_BUTTON_SELECTOR = "button.ant-btn:nth-child(2)"
FIELD_SELECTOR_PART1 = "#StudyGuide_data_"
FIELD_SELECTOR_PART2 = "_topic_id" # must be concatenated with index in the middle
ARROW_SELECTOR = "#StudyGuide > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(3) > div:nth-child(1) > span:nth-child(2)"
VIRTUAL_LIST_SELECTOR = "body > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6)"
pd.get