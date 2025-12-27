import reflex as rx
from typing import TypedDict


class NavItem(TypedDict):
    label: str
    icon: str
    value: str


class NavigationState(rx.State):
    active_page: str = "Dashboard"
    menu_items: list[NavItem] = [
        {"label": "Dashboard", "icon": "layout-dashboard", "value": "Dashboard"},
        {"label": "Appointments", "icon": "calendar", "value": "Appointments"},
        {"label": "Records", "icon": "file-text", "value": "Records"},
        {"label": "Messages", "icon": "message-square", "value": "Messages"},
        {"label": "Settings", "icon": "settings", "value": "Settings"},
    ]

    @rx.event
    def set_page(self, page: str):
        self.active_page = page