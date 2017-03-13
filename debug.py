from app import app
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
context.load_cert_chain('cert/certificate.pem', 'cert/private-key.pem')
app.run(host='0.0.0.0', port=5001, debug=True, ssl_context=context)
