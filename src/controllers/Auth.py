from uuid import uuid4 as uuid
from marshmallow import ValidationError
from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from app import bcrypt
from models.User import User
from datetime import datetime, timedelta
from services.MailSender import MailSender
from interfaces.IUser import UserRegisterSchema, UserGetTokenSchema, UserLoginSchema

class AuthController:
    @jwt_required(refresh=True)
    def refresh(self):
        try:
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)
            response = make_response()
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response, 201
        except Exception as err:
            print(err)
            return jsonify({ 'message': 'Ocorreu um erro interno, entre em contato com o suporte.'}), 500

    def signin(self):
        try:
            data = request.json

            UserLoginSchema().load(data)

            email: str = data.get('email')
            password: str = data.get('password')
            code: str = data.get('code')

            user = User().get_user_by_email(email)

            if not user:
                return jsonify({ 'message': 'E-mail e/ou senha inválido(a)' }), 400

            if not user.verify_code(code):
                return jsonify({ 'message': 'Código inválido ou expirado' }), 400

            if user.verify_password(password):
                access_token = create_access_token(identity=user.uuid)
                refresh_token = create_refresh_token(identity=user.uuid)
                response = make_response({ 'message': 'Usuário autenticado com sucesso!' })
                response.set_cookie('access_token', access_token, httponly=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True)
                return response, 201
            else:
                return jsonify({ 'message': 'E-mail e/ou senha inválido(a)' }), 400
        
        except ValidationError as err:
            message = { 'message': list(err.messages.values())[0][0] }
            print(message)
            return jsonify(message), 400

        except Exception as err:
            print(err)
            return jsonify({ 'message': 'Ocorreu um erro interno, entre em contato com o suporte.'}), 500

    def signup(self):
        try:
            data = request.json

            UserRegisterSchema().load(data)

            name: str = data.get('name')
            email: str = data.get('email')
            password: str = data.get('password')

            user_already_exists = User().get_user_by_email(email)

            if user_already_exists:
                return jsonify({ 'message': 'E-mail já cadastrado' }), 409

            password_hash = bcrypt.generate_password_hash(password).decode()
            new_user = User(
                name=name,
                email=email,
                password=password_hash
            )

            if new_user.insert():
                return { 'message': 'Cadastro efetuado com sucesso' }, 201
            else:
                return { 'message': 'Ocorreu um erro e não foi possível efetuar o cadastro' }, 500
        
        except ValidationError as err:
            message = { 'message': list(err.messages.values())[0][0] }
            print(message)
            return jsonify(message), 400

        except Exception as err:
            print(err)
            return 'Ocorreu um erro interno, entre em contato com o suporte', 500

    def send_code(self):
        try:
            email = request.args.get('email')

            if not email: return { 'message': 'É necessário fornecer um endereço de e-mail' }, 400

            UserGetTokenSchema().load({ 'email': email })

            user = User().get_user_by_email(email)

            if user and user.code_expires and user.code_expires > datetime.now():
                time_left = int((user.code_expires-datetime.now()).total_seconds())
                return jsonify({ 'message': f'Aguarde {time_left} segundos para poder enviar novamente' }), 429

            code = str(uuid())[:6]

            mail = MailSender(email, code)
            
            if mail.send():
                User().update_access_code(email, code)
                
                return jsonify({ 'message': f'Um código com duração de 60s foi enviado para {email}' }), 200
            else:
                return jsonify({ 'message': f'Ocorreu um erro interno, entre em contato com o suporte' }), 500

        except ValidationError as err:
            message = { 'message': list(err.messages.values())[0][0] }
            print(message)
            return jsonify(message), 400

        except Exception as err:
            print(err)
            return jsonify({ 'message': f'Ocorreu um erro interno, entre em contato com o suporte' }), 500