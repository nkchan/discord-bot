# Discord Task Management Bot

This is a Discord bot that helps you manage various task lists (books to read, papers, shopping lists, etc.) by using Google Sheets as a database. You can add, complete, and view tasks directly from Discord commands.

## Features

- **Add Tasks:** Add a new task to a specific list (genre).
- **Complete Tasks:** Mark a task as completed, with a timestamp.
- **List Tasks:** Display all tasks within a specific list.
- **Dynamic Genre Creation:** If you add a task to a genre that doesn't exist, a new sheet (tab) for it is automatically created in your Google Sheet.
- **CI/CD:** Automated testing via GitHub Actions.

## Project Structure

```
/
├── .github/workflows/ci.yml   # GitHub Actions workflow for CI
├── tests/test_g_sheets.py     # Unit tests for Google Sheets integration
├── .env.example               # Example environment file (credentials are not committed)
├── .gitignore                 # Specifies files to be ignored by Git
├── config.py                  # (Currently unused) For static configuration
├── discord_bot.py             # Main entry point for the Discord bot
├── g_sheets.py                # Handles all communication with the Google Sheets API
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- A Discord account and a server where you have admin rights.
- A Google Cloud Platform (GCP) project.

### 2. Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nkchan/discord-bot.git
    cd discord-bot
    ```

2.  **Create a virtual environment:**
    This isolates the project's dependencies from your system.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up credentials:**
    You will need to create two files in the project root: `.env` and `credentials.json`. These files are listed in `.gitignore` and will not be pushed to GitHub.

    -   **`.env` file:**
        Create this file and add your Discord token and Google Sheet key.
        ```env
        DISCORD_TOKEN="your_discord_bot_token"
        SPREADSHEET_KEY="your_google_sheet_key"
        ```

    -   **`credentials.json` file:**
        1.  In your GCP project, enable the **Google Drive API** and **Google Sheets API**.
        2.  Create a **Service Account**.
        3.  Create a JSON key for the service account and download it.
        4.  Rename the downloaded file to `credentials.json` and place it in the project root.
        5.  Open your Google Sheet and share it with the `client_email` found in your `credentials.json`, giving it "Editor" permissions.

5.  **Run the bot:**
    ```bash
    python3 discord_bot.py
    ```
    If everything is set up correctly, you will see a "Logged in as..." message in your console.

---

## How to Use the Bot

Use these slash commands in any channel where the bot is present.

-   ### Add an item
    Adds a new task to a list. If the list doesn't exist, it will be created.
    `/add genre:<genre_name> title:<item_title>`
    -   **Example:** `/add genre:Books title:The Hitchhiker's Guide to the Galaxy`

-   ### Mark an item as done
    Marks an existing task as "Completed" and adds the completion date.
    `/done genre:<genre_name> title:<item_title>`
    -   **Example:** `/done genre:Books title:The Hitchhiker's Guide to the Galaxy`

-   ### List items
    Displays all tasks within a specific list in an embedded message.
    `/list genre:<genre_name>`
    -   **Example:** `/list genre:Books`

---

## For Future Development (AI Collaboration Memo)

This section provides context for future AI-driven code modifications.

-   **Core Logic:** The bot's main logic is in `discord_bot.py`, which handles Discord commands. All Google Sheets operations are abstracted away in `g_sheets.py`.
-   **Authentication:** Credentials for local development are managed via `.env` and `credentials.json`. For GitHub Actions, they are stored in repository secrets (`DISCORD_TOKEN`, `SPREADSHEET_KEY`, `GCP_CREDENTIALS`).
-   **State:** The bot is stateless. All data is stored externally in Google Sheets.
-   **Dependencies:** Key libraries are `discord.py`, `gspread`, and `python-dotenv`. All are listed in `requirements.txt`.
-   **Testing:** Unit tests for the `GSheetsManager` are in `tests/test_g_sheets.py`. The test suite is run automatically by the CI pipeline.
-   **Goal:** The primary goal is to provide a simple, text-based interface for managing various to-do lists, leveraging the strengths of Discord for input and Google Sheets for storage and visibility.