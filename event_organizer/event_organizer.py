from functools import wraps
from flask import Blueprint, request, jsonify, session
from database import engine
from sqlalchemy import text
from strings import *

event_organizer = Blueprint("event_organizer", __name__)


@event_organizer.route("/register", methods=["GET", "POST"])
def register():
    data = request.form
    error = None

    if request.method == "POST":

        if data["name"] is None:
            response = jsonify(NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        elif data["address"] is None:
            response = jsonify(ADDRESS_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        elif data["email"] is None:
            response = jsonify(EMAIL_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        elif data["password"] is None:
            response = jsonify(PASSWORD_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        if error is None:
            with engine.connect() as conn:

                query = text(
                    "INSERT INTO event_organizer(name,address,email,password,datetime_created) VALUE (:name,:address,:email,:password, now())"
                )
                params = dict(
                    name=data["name"],
                    address=data["address"],
                    email=data["email"],
                    password=data["password"],
                )

                result = conn.execute(query, params)
                conn.commit()

                if result.rowcount > 0:
                    response = jsonify(REGISTRATION_SUCCESS)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response, 201
                else:
                    response = jsonify(REGISTRATION_UNSUCCESSFUL)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response, 400


# Update


@event_organizer.route("/update/<id>")
def update_event_organizer(id):

    data = request.form

    with engine.connect() as conn:

        query = text(
            "UPDATE event_organizer SET name = :name, address = :address, email =:email, password = :password WHERE id = :id"
        )
        params = dict(
            id=id,
            name=data["name"],
            address=data["address"],
            email=data["email"],
            password=data["password"],
        )

        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:
            response = jsonify(UPDATE_EVENT_ORGANIZER_SUCCESS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200
        else:

            response = jsonify(UPDATE_EVENT_ORGANIZER_UNSUCCESSFUL)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
