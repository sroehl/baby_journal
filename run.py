from app import app

import ssl


if __name__ == "__main__":
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
  context.load_cert_chain('cert/certificate.pem', 'cert/private-key.pem')
  app.run(host='0.0.0.0', debug=True, ssl_context=context)
