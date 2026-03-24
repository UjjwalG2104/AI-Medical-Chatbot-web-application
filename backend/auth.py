"""
auth.py — Authentication endpoints for the Medical Chatbot using JWT.

Endpoints:
  POST /signup  — Create a new user account.
  POST /login   — Authenticate user and return a JWT.
"""

import os
import datetime
import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

def get_jwt_secret():
    return os.getenv("JWT_SECRET_KEY", "fallback-secret-key-change-in-prod")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(force=True)
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = current_app.db

    # Check if user already exists
    if db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    
    # Create the user
    user_record = {
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    db.users.insert_one(user_record)

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = current_app.db
    user = db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT
    token_payload = {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7) # Output token valid for 7 days
    }
    token = jwt.encode(token_payload, get_jwt_secret(), algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"email": user["email"]}
    }), 200
