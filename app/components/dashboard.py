import reflex as rx
from app.states.patient_state import PatientState
from app.states.navigation_state import NavigationState


def stat_card(
    title: str,
    value: str,
    subtext: str,
    icon: str,
    color: str,
    action: rx.event.EventType = None,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"text-{color}-600 h-6 w-6"),
                class_name=f"p-3 rounded-xl bg-{color}-100 w-fit",
            ),
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-slate-500"),
                rx.el.h3(value, class_name="text-2xl font-bold text-slate-900 mt-1"),
                rx.el.p(subtext, class_name="text-xs text-slate-400 mt-1"),
            ),
            class_name="flex flex-col gap-4",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow",
    )


def appointment_card(appt: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    appt["date"].split(",")[0],
                    class_name="text-xs font-bold text-blue-600 uppercase tracking-wider",
                ),
                rx.el.p(
                    appt["date"].split(",")[1],
                    class_name="text-lg font-bold text-slate-900",
                ),
                class_name="bg-blue-50 p-3 rounded-xl text-center min-w-[80px]",
            ),
            rx.el.div(
                rx.el.h4(appt["doctor"], class_name="font-bold text-slate-900"),
                rx.el.p(
                    appt["specialty"], class_name="text-sm text-blue-600 font-medium"
                ),
                rx.el.div(
                    rx.icon("map-pin", class_name="h-3 w-3 text-slate-400 mr-1"),
                    rx.el.span(appt["location"], class_name="text-xs text-slate-500"),
                    class_name="flex items-center mt-2",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    appt["status"],
                    class_name="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700",
                )
            ),
            class_name="flex gap-4 items-start",
        ),
        class_name="p-4 rounded-xl border border-slate-100 hover:bg-slate-50 transition-colors",
    )


def record_row(record: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="text-slate-400 h-5 w-5"),
            class_name="p-2 bg-slate-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(record["title"], class_name="text-sm font-semibold text-slate-900"),
            rx.el.p(
                f"{record['type']} • {record['doctor']}",
                class_name="text-xs text-slate-500",
            ),
            class_name="flex-1 ml-3",
        ),
        rx.el.p(record["date"], class_name="text-xs text-slate-400 font-medium"),
        on_click=lambda: PatientState.open_record_from_dashboard(record),
        class_name="flex items-center p-3 hover:bg-slate-50 rounded-xl transition-colors cursor-pointer",
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                f"Welcome back, {PatientState.patient_name.split(' ')[0]}!",
                class_name="text-2xl font-bold text-slate-900",
            ),
            rx.el.p(
                "Here is an overview of your health status today.",
                class_name="text-slate-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Next Appointment", class_name="font-bold text-slate-900"),
                    rx.el.button(
                        "See All",
                        on_click=lambda: NavigationState.set_page("Appointments"),
                        class_name="text-xs font-semibold text-blue-600 hover:text-blue-700",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.cond(
                    PatientState.upcoming_appointments,
                    appointment_card(PatientState.next_appointment),
                    rx.el.p(
                        "No upcoming appointments", class_name="text-slate-500 text-sm"
                    ),
                ),
                class_name="col-span-1 lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
            ),
            rx.el.div(
                stat_card(
                    "Unread Messages",
                    PatientState.unread_messages.to_string(),
                    "2 from doctors",
                    "message-square",
                    "indigo",
                ),
                stat_card(
                    "Latest Vitals",
                    "Normal",
                    "Last check: 2 days ago",
                    "activity",
                    "emerald",
                ),
                class_name="col-span-1 flex flex-col gap-4",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Recent Medical Records", class_name="font-bold text-slate-900"
                    ),
                    rx.el.button(
                        rx.icon("arrow-right", class_name="h-4 w-4"),
                        on_click=PatientState.view_records,
                        class_name="p-2 hover:bg-slate-100 rounded-full text-slate-400 hover:text-blue-600 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    rx.foreach(PatientState.recent_records, record_row),
                    class_name="flex flex-col gap-1",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-100",
            ),
            rx.el.div(
                rx.el.h3("Quick Actions", class_name="font-bold text-slate-900 mb-4"),
                rx.el.div(
                    rx.el.button(
                        rx.icon("calendar-plus", class_name="mb-3 h-8 w-8 text-white"),
                        rx.el.span("Book Appt", class_name="font-semibold text-white"),
                        on_click=PatientState.book_appointment,
                        class_name="flex flex-col items-center justify-center p-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl shadow-lg shadow-blue-200 hover:translate-y-[-2px] transition-transform w-full",
                    ),
                    rx.el.button(
                        rx.icon("file-search", class_name="mb-3 h-8 w-8 text-blue-600"),
                        rx.el.span(
                            "View Results", class_name="font-semibold text-blue-900"
                        ),
                        on_click=PatientState.view_records,
                        class_name="flex flex-col items-center justify-center p-6 bg-white border border-slate-200 rounded-2xl hover:border-blue-300 hover:bg-blue-50 transition-colors w-full",
                    ),
                    rx.el.button(
                        rx.icon(
                            "mail-plus", class_name="mb-3 h-8 w-8 text-emerald-600"
                        ),
                        rx.el.span(
                            "Message Dr.", class_name="font-semibold text-emerald-900"
                        ),
                        on_click=PatientState.send_message,
                        class_name="flex flex-col items-center justify-center p-6 bg-white border border-slate-200 rounded-2xl hover:border-emerald-300 hover:bg-emerald-50 transition-colors w-full",
                    ),
                    rx.el.button(
                        rx.icon("pill", class_name="mb-3 h-8 w-8 text-purple-600"),
                        rx.el.span(
                            "Refills", class_name="font-semibold text-purple-900"
                        ),
                        on_click=PatientState.view_refills,
                        class_name="flex flex-col items-center justify-center p-6 bg-white border border-slate-200 rounded-2xl hover:border-purple-300 hover:bg-purple-50 transition-colors w-full",
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                class_name="bg-transparent",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        class_name="animate-fade-in",
    )