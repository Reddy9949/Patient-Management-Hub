import reflex as rx
from app.states.navigation_state import NavigationState
from app.states.patient_state import PatientState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1(
                NavigationState.active_page,
                class_name="text-2xl font-bold text-slate-900",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("bell", class_name="text-slate-600 h-5 w-5"),
                rx.el.span(
                    class_name="absolute top-2 right-2 h-2.5 w-2.5 bg-red-500 rounded-full border-2 border-white"
                ),
                class_name="relative p-2 rounded-full hover:bg-slate-100 transition-colors",
            ),
            rx.el.div(class_name="h-8 w-px bg-slate-200 mx-2"),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        PatientState.patient_name,
                        class_name="text-sm font-semibold text-slate-900 leading-none",
                    ),
                    rx.el.p(
                        f"ID: {PatientState.patient_id}",
                        class_name="text-xs text-slate-500 mt-1",
                    ),
                    class_name="text-right hidden sm:block",
                ),
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={PatientState.patient_name}&backgroundColor=2563eb",
                    class_name="h-10 w-10 rounded-full border-2 border-white shadow-sm",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 px-8 flex items-center justify-between sticky top-0 z-10",
    )