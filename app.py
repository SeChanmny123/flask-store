from flask import Flask, render_template, request, redirect
import requests
from datetime import date
import urllib.parse

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def get_all():
    res = requests.get('https://fakestoreapi.com/products')  # Replace with actual API URL
    res_json = res.json()
    return render_template('components/card.html', product_list=res_json)


@app.route('/products_detail')
def get_product_detail():
    pid = request.args.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{pid}")  # Replace with actual API URL
    res_json = res.json()
    return render_template('layout/detail.html', product_detail=res_json)


@app.route('/checkout')
def checkout():
    pid = request.args.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{pid}")  # Replace with actual API URL
    res_json = res.json()
    return render_template('layout/confirm_booking.html', product_detail=res_json)


@app.post('/confirm_checkout')
def confirm_checkout():
    pid = request.form.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{pid}")  # Replace with actual API URL
    product = res.json()

    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    quantity = request.form.get('quantity')

    if quantity is None or quantity == '':
        quantity = 1
    else:
        quantity = int(quantity)

    total_price = product['price'] * quantity

    msg = (
        "<b>👟🛒 [ New Shoe Order ] 🛒👟</b>\n"
        "<b>👤 Name:</b> <code>{name}</code>\n"
        "<b>📞 Phone:</b> <code>{phone}</code>\n"
        "<b>✉️ Email:</b> <code>{email}</code>\n"
        "<b>🏠 Address:</b> <code>{address}</code>\n"
        "<b>📅 Date:</b> <code>{date}</code>\n"
        "<b>====================</b>\n"
        "<b>💥 Order Details 💥</b>\n"
        "<b>👟 Product:</b> <code>{product_name}</code>\n"
        "<b>🔢 Quantity:</b> <code>{quantity}</code>\n"
        "<b>💲 Price per Unit:</b> <code>${price}</code>\n"
        "<b>💰 Total Price:</b> <code>${total_price}</code>\n"
    ).format(
        name=name,
        phone=phone,
        email=email,
        address=address,
        date=date.today(),
        product_name=product['title'],
        quantity=quantity,
        price=product['price'],
        total_price=total_price
    )

    send_notification(msg)

    return redirect('/')


def send_notification(msg):
    bot_token = '6365928223:AAG5DAdImAU0oHurEjMsh5CXW8T6AEFIRhU'  # Replace with your Telegram bot token
    chat_id = '@shoestores123'  # Replace with your Telegram chat ID

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={urllib.parse.quote(msg)}&parse_mode=HTML"
    res = requests.get(url)
    return res


if __name__ == '__main__':
    app.run(debug=True)
