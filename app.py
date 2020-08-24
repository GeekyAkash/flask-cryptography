from flask import Flask, render_template, request, flash
from forms import Encryption, Decryption
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)

app.config['SECRET_KEY'] = '952105ede0cb72feb223ed9c15efd61e'

BLOCK_SIZE = 16

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template("main.html")


@app.route('/encryption', methods=['GET', 'POST'])
def encryption():
    form = Encryption(request.form)
    if len(form.message.data) > 1000:
        message = flash("Maximum Number of Words must be 1000")
        return render_template('Encryption.html', title='Encryption', message=message, form=form)

    if  form.validate_on_submit():
        encrypt_message = encrypt(form.message.data, form.password.data)
        return encrypt_message

    if request.method == 'GET':
        return render_template('Encryption.html', title='Encryption', form=form)


@app.route('/decryption', methods=['GET', 'POST'])
def decryption():
    form = Decryption(request.form)
    if  form.validate_on_submit():
        decrypt_message = decrypt(form.message.data, form.password.data)
        return decrypt_message

    if request.method == 'GET':
        return render_template('Decryption.html', title='Decryption', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()