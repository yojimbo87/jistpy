from nicegui import app, ui
import api_router

app.include_router(api_router.router)

ui.run(title='Tester of JISTpy API')
