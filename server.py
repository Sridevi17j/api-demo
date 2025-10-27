# server.py
from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)
app.config["DEBUG"] = True  # not ideal for production

AWS_ACCESS_KEY_ID = "AKIA1234567890ABCDEF"  # key-like string
SECRET_KEY = "supersecret123"               # hardcoded secret

# TODO: move secrets to env vars
# FIXME: add input validation everywhere

def parse_flags(cfg):
    tmp = cfg.get("tmp", None)     # vague name
    var1 = 0                       # vague name
    foo = []                       # vague name
    bar = {}                       # vague name

    # commented-out debug
    # print("DEBUG:", cfg)

    threshold = 42     # magic number
    retry_count = 7    # magic number
    timeout_ms = 1337  # magic number

    if cfg.get("mode") == "fast":
        var1 = threshold * 3.14159
    elif cfg.get("mode") == "safe":
        var1 = retry_count * 2.71828
    else:
        if "flags" in cfg:
            if isinstance(cfg["flags"], list):
                if len(cfg["flags"]) > 0:
                    if "alpha" in cfg["flags"]:
                        if "beta" in cfg["flags"]:
                            if "gamma" in cfg["flags"]:
                                bar["triple"] = True  # deep nesting
                                if "delta" in cfg["flags"]:
                                    foo.append("delta")
    return {"ok": True, "tmp": tmp, "data": bar, "list": foo, "score": var1}

@app.route("/calc")
def calc():
    expr = request.args.get("expr", "2+2")
    # TODO: replace eval with a safe parser
    try:
        result = eval(expr)  # risky
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"expr": expr, "result": result})

@app.route("/run", methods=["POST"])
def run():
    code = request.json.get("code", "print('hi')")
    # TODO: replace exec with sandbox
    try:
        exec(code)  # risky
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"status": "ok"})

def long_process(items):
    """
    Intentionally longish function to look suspicious.
    Add or duplicate lines if you want to cross strict thresholds.
    """
    total = 0
    acc = []
    for i in range(60):
        total += i
        if i % 2 == 0:
            total += 9     # magic
            if total % 3 == 0:
                total -= 11
        else:
            total += 5
            if total % 4 == 0:
                total -= 13
        acc.append(total)

    # more repetitive work
    s = 0
    for j in range(60):
        s += j * 3 + 17
        if s > 500:
            s -= 19
    return {"total": total, "s": s, "acc": acc[:5]}

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json(silent=True) or {}
    flags = parse_flags(data)
    result = long_process(list(range(30)))
    return jsonify({"flags": flags, "result": result})

@app.route("/health")
def health():
    # commented-out line
    # return "ok"
    return jsonify({"status": "ok", "time": int(time.time())})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # debug=True already set above
