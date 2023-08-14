from flask_mail import Message
from app import mail

class MailSender:
    def __init__(self, recipent, msg):
        self.recipent = recipent
        self.msg = msg
    
    def send(self):
        try:
            msg = Message(
                subject=f'[Financial Control] Seu código de acesso',
                html=f'''
                    <!DOCTYPE html>
                    <html lang="pt-br">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    </head>
                    <body>
                        <div style="display: flex; justify-content: center;">
                            <p style="font-size: 1.5rem;">
                                Seu código de acesso: <b>{ ' '.join(list(self.msg.upper())) }</b>
                            </p>
                        </div>
                    </body>
                    </html>
                ''',
                recipients=[self.recipent]
            )

            mail.send(msg)
            return True
        except Exception as err:
            print(f'Erro ao enviar e-mail: {str(err)}')
            return False