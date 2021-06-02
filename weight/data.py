import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES: List[str] = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
RANGES: List[str] = ["Peso Diário", "Objetivos"]

CREDENTIALS_FILENAME: str = "credentials.json"
TOKEN_FILENAME: str = "token.json"


def main() -> None:
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILENAME):
        # Documentation:
        # - https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html
        creds = Credentials.from_authorized_user_file(TOKEN_FILENAME, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILENAME, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open(TOKEN_FILENAME, "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API.
    sheet = service.spreadsheets()

    result = (
        sheet.values()
        .batchGet(spreadsheetId=os.getenv("SPREADSHEET_ID"), ranges=RANGES)
        .execute()
    )

    values = result.get("valueRanges")

    weights = values[0].get("values")
    goals = values[1].get("values")

    weights_df = pd.DataFrame(weights[1:], columns=weights[0])
    goals_df = pd.DataFrame(goals[1:], columns=goals[0])

    weights_df.to_csv("data/weights.csv", index=False)
    goals_df.to_csv("data/goals.csv", index=False)


if __name__ == "__main__":
    load_dotenv()
    main()
