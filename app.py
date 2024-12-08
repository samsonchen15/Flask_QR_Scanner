from flask import Flask, render_template, request, flash, redirect, url_for
import qrcode
import os

app = Flask(__name__)
QR_CODES_DIR = "static/qr_codes"
os.makedirs(QR_CODES_DIR, exist_ok=True)

app.secret_key = "your_secret_key" 

@app.route("/", methods=["GET", "POST"])

def index():
    qr_image_path = None
    desk_number = ""
    if request.method == "POST":
        data = request.form.get("data")
        if not data.isdigit() or len(data) != 6:
            flash("Desk must be a 6-digit number!", "error")
            return redirect(url_for("index"))

        qr = qrcode.QRCode(version=1, box_size=5, border=1)
        code = f'{{"roomAltld": "AST2-D{data}"}}'
        qr.add_data(code)
        qr.make(fit=True)

        # Save QR code to a file
        qr_image = qr.make_image(fill_color="black", back_color="white")
        file_name = f"QR_Code_{data}.png"
        qr_image_path = os.path.join(QR_CODES_DIR, file_name)
        qr_image.save(qr_image_path)

        desk_number = data

    return render_template("index.html", qr_image_path=qr_image_path, desk_number=desk_number)

if __name__ == "__main__":
    app.run(debug=True)