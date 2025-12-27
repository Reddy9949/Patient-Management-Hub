import reflex as rx
from app.states.patient_state import PatientState, Appointment


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Confirmed",
                "px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700 border border-emerald-200",
            ),
            (
                "Pending",
                "px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-700 border border-amber-200",
            ),
            (
                "Cancelled",
                "px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700 border border-red-200",
            ),
            (
                "Completed",
                "px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200",
            ),
            "px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700",
        ),
    )


def appointment_card(appt: Appointment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    appt["date"].split(",")[0],
                    class_name="text-xs font-bold text-blue-600 uppercase tracking-wider",
                ),
                rx.el.p(
                    appt["date"].split(",")[1],
                    class_name="text-xl font-bold text-slate-900 leading-tight",
                ),
                rx.el.p(
                    appt["time"], class_name="text-sm font-medium text-slate-500 mt-1"
                ),
                class_name="bg-blue-50/50 p-4 rounded-xl text-center min-w-[100px] flex flex-col justify-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        appt["doctor"], class_name="font-bold text-lg text-slate-900"
                    ),
                    status_badge(appt["status"]),
                    class_name="flex justify-between items-start mb-1",
                ),
                rx.el.p(
                    appt["specialty"],
                    class_name="text-sm text-blue-600 font-medium mb-3",
                ),
                rx.el.div(
                    rx.icon("map-pin", class_name="h-4 w-4 text-slate-400 shrink-0"),
                    rx.el.span(
                        appt["location"], class_name="text-sm text-slate-600 truncate"
                    ),
                    class_name="flex items-center gap-2 mb-1",
                ),
                rx.el.div(
                    rx.icon("info", class_name="h-4 w-4 text-slate-400 shrink-0"),
                    rx.el.span(
                        appt["reason"],
                        class_name="text-sm text-slate-500 truncate italic",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex-1 py-1",
            ),
            class_name="flex gap-5 flex-col sm:flex-row",
        ),
        rx.el.div(
            rx.el.button(
                "View Details",
                on_click=lambda: PatientState.open_detail_modal(appt),
                class_name="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors w-full sm:w-auto text-center",
            ),
            class_name="mt-4 pt-4 border-t border-slate-100 flex justify-end",
        ),
        class_name="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-all",
    )


def detail_modal() -> rx.Component:
    appt = PatientState.selected_appointment
    return rx.cond(
        PatientState.is_detail_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Appointment Details",
                            class_name="text-xl font-bold text-slate-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-slate-400"),
                            on_click=PatientState.close_detail_modal,
                            class_name="p-1 hover:bg-slate-100 rounded-full transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Status", class_name="text-xs text-slate-500 mb-1"),
                            status_badge(appt["status"]),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.p("Doctor", class_name="text-xs text-slate-500 mb-1"),
                            rx.el.p(
                                appt["doctor"],
                                class_name="font-semibold text-slate-900",
                            ),
                            rx.el.p(
                                appt["specialty"], class_name="text-sm text-blue-600"
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Date & Time", class_name="text-xs text-slate-500 mb-1"
                            ),
                            rx.el.div(
                                rx.icon(
                                    "calendar", class_name="h-4 w-4 text-slate-400"
                                ),
                                rx.el.span(
                                    f"{appt['date']} at {appt['time']}",
                                    class_name="text-sm font-medium text-slate-900",
                                ),
                                class_name="flex items-center gap-2",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Location", class_name="text-xs text-slate-500 mb-1"
                            ),
                            rx.el.div(
                                rx.icon("map-pin", class_name="h-4 w-4 text-slate-400"),
                                rx.el.span(
                                    appt["location"],
                                    class_name="text-sm font-medium text-slate-900",
                                ),
                                class_name="flex items-center gap-2",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Reason for Visit",
                                class_name="text-xs text-slate-500 mb-1",
                            ),
                            rx.el.p(
                                appt["reason"],
                                class_name="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg",
                            ),
                            class_name="mb-6",
                        ),
                        class_name="space-y-2",
                    ),
                    rx.el.div(
                        rx.cond(
                            (appt["status"] == "Confirmed")
                            | (appt["status"] == "Pending"),
                            rx.el.div(
                                rx.el.button(
                                    "Reschedule",
                                    on_click=lambda: PatientState.reschedule_appointment(
                                        appt
                                    ),
                                    class_name="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors",
                                ),
                                rx.el.button(
                                    "Cancel Appointment",
                                    on_click=lambda: PatientState.cancel_appointment(
                                        appt["id"]
                                    ),
                                    class_name="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors",
                                ),
                                class_name="grid grid-cols-2 gap-3",
                            ),
                            rx.el.div(),
                        ),
                        class_name="mt-6 pt-6 border-t border-slate-100",
                    ),
                    class_name="bg-white rounded-2xl p-6 w-full max-w-md shadow-xl transform transition-all",
                ),
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-40",
                on_click=PatientState.close_detail_modal,
            ),
        ),
    )


def booking_modal() -> rx.Component:
    return rx.cond(
        PatientState.is_booking_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Book Appointment",
                        class_name="text-xl font-bold text-slate-900",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-6 w-6 text-slate-400"),
                        on_click=PatientState.close_booking_modal,
                        class_name="p-1 hover:bg-slate-100 rounded-full transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Select Doctor",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "Choose a specialist...", value="", disabled=True
                            ),
                            rx.foreach(
                                PatientState.available_doctors,
                                lambda d: rx.el.option(d, value=d),
                            ),
                            value=PatientState.booking_doctor,
                            on_change=lambda v: PatientState.update_booking_field(
                                "doctor", v
                            ),
                            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Date",
                                class_name="block text-sm font-medium text-slate-700 mb-1",
                            ),
                            rx.el.input(
                                type="date",
                                placeholder="YYYY-MM-DD",
                                on_change=lambda v: PatientState.update_booking_field(
                                    "date", v
                                ),
                                class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
                                default_value=PatientState.booking_date,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Time",
                                class_name="block text-sm font-medium text-slate-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Select time", value="", disabled=True),
                                rx.el.option("09:00 AM", value="09:00 AM"),
                                rx.el.option("10:00 AM", value="10:00 AM"),
                                rx.el.option("11:00 AM", value="11:00 AM"),
                                rx.el.option("02:00 PM", value="02:00 PM"),
                                rx.el.option("03:00 PM", value="03:00 PM"),
                                value=PatientState.booking_time,
                                on_change=lambda v: PatientState.update_booking_field(
                                    "time", v
                                ),
                                class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Location",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Select location...", value="", disabled=True),
                            rx.foreach(
                                PatientState.available_locations,
                                lambda l: rx.el.option(l, value=l),
                            ),
                            value=PatientState.booking_location,
                            on_change=lambda v: PatientState.update_booking_field(
                                "location", v
                            ),
                            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Reason for Visit",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.textarea(
                            placeholder="Briefly describe your symptoms or reason for visit...",
                            on_change=lambda v: PatientState.update_booking_field(
                                "reason", v
                            ),
                            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500 h-24 resize-none",
                            default_value=PatientState.booking_reason,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Confirm Booking",
                        on_click=PatientState.submit_booking,
                        class_name="w-full bg-blue-600 text-white font-semibold py-3 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
                    ),
                ),
                class_name="bg-white rounded-2xl p-6 w-full max-w-lg shadow-xl relative z-50",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-40",
                on_click=PatientState.close_booking_modal,
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
    )


def tab_button(label: str) -> rx.Component:
    is_active = PatientState.active_tab == label
    return rx.el.button(
        label,
        on_click=lambda: PatientState.set_tab(label),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-blue-600 bg-blue-50 rounded-lg transition-all",
            "px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-700 hover:bg-slate-50 rounded-lg transition-all",
        ),
    )


def appointments_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "My Appointments", class_name="text-2xl font-bold text-slate-900"
                ),
                rx.el.p(
                    "Manage your upcoming visits and view history.",
                    class_name="text-slate-500 mt-1",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-5 w-5 mr-2"),
                "Book New",
                on_click=PatientState.open_booking_modal,
                class_name="flex items-center bg-blue-600 text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    tab_button("Upcoming"),
                    tab_button("Past"),
                    tab_button("All"),
                    class_name="flex gap-1 bg-white p-1 rounded-xl border border-slate-100 shadow-sm",
                ),
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400",
                    ),
                    rx.el.input(
                        placeholder="Search doctor or specialty...",
                        on_change=PatientState.set_appointment_search,
                        class_name="pl-10 pr-4 py-2 rounded-xl border-slate-200 text-sm w-full sm:w-64 focus:ring-blue-500 focus:border-blue-500",
                        default_value=PatientState.appointment_search,
                    ),
                    class_name="relative w-full sm:w-auto",
                ),
                class_name="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6",
            ),
            rx.el.div(
                rx.cond(
                    PatientState.filtered_appointments,
                    rx.foreach(PatientState.filtered_appointments, appointment_card),
                    rx.el.div(
                        rx.icon(
                            "calendar-x", class_name="h-12 w-12 text-slate-300 mb-3"
                        ),
                        rx.el.p(
                            "No appointments found.",
                            class_name="text-slate-500 font-medium",
                        ),
                        class_name="flex flex-col items-center justify-center py-12 text-center bg-white rounded-2xl border border-dashed border-slate-200",
                    ),
                ),
                class_name="flex flex-col gap-4",
            ),
            class_name="col-span-1 lg:col-span-3",
        ),
        booking_modal(),
        detail_modal(),
        class_name="animate-fade-in",
    )