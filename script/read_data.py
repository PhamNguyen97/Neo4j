import pandas as pd
import json
import re

datetime_re = re.compile(r": datetime.datetime\((.*?)\)")
re_1 = re.compile(r'([0-9])+"')

data = pd.read_excel("data/data.xlsx")

e_count = 0
for i, row in data.iterrows():
    print(i)
    comment = row["comments_full"]
    if not isinstance(comment, float):
        # comment = comment.replace('"', "``")
        inches = re_1.findall(comment)
        for inch in inches:
            comment = comment.replace(f'{inch}"',
                                      f'{inch}``')

        if comment[-2:] != "}]":
            comment += "'}]"
        comment = comment.replace('" FHD', "`` FHD").replace("'", '"').replace('" ', "' ").replace(": None", ": null")
        datetime_strings = datetime_re.findall(comment)
        for datetime_string in datetime_strings:
            comment = comment.replace(f": datetime.datetime({datetime_string})", f': "datetime.datetime({datetime_string})"')
        try:
            comment = json.loads(comment)
        except Exception as e:
            print(e)
            print(comment)
            print(comment[32760:32770])
            e_count += 1
            break

