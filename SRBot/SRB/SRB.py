# Local imports
from GSheet.GSheet import GSheet
from SRBot.SRB.Soldier import Soldier

# STD
from os import getenv as os_getenv
from dotenv import load_dotenv
load_dotenv()


SRB_SPREADSHEET_ID = os_getenv('SRB_SPREADSHEET_ID')
SRB_RANGE = 'SRB!A:O'


class SRB:
    def __init__(self):
        with GSheet(SRB_SPREADSHEET_ID, SRB_RANGE) as sheet:
            self.raw_SRB = sheet.values

    def get_member(self, dodid: int|str=None, discord_id: int|str=None):
        # Checking which ID we'll be checking for. DODID takes priority
        if dodid:
            return self.raw_SRB.loc[self.raw_SRB['DODID'] == str(dodid)]

        elif discord_id:
            return self.raw_SRB.loc[self.raw_SRB['Discord ID'] == str(discord_id)]

if __name__ == '__main__':
    from pprint import pprint

    SRB = SRB()
    print()
    print(SRB.get_member(1064).to_string(index=False))