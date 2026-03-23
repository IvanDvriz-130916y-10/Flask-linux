import argparse
from flask import Flask, request, jsonify
from web.executor import execute_python_code
from web.forms import ExecuteCodeForm

def make_app(custom_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="dev-secret-key",
        WTF_CSRF_ENABLED=False,
    )
    if custom_config:
        app.config.update(custom_config)

    @app.route("/")
    def home():
        return "Practice 5 is running. Use POST /execute with fields 'code' and 'timeout'."

    @app.post("/execute")
    def run_code():
# обрабатываем форму
        form = ExecuteCodeForm(meta={"csrf": False})
        form.process(data=request.form)
        if not form.validate():
            return jsonify({"ok": False, "errors": form.errors}), 400

# запускаем выполнение
        res = execute_python_code(form.code.data, int(form.timeout.data))

        if res.timed_out:
            return jsonify({
                "ok": True,
                "timed_out": True,
                "message": "Execution did not finish within the given timeout.",
                "stdout": res.stdout,
                "stderr": res.stderr,
                "returncode": res.returncode,
            })
        else:
            return jsonify({
                "ok": True,
                "timed_out": False,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "returncode": res.returncode,
            })

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    application = make_app()
    application.run(host="127.0.0.1", port=args.port, debug=False)