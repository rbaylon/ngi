from models import ChapterPayments
from baseapp import db


class ChapterPaymentsController:
    def __init__(self):
        pass

    def add(self, payment):
        existing = ChapterPayments.query.filter_by(received_from=payment['received_from'],
                                                   received_date=payment['received_date'],
                                                   payment_type=payment['payment_type'],
                                                   received_amount=payment['received_amount']).first()
        if not existing:
            new_payment.received_from = payment['received_from']
            new_payment.received_date = payment['received_date']
            new_payment.received_amount = payment['received_amount']
            new_payment.payment_type = payment['payment_type']
            new_payment.cpc = payment['cpc']
            new_payment.chapter = payment['chapter']
            db.session.add(new_payment)
            db.session.commit()
            return True

        return False

    def edit(self, payment):
        existing_payment = ChapterPayments.query.filter_by(id=payment['id']).first()
        if existing_payment:
            existing_payment.received_from = payment['received_from']
            existing_payment.received_date = payment['received_date']
            existing_payment.received_amount = payment['received_amount']
            existing_payment.payment_type = payment['payment_type']
            existing_payment.cpc = payment['cpc']
            existing_payment.chapter = payment['chapter']
            db.session.commit()
            return True

        return False

    def delete(self, payment):
        existing_payment = ChapterPayments.query.filter_by(id=payment['id']).first()
        if existing_payment:
            db.session.delete(existing_payment)
            db.session.commit()
            return True

        return False