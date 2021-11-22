from baseapp import app
from models import NgiPerson, Chapter, ChapterPayments
from controllers import NgiPersonController, ChapterController, ChapterPaymentsController
from forms import NgiForm, ChapterForm, ChapterSelectForm, ChapterPaymentForm
from flask_login import login_required
from flask import render_template, request, redirect, url_for, abort
from datetime import datetime
from Utils.variables import cpc_amounts


@app.route("/members/<int:page_num>")
@login_required
def members(page_num):
    members = NgiPerson.query.paginate(per_page=500, page=page_num, error_out=True)
    return render_template('members.html',members=members)


@app.route("/member/add", methods=["GET", "POST"])
@login_required
def addmember():
    form = NgiForm()
    if form.validate_on_submit():
        controller = NgiPersonController()
        if form.chapter.data:
            chapter_name = form.chapter.data.name
        else:
            chapter_name = None
        data = {'first_name': form.first_name.data, 'middle_name': form.middle_name.data,
                'last_name': form.last_name.data, 'pseudonym': form.pseudonym.data, 'gender': form.gender.data,
                'dob': form.dob.data, 'contact_number': form.contact_number.data, 'address': form.address.data,
                'ngi_number': form.ngi_number.data, 'member_since': form.member_since.data, 'rank': form.rank.data,
                'chapter': chapter_name}
        controller.add(data)
        return redirect(url_for('members', page_num=1))

    return render_template('member.html', form=form)


@app.route("/member/<int:person_id>", methods=["GET", "POST"])
@login_required
def editmember(person_id):
    form = NgiForm()
    person = NgiPerson.query.get_or_404(person_id)
    if form.validate_on_submit():
        controller = NgiPersonController()
        if form.delete.data == 'Y':
            data = {'id': person.id}
            controller.delete(data)
            return redirect(url_for('members', page_num=1))
        else:
            if form.chapter.data:
                chapter_name = form.chapter.data.name
            else:
                chapter_name = None
            data = {'first_name': form.first_name.data, 'middle_name': form.middle_name.data,
                    'last_name': form.last_name.data, 'pseudonym': form.pseudonym.data, 'gender': form.gender.data,
                    'dob': form.dob.data, 'contact_number': form.contact_number.data, 'address': form.address.data,
                    'ngi_number': form.ngi_number.data, 'member_since': form.member_since.data, 'rank': form.rank.data,
                    'chapter': chapter_name, 'id': person_id}
            controller.edit(data)
            return redirect(url_for('members', page_num=1))

    form.first_name.data = person.person.FirstName
    form.middle_name.data = person.person.MiddleName
    form.last_name.data = person.person.LastName
    form.pseudonym.data = person.pseudonym
    form.gender.data = person.person.gender
    form.dob.data = datetime.strptime(person.person.dob, "%Y-%m-%d").date()
    form.contact_number.data = person.contact_number
    form.address.data = person.address
    form.ngi_number.data = person.ngi_number
    form.member_since.data = datetime.strptime(person.member_since, "%Y-%m-%d").date()
    form.rank.data = person.rank
    form.chapter.data = Chapter.query.filter_by(name=person.chapter).first()

    delete = request.args.get('delete', None)
    edit = request.args.get('edit', None)
    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    if edit:
        form.edit.data = 'Y'
    else:
        form.edit.data = 'N'

    return render_template('member.html', form=form, person_id=person.id)


@app.route("/chapters/<int:page_num>")
@login_required
def chapters(page_num):
    chapters = Chapter.query.paginate(per_page=100, page=page_num, error_out=True)
    return render_template('chapters.html',chapters=chapters)


@app.route("/chapter/add", methods=["GET", "POST"])
@login_required
def addchapter():
    form = ChapterForm()
    if form.validate_on_submit():
        controller = ChapterController()
        data = {'name': form.name.data, 'founder': form.founder.data, 'founded': form.founded.data}
        controller.add(data)
        return redirect(url_for('chapters', page_num=1))

    return render_template('chapter.html', form=form)


@app.route("/chapter/<int:chapter_id>", methods=["GET", "POST"])
@login_required
def editchapter(chapter_id):
    form = ChapterForm()
    chapter = Chapter.query.get_or_404(chapter_id)
    if form.validate_on_submit():
        controller = ChapterController()
        if form.delete.data == 'Y':
            data = {'id': chapter.id}
            controller.delete(data)
            return redirect(url_for('chapters', page_num=1))
        else:
            data = {'name': form.name.data, 'founder': form.founder.data,
                    'founded': form.founded.data, 'id': chapter_id}
            controller.edit(data)
            return redirect(url_for('chapters', page_num=1))

    form.name.data = chapter.name
    form.founder.data = chapter.founder
    form.founded.data = datetime.strptime(chapter.founded, "%Y-%m-%d").date()

    delete = request.args.get('delete', None)
    edit = request.args.get('edit', None)
    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    if edit:
        form.edit.data = 'Y'
    else:
        form.edit.data = 'N'

    return render_template('chapter.html', form=form, chapter_id=chapter.id)


@app.route("/chapter/payments/<int:chapter_id>")
@login_required
def chapter_payments(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter_payments = ChapterPayments.query.filter_by(chapter=chapter.name).all()
    payments = []
    total_chapter_share = 0
    total_cpc_share = 0
    for p in chapter_payments:
        data = {
            'received_from': p.received_from,
            'received_date': p.received_date,
            'received_amount': p.received_amount,
            'payment_type': p.payment_type,
            'cpc': p.cpc,
            'chapter': p.chapter,
            'id': int(p.id)
        }
        if p.payment_type in cpc_amounts:
            cpc_share = float(cpc_amounts[p.payment_type])
            chapter_share = float(p.received_amount) - cpc_share
        else:
            cpc_share = 0
            chapter_share = float(p.received_amount)

        data['cpc_share'] = cpc_share
        data['chapter_share'] = chapter_share
        total_chapter_share += chapter_share
        total_cpc_share += cpc_share
        payments.append(data)
        all_data = {'payments': payments, 'total_cpc': total_cpc_share, 'total_chapter': total_chapter_share}
    return render_template('chapter_payments.html', chapter_payments=all_data, chapter_id=chapter_id)


@app.route("/chapters/accounting", methods=["GET", "POST"])
@login_required
def chapters_select():
    form = ChapterSelectForm()
    if form.validate_on_submit():
        return redirect(url_for('chapter_payments', chapter_id=form.chapter.data.id))

    return render_template('chapters_select.html', form=form)


@app.route("/chapter/accounting/add/<int:chapter_id>", methods=["GET", "POST"])
@login_required
def addchapter_payment(chapter_id):
    form = ChapterPaymentForm()
    chapter = Chapter.query.get_or_404(chapter_id)
    form.received_from.query_factory = NgiPerson.query.filter_by(chapter=chapter.name).all
    if form.validate_on_submit():
        controller = ChapterPaymentsController()
        data = {'received_from': form.received_from.data.__str__(), 'received_date': str(form.received_date.data),
                'received_amount': str(form.received_amount.data), 'payment_type': form.payment_type.data,
                'cpc': form.cpc.data, 'chapter': chapter.name}

        controller.add(data)
        return redirect(url_for('chapter_payments', chapter_id=chapter.id))

    form.chapter.data = chapter
    return render_template('chapter_payment.html', form=form, chapter_id=chapter.id)


@app.route("/chapter/accounting/<int:payment_id>", methods=["GET", "POST"])
@login_required
def editchapter_payment(payment_id):
    form = ChapterPaymentForm()
    payment = ChapterPayments.query.get_or_404(payment_id)
    chapter = Chapter.query.filter_by(name=payment.chapter).first()
    form.received_from.query_factory = NgiPerson.query.filter_by(chapter=chapter.name).all
    if form.validate_on_submit():
        controller = ChapterPaymentsController()
        if form.delete.data == 'Y':
            data = {'id': payment.id}
            controller.delete(data)
            return redirect(url_for('chapter_payments', chapter_id=chapter.id))
        else:
            data = {'received_from': form.received_from.data.__str__(), 'received_date': str(form.received_date.data),
                    'received_amount': str(form.received_amount.data), 'payment_type': form.payment_type.data,
                    'cpc': form.cpc.data, 'chapter': chapter.name, 'id': payment_id}
            controller.edit(data)
            return redirect(url_for('chapter_payments', chapter_id=chapter.id))

    persons = NgiPerson.query.filter_by(chapter=chapter.name).all()
    for person in persons:
        if person.__str__() == payment.received_from:
            form.received_from.data = person
            break

    form.received_date.data = datetime.strptime(payment.received_date, "%Y-%m-%d").date()
    form.received_amount.data = float(payment.received_amount)
    form.payment_type.data = payment.payment_type
    form.cpc.data = payment.cpc
    form.chapter.data = Chapter.query.filter_by(name=chapter.name).first()

    delete = request.args.get('delete', None)
    edit = request.args.get('edit', None)
    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    if edit:
        form.edit.data = 'Y'
    else:
        form.edit.data = 'N'

    return render_template('chapter_payment.html', form=form, payment_id=payment.id)
