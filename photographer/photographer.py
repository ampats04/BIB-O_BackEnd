from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, render_template, redirect, url_for, flash, request
from strings import (
    NAME_EMPTY,
    ADDRESS_EMPTY,
    EMAIL_EMPTY,
    STATUS_EMPTY,
    PHOTOGRAPHER_EXISTS,
    PHOTOGRAPHER_REGISTERED_SUCCESSFULLY,
)


class photographer_obj:
    def __init__(self, event_organizer_id, name, address, email, password, status):

        self.event_orgainzer_id = event_organizer_id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        self.status = status


photographer = Blueprint("photographers", __name__)


@photographer.route("<event_organizer_id>/registration", methods=["GET", "POST"])
def register_photographer(event_organizer_id):

    data = request.form
    error = None

    if request.method == "POST":
        if data["name"] is None:
            error = NAME_EMPTY
        elif data["address"] is None:
            error = ADDRESS_EMPTY
        elif data["email"] is None:
            error = EMAIL_EMPTY
        elif data["status"] is None:
            error = STATUS_EMPTY

    if error is None:

        try:
            with engine.connect() as conn:
                query = text(
                    "INSERT INTO photographer(event_organizer_id, name, address, email, status) VALUES(:event_organizer_id, :name, :address, :email, :status)"
                )
                params = dict(
                    event_organizer_id=event_organizer_id,
                    name=data["name"],
                    address=data["address"],
                    email=data["email"],
                    status=data["status"],
                )

                conn.execute(query, params)

                conn.commit()
        except exc.IntegrityError as e:
            error = PHOTOGRAPHER_EXISTS

        else:
            redirect(
                url_for("photographer"), message=PHOTOGRAPHER_REGISTERED_SUCCESSFULLY
            )

    return render_template("photographer.vue")
