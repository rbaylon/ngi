from baseapp import app
from models import NgiPerson
from controllers import NgiPersonController
from forms import NgiForm
from flask_login import login_required
from flask import render_template, request, redirect, url_for, abort
from datetime import datetime


@app.route("/members/<int:page_num>")
@login_required
def members(page_num):
    members = NgiPerson.query.paginate(per_page=100, page=page_num, error_out=True)
    return render_template('members.html',members=members)


@app.route("/member/add", methods=["GET", "POST"])
@login_required
def addmember():
    form = NgiForm()
    if form.validate_on_submit():
        controller = NgiPersonController()
        data = {'first_name': form.first_name.data, 'middle_name': form.middle_name.data,
                'last_name': form.last_name.data, 'pseudonym': form.pseudonym.data, 'gender': form.gender.data,
                'dob': form.dob.data, 'contact_number': form.contact_number.data, 'address': form.address.data,
                'ngi_number': form.ngi_number.data, 'member_since': form.member_since.data, 'rank': form.rank.data,
                'chapter': form.chapter.data}
        controller.add(data)
        return redirect(url_for('members', page_num=1))

    return render_template('member.html', form=form)


@app.route("/member/<int:person_id>", methods=["GET", "POST"])
@login_required
def editmember(person_id):
    form = NgiForm()
    person = NgiPerson.query.filter_by(id=person_id).first()
    if form.validate_on_submit():
        controller = NgiPersonController()
        if form.delete.data == 'Y':
            data = {'id': person.id}
            controller.delete(data)
            return redirect(url_for('members', page_num=1))
        else:
            data = {'first_name': form.first_name.data, 'middle_name': form.middle_name.data,
                    'last_name': form.last_name.data, 'pseudonym': form.pseudonym.data, 'gender': form.gender.data,
                    'dob': form.dob.data, 'contact_number': form.contact_number.data, 'address': form.address.data,
                    'ngi_number': form.ngi_number.data, 'member_since': form.member_since.data, 'rank': form.rank.data,
                    'chapter': form.chapter.data, 'id': person_id}
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
    form.chapter.data = person.chapter

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