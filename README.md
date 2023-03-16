# SkyPro Diploma: TodoList
### Python 3.10, Django 4.1.5, Postgres

A simple todolist API-based app. Front from an image, Telegram bot lives in a separate repository of mine.
This is a Django Rest Framework project. The structure:
- core: user authentication and TG user validation
- boards: goal boards
- goals: goal categories, goals and comments.
- The structure is a bit strange due to the way tasks were exposed.

* Project start, first commit.
* Docker and deployment stuff added.
* Authorization added.
* VK authorization is present, but doesn't work, as I don't have an account there.
Github authorization is working, but not present on the front. Check /api/oauth/login/github manually.
* Goals, categories and goal comments added
* Boards added
* Telegram bot added
* Tests...
