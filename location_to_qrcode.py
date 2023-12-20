import qrcode


def to_qrcode(location, message_id):
    # QR-kod yaratish
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Lokatsiyani ma'lumotlari orqali QR-kodni yaratish
    qr_data = f"Latitude: {location.latitude}, Longitude: {location.longitude}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    # QR-kodni rasmga olish
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # QR-kodni foydalanuvchiga yuborish
    user_id = message_id
    qr_image_path = f"qr.jpg"
    qr_image.save(qr_image_path)
