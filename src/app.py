from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")

MUP_header = ["military_id", "name", "start_date", "end_date"]
MUP = [
    [0, "Khalid Tarek", "2/1/2023", "1/3/2024"],
    [1, "Hassan Mohammedi", "2/1/2023", "1/3/2024"],
    [2, "Alaa Fathi", "2/1/2023", "1/3/2024"],
    [3, "Basel Elsayed", "2/1/2023", "1/3/2024"],
]

@app.route('/')
def hello_world():
    return render_template("index.html", MUP_header=MUP_header, MUP=MUP)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)