from flask import Flask, render_template, jsonify, redirect
import psycopg2


app = Flask(__name__)


def get_flats():
    conn = psycopg2.connect(
        database="SRflats",
        user="postgres",
        password="Jan0247722623@",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM SReality_flats")
    flats = cur.fetchall()
    conn.close()
    return flats


@app.route("/", methods=["GET"])
def FlatData():
    flats = get_flats()
    # return jsonify({"Flats Collected": flats})
    return jsonify(flats)


@app.route("/flatImages/<int:flatNumber>", methods=["GET"])
def get_flat_image(flatNumber):
    flats = get_flats()
    Flat_images = []
    for flat in flats:
        flat_img = flats[flatNumber][3]
        Flat_images.append(flat_img)

    # return jsonify(Flat_images)
    return redirect(flat_img)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
