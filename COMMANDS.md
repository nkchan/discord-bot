# Bot Commands

This file lists the available commands for the Discord Task Management Bot.

## Commands

-   `/add genre:<genre_name> title:<item_title>`
    -   Adds a new task to a list. If the list doesn't exist, it will be created.
    -   **Example:** `/add genre:Books title:The Hitchhiker's Guide to the Galaxy`

-   `/done genre:<genre_name> title:<item_title>`
    -   Marks an existing task as "Completed" and adds the completion date.
    -   **Example:** `/done genre:Books title:The Hitchhiker's Guide to the Galaxy`

-   `/list genre:<genre_name>`
    -   Displays all tasks within a specific list in an embedded message.
    -   **Example:** `/list genre:Books`
