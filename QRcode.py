import qrcode

# URL zu deinem GIF
url = "https://raw.githubusercontent.com/Schmotycs/AnimationDNA/main/dna_animation.gif"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("dna_qrcode.png")
