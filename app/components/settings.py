import reflex as rx
from app.states.patient_state import PatientState


def profile_input(
    label: str, value: str, field_name: str, type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-700 mb-1"),
        rx.el.input(
            type=type,
            default_value=value,
            on_change=lambda v: PatientState.update_profile_field(field_name, v),
            class_name="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-blue-500",
        ),
        class_name="mb-4",
    )


def toggle_switch(
    label: str, description: str, checked: bool, setting_name: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-semibold text-slate-900"),
            rx.el.p(description, class_name="text-xs text-slate-500"),
        ),
        rx.el.label(
            rx.el.input(
                type="checkbox",
                default_checked=checked,
                on_change=lambda v: PatientState.toggle_setting(setting_name, v),
                class_name="sr-only peer",
            ),
            rx.el.div(
                class_name="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
            ),
            class_name="relative inline-flex items-center cursor-pointer",
        ),
        class_name="flex items-center justify-between py-4 border-b border-slate-100 last:border-0",
    )


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Account Settings", class_name="text-2xl font-bold text-slate-900"
            ),
            rx.el.p(
                "Manage your profile information and preferences.",
                class_name="text-slate-500 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Personal Profile",
                        class_name="text-lg font-bold text-slate-900 mb-4",
                    ),
                    rx.el.div(
                        rx.image(
                            src=f"https://api.dicebear.com/9.x/initials/svg?seed={PatientState.patient_name}",
                            class_name="h-20 w-20 rounded-full bg-slate-100 mb-4 mx-auto",
                        ),
                        rx.el.button(
                            "Change Avatar",
                            class_name="text-sm text-blue-600 font-medium hover:text-blue-700 block mx-auto mb-6",
                        ),
                    ),
                    profile_input("Full Name", PatientState.patient_name, "name"),
                    profile_input(
                        "Email Address", PatientState.profile_email, "email", "email"
                    ),
                    profile_input(
                        "Phone Number", PatientState.profile_phone, "phone", "tel"
                    ),
                    profile_input(
                        "Home Address", PatientState.profile_address, "address"
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-200",
                ),
                class_name="space-y-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Notifications",
                        class_name="text-lg font-bold text-slate-900 mb-4",
                    ),
                    rx.el.div(
                        toggle_switch(
                            "Email Alerts",
                            "Receive updates about your appointments and results via email.",
                            PatientState.setting_email_alert,
                            "email_alert",
                        ),
                        toggle_switch(
                            "SMS Notifications",
                            "Get text messages for urgent reminders.",
                            PatientState.setting_sms_alert,
                            "sms_alert",
                        ),
                        toggle_switch(
                            "Appointment Reminders",
                            "Receive reminders 24 hours before your visit.",
                            PatientState.setting_appt_reminder,
                            "appt_reminder",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Privacy & Security",
                        class_name="text-lg font-bold text-slate-900 mb-4",
                    ),
                    rx.el.div(
                        toggle_switch(
                            "Profile Visibility",
                            "Allow other doctors in the network to search your profile.",
                            PatientState.setting_profile_visible,
                            "profile_visible",
                        )
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Change Password",
                            class_name="w-full text-left px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors border border-slate-200 mb-3",
                        ),
                        rx.el.button(
                            "Two-Factor Authentication",
                            class_name="w-full text-left px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors border border-slate-200",
                        ),
                        class_name="mt-4",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-slate-200",
                ),
                class_name="space-y-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
        ),
        rx.el.div(
            rx.el.button(
                "Save Changes",
                on_click=PatientState.save_settings,
                class_name="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200",
            ),
            class_name="mt-8 flex justify-end",
        ),
        class_name="animate-fade-in",
    )