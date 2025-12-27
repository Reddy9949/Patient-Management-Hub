import reflex as rx
from typing import TypedDict
from datetime import datetime
import logging


class Appointment(TypedDict):
    id: str
    doctor: str
    specialty: str
    date: str
    time: str
    location: str
    status: str
    reason: str


class MedicalRecord(TypedDict):
    id: str
    title: str
    date: str
    type: str
    doctor: str
    description: str
    file_size: str
    status: str


class Message(TypedDict):
    id: str
    sender: str
    recipient: str
    role: str
    subject: str
    preview: str
    body: str
    date: str
    read: bool
    avatar: str
    replies: list[dict]


class PatientState(rx.State):
    patient_name: str = "Sarah Jenkins"
    patient_id: str = "P-89201"
    patient_age: int = 34
    patient_blood_type: str = "O+"
    all_appointments: list[Appointment] = [
        {
            "id": "1",
            "doctor": "Dr. Michael Chen",
            "specialty": "Cardiology",
            "date": "Oct 24, 2024",
            "time": "10:00 AM",
            "location": "Main Campus, Wing A",
            "status": "Confirmed",
            "reason": "Regular Checkup",
        },
        {
            "id": "2",
            "doctor": "Dr. Emily Wilson",
            "specialty": "Dermatology",
            "date": "Nov 12, 2024",
            "time": "02:30 PM",
            "location": "West Clinic, Ste 304",
            "status": "Pending",
            "reason": "Skin Rash Consultation",
        },
        {
            "id": "3",
            "doctor": "Dr. James Wilson",
            "specialty": "General Practice",
            "date": "Sep 15, 2024",
            "time": "09:00 AM",
            "location": "Main Campus, Wing B",
            "status": "Completed",
            "reason": "Annual Physical",
        },
        {
            "id": "4",
            "doctor": "Dr. Sarah Smith",
            "specialty": "Endocrinology",
            "date": "Aug 05, 2024",
            "time": "11:15 AM",
            "location": "Eastside Medical Center",
            "status": "Cancelled",
            "reason": "Follow up",
        },
    ]
    appointment_filter: str = "Upcoming"
    appointment_search: str = ""
    active_tab: str = "Upcoming"
    is_booking_open: bool = False
    booking_doctor: str = ""
    booking_date: str = ""
    booking_time: str = ""
    booking_location: str = ""
    booking_reason: str = ""
    booking_id: str = ""
    selected_appointment: Appointment = {}
    is_detail_open: bool = False
    available_doctors: list[str] = [
        "Dr. Michael Chen (Cardiology)",
        "Dr. Emily Wilson (Dermatology)",
        "Dr. James Wilson (General Practice)",
        "Dr. Sarah Smith (Endocrinology)",
        "Dr. Lisa Ray (Pediatrics)",
    ]
    available_locations: list[str] = [
        "Main Campus, Wing A",
        "Main Campus, Wing B",
        "West Clinic, Ste 304",
        "Eastside Medical Center",
        "North Valley Hospital",
    ]
    active_record_tab: str = "All"
    record_search: str = ""
    selected_record: MedicalRecord = {}
    is_record_detail_open: bool = False
    recent_records: list[MedicalRecord] = [
        {
            "id": "rec_001",
            "title": "Blood Work Panel - Q3",
            "date": "Oct 20, 2024",
            "type": "Lab Results",
            "doctor": "Dr. Sarah Smith",
            "description": "Comprehensive metabolic panel and lipid profile results.",
            "file_size": "2.4 MB",
            "status": "Final",
        },
        {
            "id": "rec_002",
            "title": "Annual Physical Summary",
            "date": "Sep 15, 2024",
            "type": "Visit Summaries",
            "doctor": "Dr. James Wilson",
            "description": "Summary of annual physical examination, including vitals and patient history update.",
            "file_size": "1.1 MB",
            "status": "Final",
        },
        {
            "id": "rec_003",
            "title": "Echocardiogram Report",
            "date": "Aug 02, 2024",
            "type": "Imaging",
            "doctor": "Dr. Michael Chen",
            "description": "Transthoracic echocardiogram imaging report and cardiologist notes.",
            "file_size": "15.8 MB",
            "status": "Final",
        },
        {
            "id": "rec_004",
            "title": "Amoxicillin Prescription",
            "date": "Jul 10, 2024",
            "type": "Prescriptions",
            "doctor": "Dr. Emily Wilson",
            "description": "Prescription details for 10-day course of antibiotics.",
            "file_size": "0.5 MB",
            "status": "Expired",
        },
        {
            "id": "rec_005",
            "title": "Dermatology Consult Note",
            "date": "Nov 12, 2024",
            "type": "Visit Summaries",
            "doctor": "Dr. Emily Wilson",
            "description": "Consultation notes regarding skin rash assessment and treatment plan.",
            "file_size": "1.2 MB",
            "status": "Final",
        },
    ]
    unread_messages: int = 2
    selected_message: Message = {}
    is_compose_open: bool = False
    is_replying: bool = False
    compose_recipient: str = ""
    compose_subject: str = ""
    compose_body: str = ""
    latest_messages: list[Message] = [
        {
            "id": "msg_01",
            "sender": "Dr. Michael Chen",
            "recipient": "Sarah Jenkins",
            "role": "Cardiologist",
            "subject": "Re: Follow up on medication",
            "preview": "Please continue with the current dosage until our next appointment...",
            "body": """Hi Sarah,

Thanks for the update. Based on your blood pressure readings, I think we should stay the course. Please continue with the current dosage until our next appointment. If you experience any dizziness, let me know immediately.

Best,
Dr. Chen""",
            "date": "Today, 9:15 AM",
            "read": False,
            "avatar": "Michael",
            "replies": [],
        },
        {
            "id": "msg_02",
            "sender": "Lab Services",
            "recipient": "Sarah Jenkins",
            "role": "System",
            "subject": "Results Available: Blood Panel",
            "preview": "Your recent lab results from Oct 20 are now available for view...",
            "body": """Dear Patient,

Your recent lab results from Oct 20 are now available for viewing in the Medical Records section of your portal. Please contact your ordering physician if you have questions about these results.

Thank you,
Central Labs""",
            "date": "Yesterday, 4:30 PM",
            "read": False,
            "avatar": "Lab",
            "replies": [],
        },
        {
            "id": "msg_03",
            "sender": "Dr. James Wilson",
            "recipient": "Sarah Jenkins",
            "role": "Primary Care",
            "subject": "Annual Physical Reminder",
            "preview": "It's that time of year again. Please schedule your physical soon...",
            "body": """Hello Sarah,

Just a friendly reminder that you are due for your annual physical this month. Regular check-ups are key to maintaining good health. Please use the booking tool or call our office to set up a time.

Regards,
Dr. Wilson""",
            "date": "Oct 01, 2024",
            "read": True,
            "avatar": "James",
            "replies": [
                {
                    "id": "msg_03_reply_1",
                    "sender": "Sarah Jenkins",
                    "recipient": "Dr. James Wilson",
                    "role": "Patient",
                    "subject": "Re: Annual Physical Reminder",
                    "preview": "Thanks Dr. Wilson, I'll book it now.",
                    "body": "Thanks Dr. Wilson, I'll book it now.",
                    "date": "Oct 02, 2024",
                    "read": True,
                    "avatar": "Sarah",
                    "replies": [],
                }
            ],
        },
    ]
    profile_email: str = "sarah.jenkins@example.com"
    profile_phone: str = "(555) 123-4567"
    profile_address: str = "123 Maple Ave, Springfield, IL"
    setting_email_alert: bool = True
    setting_sms_alert: bool = False
    setting_appt_reminder: bool = True
    setting_profile_visible: bool = False
    download_url: str = ""

    @rx.var
    def upcoming_appointments(self) -> list[Appointment]:
        return [
            appt
            for appt in self.all_appointments
            if appt["status"] in ["Confirmed", "Pending"]
        ]

    @rx.var
    def filtered_appointments(self) -> list[Appointment]:
        filtered = self.all_appointments
        if self.active_tab == "Upcoming":
            filtered = [a for a in filtered if a["status"] in ["Confirmed", "Pending"]]
        elif self.active_tab == "Past":
            filtered = [
                a for a in filtered if a["status"] in ["Completed", "Cancelled"]
            ]
        if self.appointment_search:
            search = self.appointment_search.lower()
            filtered = [
                a
                for a in filtered
                if search in a["doctor"].lower() or search in a["specialty"].lower()
            ]
        return filtered

    @rx.var
    def next_appointment(self) -> Appointment:
        return self.upcoming_appointments[0] if self.upcoming_appointments else {}

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def open_booking_modal(self):
        self.is_booking_open = True
        self.booking_id = ""
        self.booking_doctor = ""
        self.booking_date = ""
        self.booking_time = ""
        self.booking_location = ""
        self.booking_reason = ""

    @rx.event
    def close_booking_modal(self):
        self.is_booking_open = False

    @rx.event
    def open_detail_modal(self, appointment: Appointment):
        self.selected_appointment = appointment
        self.is_detail_open = True

    @rx.event
    def close_detail_modal(self):
        self.is_detail_open = False

    @rx.event
    def update_booking_field(self, field: str, value: str):
        setattr(self, f"booking_{field}", value)

    @rx.event
    def submit_booking(self):
        if not self.booking_doctor or not self.booking_date:
            return rx.toast("Please fill in all required fields.", duration=3000)
        import random

        display_date = self.booking_date
        try:
            dt = datetime.strptime(self.booking_date, "%Y-%m-%d")
            display_date = dt.strftime("%b %d, %Y")
        except ValueError as e:
            logging.exception(f"Error parsing booking date: {e}")
        new_appt = {
            "id": self.booking_id or str(random.randint(1000, 9999)),
            "doctor": self.booking_doctor.split("(")[0].strip(),
            "specialty": self.booking_doctor.split("(")[1].strip(")")
            if "(" in self.booking_doctor
            else "General",
            "date": display_date,
            "time": self.booking_time or "09:00 AM",
            "location": self.booking_location,
            "status": "Pending",
            "reason": self.booking_reason,
        }
        if self.booking_id:
            self.all_appointments = [
                new_appt if a["id"] == self.booking_id else a
                for a in self.all_appointments
            ]
            rx.toast("Appointment rescheduled successfully.")
        else:
            self.all_appointments.insert(0, new_appt)
            rx.toast("Appointment request sent successfully.")
        self.is_booking_open = False

    @rx.event
    def cancel_appointment(self, appt_id: str):
        self.all_appointments = [
            {**a, "status": "Cancelled"} if a["id"] == appt_id else a
            for a in self.all_appointments
        ]
        self.is_detail_open = False
        rx.toast("Appointment cancelled.")

    @rx.event
    def reschedule_appointment(self, appt: Appointment):
        self.is_detail_open = False
        self.booking_id = appt["id"]
        self.booking_doctor = f"{appt['doctor']} ({appt['specialty']})"
        try:
            dt = datetime.strptime(appt["date"], "%b %d, %Y")
            self.booking_date = dt.strftime("%Y-%m-%d")
        except ValueError as e:
            logging.exception(f"Error parsing date for rescheduling: {e}")
            self.booking_date = appt["date"]
        self.booking_time = appt["time"]
        self.booking_location = appt["location"]
        self.booking_reason = appt.get("reason", "")
        self.is_booking_open = True

    @rx.event
    async def book_appointment(self):
        from app.states.navigation_state import NavigationState

        nav = await self.get_state(NavigationState)
        nav.active_page = "Appointments"
        self.open_booking_modal()

    @rx.event
    async def view_records(self):
        from app.states.navigation_state import NavigationState

        nav = await self.get_state(NavigationState)
        nav.active_page = "Records"
        self.active_record_tab = "All"
        self.record_search = ""

    @rx.event
    async def open_record_from_dashboard(self, record: MedicalRecord):
        from app.states.navigation_state import NavigationState

        nav = await self.get_state(NavigationState)
        nav.active_page = "Records"
        self.selected_record = record
        self.is_record_detail_open = True

    @rx.event
    async def send_message(self):
        from app.states.navigation_state import NavigationState

        nav = await self.get_state(NavigationState)
        nav.active_page = "Messages"
        self.open_compose_modal()

    @rx.event
    async def view_refills(self):
        from app.states.navigation_state import NavigationState

        nav = await self.get_state(NavigationState)
        nav.active_page = "Records"
        self.active_record_tab = "Prescriptions"
        self.record_search = ""

    @rx.var
    def filtered_records(self) -> list[MedicalRecord]:
        records = self.recent_records
        if self.active_record_tab != "All":
            records = [r for r in records if r["type"] == self.active_record_tab]
        if self.record_search:
            search = self.record_search.lower()
            records = [
                r
                for r in records
                if search in r["title"].lower() or search in r["doctor"].lower()
            ]
        return records

    @rx.event
    def set_record_tab(self, tab: str):
        self.active_record_tab = tab

    @rx.event
    def set_record_search(self, term: str):
        self.record_search = term

    @rx.event
    def open_record_detail(self, record: MedicalRecord):
        self.selected_record = record
        self.is_record_detail_open = True

    @rx.event
    def close_record_detail(self):
        self.is_record_detail_open = False

    @rx.event
    async def download_record(self):
        record = self.selected_record
        yield rx.toast(f"Generating download for {record['title']}...", duration=2000)
        content = f"MEDICAL RECORD REPORT\n---------------------\nID: {record.get('id', 'N/A')}\nTitle: {record.get('title', 'N/A')}\nDate: {record.get('date', 'N/A')}\nType: {record.get('type', 'N/A')}\nDoctor: {record.get('doctor', 'N/A')}\nStatus: {record.get('status', 'N/A')}\n\nDESCRIPTION:\n{record.get('description', 'No description available.')}\n\n---------------------\nGenerated by MediPortal\n"
        safe_title = (
            "".join(
                (
                    c
                    for c in record.get("title", "record")
                    if c.isalnum() or c in (" ", "_", "-")
                )
            )
            .strip()
            .replace(" ", "_")
        )
        filename = f"{safe_title}_{record.get('id', 'doc')}.txt"
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        self.download_url = f"/_upload/{filename}"
        yield rx.download(url=self.download_url)

    @rx.event
    def select_message(self, message: Message):
        self.selected_message = message
        self.latest_messages = [
            {**m, "read": True} if m["id"] == message["id"] else m
            for m in self.latest_messages
        ]
        self.unread_messages = max(
            0, len([m for m in self.latest_messages if not m["read"]])
        )

    @rx.event
    def open_compose_modal(self):
        self.is_compose_open = True
        self.is_replying = False
        self.compose_recipient = ""
        self.compose_subject = ""
        self.compose_body = ""

    @rx.event
    def close_compose_modal(self):
        self.is_compose_open = False

    @rx.event
    def update_compose_field(self, field: str, value: str):
        setattr(self, f"compose_{field}", value)

    @rx.event
    def submit_message(self):
        if not self.compose_recipient or not self.compose_body:
            return rx.toast("Please fill in recipient and message body.", duration=3000)
        import random

        new_msg = {
            "id": str(random.randint(10000, 99999)),
            "sender": "Me",
            "recipient": self.compose_recipient,
            "role": "Patient",
            "subject": self.compose_subject or "(No Subject)",
            "preview": self.compose_body[:50] + "...",
            "body": self.compose_body,
            "date": "Just now",
            "read": True,
            "avatar": "Sarah",
            "replies": [],
        }
        if self.is_replying and self.selected_message:
            updated_messages = []
            for msg in self.latest_messages:
                if msg["id"] == self.selected_message["id"]:
                    msg["replies"].append(new_msg)
                    self.selected_message = msg
                updated_messages.append(msg)
            self.latest_messages = updated_messages
            rx.toast("Reply sent successfully.")
        else:
            self.latest_messages.insert(0, new_msg)
            rx.toast("Message sent successfully.")
        self.is_compose_open = False

    @rx.event
    def reply_message(self):
        self.is_compose_open = True
        self.is_replying = True
        sender = self.selected_message["sender"]
        if sender == "Me":
            self.compose_recipient = self.selected_message["recipient"]
        else:
            self.compose_recipient = sender
        self.compose_subject = f"Re: {self.selected_message['subject']}"
        self.compose_body = ""

    @rx.event
    def update_profile_field(self, field: str, value: str):
        setattr(self, f"profile_{field}", value)

    @rx.event
    def toggle_setting(self, setting: str, value: bool):
        setattr(self, f"setting_{setting}", value)

    @rx.event
    def save_settings(self):
        rx.toast("Settings saved successfully.")