import reflex as rx
from app.states.navigation_state import NavigationState


def nav_item(item: dict) -> rx.Component:
    is_active = NavigationState.active_page == item["value"]
    return rx.el.button(
        rx.icon(
            item["icon"],
            class_name=rx.cond(
                is_active,
                "text-blue-600",
                "text-slate-500 group-hover:text-blue-600 transition-colors",
            ),
            size=20,
        ),
        rx.el.span(
            item["label"],
            class_name=rx.cond(
                is_active,
                "font-semibold text-blue-900",
                "font-medium text-slate-600 group-hover:text-blue-900 transition-colors",
            ),
        ),
        on_click=lambda: NavigationState.set_page(item["value"]),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-4 py-3 bg-blue-50 rounded-xl w-full transition-all border-r-4 border-blue-600",
            "flex items-center gap-3 px-4 py-3 hover:bg-slate-50 rounded-xl w-full transition-all group border-r-4 border-transparent",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="text-white h-6 w-6"),
                class_name="bg-blue-600 p-2 rounded-lg shadow-lg shadow-blue-200",
            ),
            rx.el.div(
                rx.el.span("Medi", class_name="text-blue-900 font-bold text-xl"),
                rx.el.span("Portal", class_name="text-blue-600 font-bold text-xl"),
                class_name="flex flex-row",
            ),
            class_name="flex items-center gap-3 px-2 mb-10",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.p(
                    "MENU",
                    class_name="text-xs font-bold text-slate-400 mb-4 px-4 tracking-wider",
                ),
                rx.foreach(NavigationState.menu_items, nav_item),
                class_name="flex flex-col gap-2",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("life-buoy", class_name="text-blue-600 h-6 w-6 mb-2"),
                rx.el.p(
                    "Need Help?", class_name="font-semibold text-slate-900 text-sm"
                ),
                rx.el.p("Contact support", class_name="text-xs text-slate-500 mb-3"),
                rx.el.button(
                    "Support Center",
                    class_name="w-full bg-blue-600 text-white text-xs font-semibold py-2 rounded-lg hover:bg-blue-700 transition-colors",
                ),
                class_name="bg-blue-50 rounded-2xl p-4",
            ),
            class_name="mt-auto",
        ),
        class_name="hidden lg:flex flex-col w-64 h-screen bg-white border-r border-slate-200 p-6 fixed left-0 top-0 z-20",
    )