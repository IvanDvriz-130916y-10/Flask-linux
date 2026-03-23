import subprocess
import shlex
from flask import Flask, request, jsonify, Response

def create_app(testing=False):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="dev-secret-key",
        WTF_CSRF_ENABLED=False,
        TESTING=bool(testing),
    )

    @app.get("/")
    def home():
        return "<h3>Practice 4</h3><ul><li>POST /registration</li><li>GET /uptime</li><li>GET /ps?arg=a&arg=u&arg=x</li></ul>"

    @app.post("/registration")
    def register():
# берём данные из JSON или формы
        if request.is_json:
            data = request.get_json(silent=True) or {}
        else:
            data = request.form.to_dict(flat=True)

        from web.forms import RegistrationForm
        form = RegistrationForm(data=data)
        if not form.validate():
# собираем ошибки в плоский список
            errors_flat = []
            for fname, msgs in form.errors.items():
                for m in msgs:
                    errors_flat.append(f"{fname}: {m}")
            return jsonify({"errors": errors_flat, "field_errors": form.errors}), 400

        return jsonify({
            "status": "ok",
            "data": {
                "email": form.email.data,
                "phone": form.phone.data,
                "name": form.name.data,
                "address": form.address.data,
                "index": form.index.data,
                "comment": form.comment.data,
            }
        })

    @app.get("/uptime")
    def show_uptime():
        try:
            out = subprocess.run(["uptime", "-p"], capture_output=True, text=True, check=True).stdout
        except Exception as e:
            return f"Current uptime is unknown ({e})", 500
        pretty = out.strip().removeprefix("up ").strip()
        return f"Current uptime is {pretty}"

    @app.get("/ps")
    def run_ps():
        args = request.args.getlist("arg")
        cmd = ["ps"] + args
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            return "<pre>ps is not available</pre>", 500
        except Exception as err:
            return f"<pre>Error: {shlex.quote(str(err))}</pre>", 500
        out = (p.stdout or "") + (p.stderr or "")
        return f"<pre>{out}</pre>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)