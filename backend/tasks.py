from extensions import celery, mail
from flask_mail import Message
from flask import current_app
from model import User, ReserveSpot
import csv, os
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

@celery.task()
def send_daily_reminders():
    users = User.query.all()
    for user in users:
        msg = Message("Daily Parking Reminder", recipients=[user.email])
        msg.body = f"Hi {user.fullname},\nDon't forget to check your active bookings today."
        mail.send(msg)


@celery.task()
def generate_monthly_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return 'User not found'

    bookings = ReserveSpot.query.filter_by(user_id=user_id).filter(ReserveSpot.leaving_time.isnot(None)).all()

    total_cost = 0
    lines = [
        f"📅 Monthly Parking Report for {user.fullname}",
        f"────────────────────────────────────────────",
        f"{'ID':<5}{'Vehicle':<15}{'Start':<20}{'End':<20}{'Cost':>8}",
        f"{'-'*70}"
    ]

    for b in bookings:
        parking_ist = b.parking_time.replace(tzinfo=timezone.utc).astimezone(IST)
        leaving_ist = b.leaving_time.replace(tzinfo=timezone.utc).astimezone(IST) if b.leaving_time else None
        leaving = leaving_ist.strftime('%Y-%m-%d %H:%M') if b.leaving_time else '---'
        parking = parking_ist.strftime('%Y-%m-%d %H:%M')
        cost = f"{b.cost:.2f}" if b.cost else ""
        total_cost += b.cost if b.leaving_time else 0
        lines.append(f"{b.id:<5}{b.vehicle_no:<15}{parking:<20}{leaving:<20}{cost:>8}")

    lines.append(f"{'-'*70}")
    lines.append(f"Total Bookings: {len(bookings)}")
    lines.append(f"Total Spent (Rs): ₹{total_cost:.2f}")
    lines.append(f"────────────────────────────────────────────")

    report = "\n".join(lines)

    # Send email
    msg = Message("Your Monthly Parking Report 🚗", recipients=[user.email])
    msg.body = report
    mail.send(msg)

    return report

@celery.task()
def generate_all_monthly_reports():
    users = User.query.all()
    for user in users:
        generate_monthly_report.delay(user.id)



@celery.task()
def export_bookings_to_csv(user_id):
    user = User.query.get(user_id)
    bookings = ReserveSpot.query.filter_by(user_id=user_id).filter(ReserveSpot.leaving_time.isnot(None)).all()
    filename = f"bookings_{user_id}_{datetime.now(timezone.utc).isoformat()}.csv"
    filepath = os.path.join(current_app.config.get('EXPORT_DIR', '.'), filename)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Vehicle No', 'Parking Time', 'Leaving Time', 'Cost'])
        for b in bookings:
            parking_ist = b.parking_time.replace(tzinfo=timezone.utc).astimezone(IST)
            leaving_ist = b.leaving_time.replace(tzinfo=timezone.utc).astimezone(IST) if b.leaving_time else None
            writer.writerow([b.id,
                             b.vehicle_no,
                             parking_ist.strftime('%d %b %Y, %I:%M %p'),
                             leaving_ist.strftime('%d %b %Y, %I:%M %p') if leaving_ist else '---',
                             b.cost
                             ])

    # Send file via email
    msg = Message("Your Booking Export CSV", recipients=[user.email])
    msg.body = "Please find attached your booking history in CSV format."
    with open(filepath, 'rb') as f:
        msg.attach(filename, "text/csv", f.read())

    mail.send(msg)
    return filepath