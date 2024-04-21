import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import os 

smtp_server = 'smtp.gmail.com'  # Cambia esto al servidor SMTP que estés utilizando
smtp_port = 587  # Cambia esto al puerto adecuado
sender_email = 't510701220@unitru.edu.pe'
sender_password = 'wnjw sswr liaq bglv'#open('token.txt').read().strip()

# Detalles del correo electrónico
receiver_email = ['ailinsan2002@gmail.com']
subject = 'Envío de reporte de Reactiva'
body = 'Buenas tardes, Le adjunto lo solicitado'

# Crear el objeto MIMEMultipart
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ', '.join(receiver_email)
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))


# Adjuntar archivo
file_path = './ReactivaNuevo.xlsx'  # Cambia la ruta al archivo que quieras adjuntar
with open(file_path, 'rb') as file:
    attachment = MIMEApplication(file.read(), _subtype="xlsx")
    attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
    msg.attach(attachment)
    
# Iniciar la conexión con el servidor SMTP
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Iniciar el modo seguro
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print('Correo enviado exitosamente')