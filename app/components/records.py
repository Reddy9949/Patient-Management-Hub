import reflex as rx
from app.states.patient_state import PatientState, MedicalRecord


def record_type_icon(rtype: str) -> rx.Component:
    return rx.match(
        rtype,
        (
            "Lab Results",
            rx.icon("flask-conical", class_name="text-emerald-600 h-6 w-6"),
        ),
        ("Prescriptions", rx.icon("pill", class_name="text-blue-600 h-6 w-6")),
        ("Imaging", rx.icon("image", class_name="text-purple-600 h-6 w-6")),
        ("Visit Summaries", rx.icon("file-text", class_name="text-amber-600 h-6 w-6")),
        rx.icon("file", class_name="text-slate-500 h-6 w-6"),
    )


def record_card(record: MedicalRecord) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                record_type_icon(record["type"]),
                class_name="p-3 bg-slate-50 rounded-xl",
            ),
            rx.el.div(
                rx.el.h4(record["title"], class_name="font-bold text-slate-900"),
                rx.el.div(
                    rx.el.p(
                        record["type"],
                        class_name="text-xs font-semibold text-blue-600 uppercase tracking-wide",
                    ),
                    rx.el.span("•", class_name="text-slate-300"),
                    rx.el.p(
                        record["date"], class_name="text-xs text-slate-500 font-medium"
                    ),
                    class_name="flex items-center gap-2 mt-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4 mr-2"),
                    "View",
                    on_click=lambda: PatientState.open_record_detail(record),
                    class_name="flex items-center px-3 py-1.5 text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                )
            ),
            class_name="flex items-start gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Doctor:", class_name="text-xs text-slate-400 font-medium mr-2"
                ),
                rx.el.span(
                    record["doctor"], class_name="text-sm text-slate-600 font-medium"
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.span(
                    "Size:", class_name="text-xs text-slate-400 font-medium mr-2"
                ),
                rx.el.span(
                    record["file_size"],
                    class_name="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full",
                ),
                class_name="flex items-center",
            ),
            class_name="mt-4 pt-3 border-t border-slate-50 flex justify-between items-center",
        ),
        class_name="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-all",
    )


def record_detail_modal() -> rx.Component:
    rec = PatientState.selected_record
    return rx.cond(
        PatientState.is_record_detail_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Record Details",
                            class_name="text-xl font-bold text-slate-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-slate-400"),
                            on_click=PatientState.close_record_detail,
                            class_name="p-1 hover:bg-slate-100 rounded-full transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            record_type_icon(rec["type"]),
                            class_name="p-4 bg-slate-50 rounded-full mb-4 w-fit mx-auto",
                        ),
                        rx.el.h2(
                            rec["title"],
                            class_name="text-2xl font-bold text-slate-900 text-center mb-1",
                        ),
                        rx.el.p(
                            f"Document ID: {rec['id']}",
                            class_name="text-xs text-slate-400 text-center uppercase tracking-widest mb-6",
                        ),
                        class_name="flex flex-col items-center",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Type", class_name="text-xs text-slate-500 mb-1"),
                            rx.el.p(
                                rec["type"], class_name="font-medium text-slate-900"
                            ),
                            class_name="p-3 bg-slate-50 rounded-xl",
                        ),
                        rx.el.div(
                            rx.el.p("Date", class_name="text-xs text-slate-500 mb-1"),
                            rx.el.p(
                                rec["date"], class_name="font-medium text-slate-900"
                            ),
                            class_name="p-3 bg-slate-50 rounded-xl",
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Ordering Physician",
                            class_name="text-xs text-slate-500 mb-1",
                        ),
                        rx.el.div(
                            rx.icon("stethoscope", class_name="h-4 w-4 text-blue-500"),
                            rx.el.span(
                                rec["doctor"], class_name="font-medium text-slate-900"
                            ),
                            class_name="flex items-center gap-2 p-3 border border-slate-100 rounded-xl",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Description", class_name="text-xs text-slate-500 mb-1"
                        ),
                        rx.el.p(
                            rec["description"],
                            class_name="text-sm text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-xl",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        rx.icon("download", class_name="h-5 w-5 mr-2"),
                        "Download Document",
                        on_click=PatientState.download_record,
                        class_name="w-full flex items-center justify-center bg-blue-600 text-white font-semibold py-3 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
                    ),
                ),
                class_name="bg-white rounded-2xl p-8 w-full max-w-lg shadow-2xl relative z-50 transform transition-all",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity z-40",
                on_click=PatientState.close_record_detail,
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
    )


def tab_button(label: str) -> rx.Component:
    is_active = PatientState.active_record_tab == label
    return rx.el.button(
        label,
        on_click=lambda: PatientState.set_record_tab(label),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-white bg-slate-900 rounded-lg transition-all shadow-md",
            "px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-all",
        ),
    )


def records_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Medical Records", class_name="text-2xl font-bold text-slate-900"
                ),
                rx.el.p(
                    "Access your lab results, imaging, and visit summaries.",
                    class_name="text-slate-500 mt-1",
                ),
                class_name="mb-6",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4",
        ),
        rx.el.div(
            rx.el.div(
                tab_button("All"),
                tab_button("Lab Results"),
                tab_button("Prescriptions"),
                tab_button("Visit Summaries"),
                tab_button("Imaging"),
                class_name="flex flex-wrap gap-2 mb-6",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400",
                ),
                rx.el.input(
                    placeholder="Search by title or doctor...",
                    on_change=PatientState.set_record_search,
                    class_name="pl-10 pr-4 py-2.5 rounded-xl border-slate-200 text-sm w-full md:w-80 focus:ring-blue-500 focus:border-blue-500 shadow-sm",
                    default_value=PatientState.record_search,
                ),
                class_name="relative mb-8",
            ),
        ),
        rx.cond(
            PatientState.filtered_records,
            rx.el.div(
                rx.foreach(PatientState.filtered_records, record_card),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.icon("folder-search", class_name="h-16 w-16 text-slate-200 mb-4"),
                rx.el.h3(
                    "No records found",
                    class_name="text-lg font-semibold text-slate-900",
                ),
                rx.el.p(
                    "Try adjusting your search or filters.", class_name="text-slate-500"
                ),
                class_name="flex flex-col items-center justify-center py-24 text-center bg-white rounded-2xl border border-dashed border-slate-200",
            ),
        ),
        record_detail_modal(),
        class_name="animate-fade-in",
    )