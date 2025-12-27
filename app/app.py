import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.dashboard import dashboard_view
from app.components.appointments import appointments_view
from app.components.records import records_view
from app.components.messages import messages_view
from app.components.settings import settings_view
from app.states.navigation_state import NavigationState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.match(
                        NavigationState.active_page,
                        ("Dashboard", dashboard_view()),
                        ("Appointments", appointments_view()),
                        ("Records", records_view()),
                        ("Messages", messages_view()),
                        ("Settings", settings_view()),
                        dashboard_view(),
                    ),
                    class_name="max-w-7xl mx-auto",
                ),
                class_name="flex-1 overflow-auto p-6 lg:p-10 bg-slate-50 min-h-[calc(100vh-80px)]",
            ),
            class_name="flex flex-col min-h-screen lg:ml-64 w-full",
        ),
        class_name="flex min-h-screen bg-slate-50 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")