import reflex as rx
from app.states.patient_state import PatientState, Message


def message_item(msg: Message) -> rx.Component:
    is_selected = PatientState.selected_message["id"] == msg["id"]
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={msg['avatar']}",
                class_name="h-10 w-10 rounded-full bg-slate-100 shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        rx.cond(
                            msg["sender"] == "Me",
                            "To: " + msg["recipient"],
                            msg["sender"],
                        ),
                        class_name=rx.cond(
                            ~msg["read"],
                            "text-sm font-bold text-slate-900",
                            "text-sm font-medium text-slate-700",
                        ),
                    ),
                    rx.el.span(msg["date"], class_name="text-xs text-slate-400"),
                    class_name="flex justify-between items-baseline",
                ),
                rx.el.p(
                    msg["subject"],
                    class_name=rx.cond(
                        ~msg["read"],
                        "text-xs font-semibold text-slate-900 mt-0.5 truncate",
                        "text-xs text-slate-600 mt-0.5 truncate",
                    ),
                ),
                rx.el.p(
                    msg["preview"], class_name="text-xs text-slate-400 mt-1 truncate"
                ),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex gap-3",
        ),
        on_click=lambda: PatientState.select_message(msg),
        class_name=rx.cond(
            is_selected,
            "p-4 bg-blue-50 border-l-4 border-blue-600 cursor-pointer transition-all",
            "p-4 bg-white hover:bg-slate-50 border-l-4 border-transparent border-b border-slate-100 cursor-pointer transition-all",
        ),
    )


def thread_message_item(msg: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={msg['avatar']}",
                class_name="h-10 w-10 rounded-full bg-slate-100 shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        msg["sender"], class_name="font-semibold text-slate-900 text-sm"
                    ),
                    rx.el.span(msg["date"], class_name="text-xs text-slate-500 ml-2"),
                    class_name="flex items-baseline",
                ),
                rx.text(
                    msg["body"],
                    white_space="pre-wrap",
                    class_name="text-slate-700 text-sm leading-relaxed mt-1",
                ),
                class_name="flex-1",
            ),
            class_name="flex gap-3",
        ),
        class_name="py-6 border-b border-slate-100 last:border-0",
    )


def conversation_view() -> rx.Component:
    msg = PatientState.selected_message
    return rx.cond(
        msg,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        msg["subject"],
                        class_name="text-xl font-bold text-slate-900 leading-tight",
                    ),
                    rx.el.div(
                        rx.el.span(
                            msg["role"],
                            class_name="px-2 py-1 bg-slate-100 text-slate-600 text-xs font-medium rounded-md",
                        ),
                        rx.el.span(msg["date"], class_name="text-sm text-slate-500"),
                        class_name="flex gap-2 items-center mt-2",
                    ),
                    class_name="p-6 border-b border-slate-100",
                ),
                rx.el.div(
                    thread_message_item(msg),
                    rx.foreach(msg["replies"], thread_message_item),
                    class_name="p-6 flex-1 overflow-auto",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("reply", class_name="h-4 w-4 mr-2"),
                        "Reply",
                        on_click=PatientState.reply_message,
                        class_name="bg-blue-600 text-white px-6 py-2 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
                    ),
                    class_name="p-6 border-t border-slate-100 bg-slate-50 rounded-b-2xl",
                ),
            ),
            class_name="bg-white rounded-2xl shadow-sm border border-slate-200 h-full flex flex-col",
        ),
        rx.el.div(
            rx.icon("mail-open", class_name="h-16 w-16 text-slate-200 mb-4"),
            rx.el.p(
                "Select a conversation to read", class_name="text-slate-400 font-medium"
            ),
            class_name="h-full flex flex-col items-center justify-center bg-slate-50 rounded-2xl border border-dashed border-slate-200",
        ),
    )


def compose_modal() -> rx.Component:
    return rx.cond(
        PatientState.is_compose_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "New Message", class_name="text-xl font-bold text-slate-900"
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-6 w-6 text-slate-400"),
                        on_click=PatientState.close_compose_modal,
                        class_name="p-1 hover:bg-slate-100 rounded-full transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "To",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "Select recipient...", value="", disabled=True
                            ),
                            rx.foreach(
                                PatientState.available_doctors,
                                lambda d: rx.el.option(d, value=d),
                            ),
                            rx.el.option(
                                "Billing Department", value="Billing Department"
                            ),
                            rx.el.option("Lab Services", value="Lab Services"),
                            value=PatientState.compose_recipient,
                            on_change=lambda v: PatientState.update_compose_field(
                                "recipient", v
                            ),
                            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Subject",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="Enter subject...",
                            on_change=lambda v: PatientState.update_compose_field(
                                "subject", v
                            ),
                            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
                            default_value=PatientState.compose_subject,
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Message",
                            class_name="block text-sm font-medium text-slate-700 mb-1",
                        ),
                        rx.cond(
                            PatientState.is_replying,
                            rx.el.div(
                                rx.el.p(
                                    "Conversation History",
                                    class_name="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2",
                                ),
                                rx.el.div(
                                    thread_message_item(PatientState.selected_message),
                                    rx.foreach(
                                        PatientState.selected_message["replies"],
                                        thread_message_item,
                                    ),
                                    class_name="bg-slate-50 p-4 rounded-xl border border-slate-200 mb-4 max-h-60 overflow-y-auto",
                                ),
                            ),
                        ),
                        rx.el.textarea(
                            placeholder="Type your message here...",
                            on_change=lambda v: PatientState.update_compose_field(
                                "body", v
                            ),
                            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500 h-48 resize-none",
                            default_value=PatientState.compose_body,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Send Message",
                        on_click=PatientState.submit_message,
                        class_name="w-full bg-blue-600 text-white font-semibold py-3 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
                    ),
                ),
                class_name="bg-white rounded-2xl p-6 w-full max-w-lg shadow-xl relative z-50",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-40",
                on_click=PatientState.close_compose_modal,
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
    )


def messages_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Messages", class_name="text-2xl font-bold text-slate-900"),
                rx.el.p(
                    "Secure communication with your healthcare team.",
                    class_name="text-slate-500 mt-1",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4 mr-2"),
                "Compose",
                on_click=PatientState.open_compose_modal,
                class_name="flex items-center bg-blue-600 text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Search messages...",
                        class_name="w-full rounded-xl border-slate-200 bg-slate-50 focus:bg-white transition-colors pl-4 pr-4 py-2 text-sm",
                    ),
                    class_name="p-4 border-b border-slate-100",
                ),
                rx.el.div(
                    rx.foreach(PatientState.latest_messages, message_item),
                    class_name="flex flex-col overflow-y-auto h-[calc(100vh-320px)]",
                ),
                class_name="col-span-1 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-[calc(100vh-250px)]",
            ),
            rx.el.div(
                conversation_view(),
                class_name="col-span-1 lg:col-span-2 h-[calc(100vh-250px)]",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
        compose_modal(),
        class_name="animate-fade-in",
    )