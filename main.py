from core import STORAGE_SECRET, init_db
from nicegui import ui, app

import models
init_db()

import views.pages.login
import views.pages.my_shelf

@ui.page('/')
def index():
    if not app.storage.user.get('user_id'):
        ui.navigate.to('/login')
    else:
        ui.navigate.to('/my_shelf')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        storage_secret=STORAGE_SECRET,
        title="Shelf",
        favicon='static/favicon.svg'
    )