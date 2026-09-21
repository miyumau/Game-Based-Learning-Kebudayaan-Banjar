from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "kunci_rahasia_flask"

# ============================
# KONFIGURASI DATABASE
# ============================
app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://root:@localhost:3307/projek_ppl"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ============================
# MODEL DATABASE
# ============================

# Tabel Siswa
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Tabel Guru (Hanya bisa ditambah manual lewat database)
class Guru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_guru = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class QuizProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), nullable=False)
    stage = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer, default=0) 

class TebakProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), nullable=False)
    stage = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer, default=0)

class MatchingProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), nullable=False)
    stage = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer, default=0)

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    total_score = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())

# Pastikan semua tabel terbuat
with app.app_context():
    db.create_all()

# ============================
# FUNGSI(LOGIKANYA)
# ============================

def update_leaderboard_logic():
    """Menarik data dari tabel progress dan memperbarui tabel Leaderboard secara fisik"""
    users = User.query.all()
    for user in users:
        # Hitung skor total hanya yang statusnya passed=True
        score_quiz = db.session.query(db.func.sum(QuizProgress.score)).filter_by(user_email=user.email, passed=True).scalar() or 0
        score_tebak = db.session.query(db.func.sum(TebakProgress.score)).filter_by(user_email=user.email, passed=True).scalar() or 0
        score_match = db.session.query(db.func.sum(MatchingProgress.score)).filter_by(user_email=user.email, passed=True).scalar() or 0
        
        total = score_quiz + score_tebak + score_match
        
        # Cari di tabel Leaderboard
        entry = Leaderboard.query.filter_by(email=user.email).first()
        if entry:
            entry.total_score = total
            entry.username = user.username
            entry.last_updated = db.func.current_timestamp()
        else:
            new_entry = Leaderboard(username=user.username, email=user.email, total_score=total)
            db.session.add(new_entry)
    db.session.commit()

# ============================
# AUTHENTICATION
# ============================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # 1. Cek di tabel Siswa (User)
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session.update({"user": email, "username": user.username, "role": "siswa"})
            return redirect(url_for("home"))

        # 2. Cek di tabel Guru
        guru = Guru.query.filter_by(email=email).first()
        if guru and bcrypt.check_password_hash(guru.password, password):
            session.update({"user": email, "username": guru.nama_guru, "role": "guru"})
            return redirect(url_for("halaman_guru"))

        return render_template("base.html", error="Email atau Password salah!")
    return render_template("base.html")

@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        db.session.add(User(username=username, email=email, password=hashed))
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("pages/signup.html")

# ============================
# DASHBOARD GURU LAWAN LEADERBOARD API
# ============================

@app.route("/guru")
def halaman_guru():
    if "user" not in session or session.get("role") != "guru":
        return "Akses Ditolak!", 403
    
    # maambil data semua siswa untuk dashboard statistik
    semua_siswa = User.query.all()
    statistik_siswa = []
    for siswa in semua_siswa:
        q = QuizProgress.query.filter_by(user_email=siswa.email, passed=True).all()
        t = TebakProgress.query.filter_by(user_email=siswa.email, passed=True).all()
        m = MatchingProgress.query.filter_by(user_email=siswa.email, passed=True).all()
        
        statistik_siswa.append({
            "username": siswa.username,
            "email": siswa.email,
            "quiz": max([i.stage for i in q]) if q else 0,
            "tebak": max([i.stage for i in t]) if t else 0,
            "match": max([i.stage for i in m]) if m else 0,
            "score": sum([i.score for i in q+t+m]),
            "time": sum([i.time_taken for i in q+t+m])
        })
    return render_template("pages/guru.html", statistik=statistik_siswa)

@app.route("/api/leaderboard_data")
def leaderboard_data():
    """Mengambil data 10 besar langsung dari tabel Leaderboard fisik"""
    update_leaderboard_logic() # Sinkronisasi data dulu
    top = Leaderboard.query.order_by(Leaderboard.total_score.desc()).limit(10).all()
    return jsonify([{"username": p.username, "email": p.email, "total_score": p.total_score} for p in top])

# ============================
# LOGIKA GAME & PROGRESS
# ============================

@app.route("/home")
def home():
    if "user" not in session: return redirect(url_for("login"))
    e = session["user"]
    q = QuizProgress.query.filter_by(user_email=e, passed=True).all()
    t = TebakProgress.query.filter_by(user_email=e, passed=True).all()
    m = MatchingProgress.query.filter_by(user_email=e, passed=True).all()
    
    return render_template("pages/home.html", 
        max_stage_quiz=max([i.stage for i in q]) if q else 0, score_quiz=sum([i.score for i in q]),
        max_stage_tebak=max([i.stage for i in t]) if t else 0, score_tebak=sum([i.score for i in t]),
        max_stage_matching=max([i.stage for i in m]) if m else 0, score_match=sum([i.score for i in m]),
        total_detik=sum([i.time_taken for i in q+t+m]))

@app.route("/api/submit_quiz", methods=["POST"])
def submit_quiz():
    if "user" not in session: return jsonify({"status": "error"}), 401
    data = request.get_json()
    g_name = data.get("game_name")
    stage = data.get("stage")
    score = data.get("score")
    total = data.get("total_soal")
    time = data.get("time_taken", 0)
    
    is_passed = score > 0 if g_name in ["tebak", "matching"] else score >= (total / 2)
    Model = {"quiz": QuizProgress, "tebak": TebakProgress, "matching": MatchingProgress}.get(g_name)
    
    exist = Model.query.filter_by(user_email=session["user"], stage=stage).first()
    if exist:
        if score > exist.score or (is_passed and not exist.passed):
            exist.score, exist.passed, exist.time_taken = score, is_passed, time
    else:
        db.session.add(Model(user_email=session["user"], stage=stage, score=score, passed=is_passed, time_taken=time))
    
    db.session.commit()
    update_leaderboard_logic() # Otomatis sinkronkan ke tabel Leaderboard
    return jsonify({"status": "success", "passed": is_passed})

# ============================
# ROUTES NAVIGASI & DYNAMIS
# ============================

@app.route("/game")
def game():
    if "user" not in session: return redirect(url_for("login"))
    u_t = QuizProgress.query.filter_by(user_email=session["user"], stage=5, passed=True).first()
    u_m = TebakProgress.query.filter_by(user_email=session["user"], stage=9, passed=True).first()
    return render_template("pages/game.html", unlock_tebak=bool(u_t), unlock_matching=bool(u_m))

@app.route("/quiz")
def quiz():
    p = QuizProgress.query.filter_by(user_email=session["user"], passed=True).all()
    return render_template("pages/quiz.html", max_stage=(max([i.stage for i in p]) + 1 if p else 1))

@app.route("/tebak_gambar")
def tebak_gambar():
    p = TebakProgress.query.filter_by(user_email=session["user"], passed=True).all()
    return render_template("pages/tebak_gambar.html", max_stage=(max([i.stage for i in p]) + 1 if p else 1))

@app.route("/matching")
def matching():
    p = MatchingProgress.query.filter_by(user_email=session["user"], passed=True).all()
    return render_template("pages/matching.html", max_stage=(max([i.stage for i in p]) + 1 if p else 1))

@app.route("/leaderboard")
def leaderboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("pages/leaderboard.html")

# Dynamic Routes Generator (Game Pages)
for i in range(1, 11):
    app.add_url_rule(f"/quiz_{i}", f"quiz_{i}", lambda i=i: render_template(f"pages/quiz_{i}.html") if "user" in session else redirect(url_for("login")))
    app.add_url_rule(f"/tebak_gambar_{i}", f"tebak_gambar_{i}", lambda i=i: render_template(f"pages/tebak_gambar_{i}.html") if "user" in session else redirect(url_for("login")))
    app.add_url_rule(f"/matching_{i}", f"matching_{i}", lambda i=i: render_template(f"pages/matching_{i}.html") if "user" in session else redirect(url_for("login")))

# Materi Routes
materis = ["materi", "profil", "rumah_adat", "kue_banjar", "kumpulan_rumah", "rumah_bubungan_tinggi", "rumah_balai_laki", "rumah_gajah_baliku", "rumah_palimasan", "kumpulan_kue", "rumah_balai_bini", "wadai_cincin", "wadai_putu_mayang"]
for m in materis:
    app.add_url_rule(f"/{m}", m, lambda m=m: render_template(f"pages/{m}.html") if "user" in session else redirect(url_for("login")))

if __name__ == "__main__":
    app.run(debug=True)