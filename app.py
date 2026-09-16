from flask import Flask, render_template, request, jsonify
import math
import random

app = Flask(__name__)

# Demo locations across the North-East Region.
LOCATIONS = [
    {"name":"Aizawl, Mizoram","lat":23.7271,"lon":92.7176,"elev":1132,"slope":38,"soil":"Clay/Loam","base_rain":185},
    {"name":"Gangtok, Sikkim","lat":27.3389,"lon":88.6065,"elev":1650,"slope":42,"soil":"Loam","base_rain":210},
    {"name":"Shillong, Meghalaya","lat":25.5788,"lon":91.8933,"elev":1496,"slope":31,"soil":"Laterite/Loam","base_rain":195},
    {"name":"Itanagar, Arunachal Pradesh","lat":27.0844,"lon":93.6053,"elev":440,"slope":36,"soil":"Sandy Loam","base_rain":220},
    {"name":"Kohima, Nagaland","lat":25.6751,"lon":94.1086,"elev":1261,"slope":34,"soil":"Loam","base_rain":175},
    {"name":"Imphal, Manipur","lat":24.8170,"lon":93.9368,"elev":786,"slope":22,"soil":"Clay/Loam","base_rain":145},
    {"name":"Agartala, Tripura","lat":23.8315,"lon":91.2868,"elev":16,"slope":9,"soil":"Alluvial","base_rain":160},
    {"name":"Guwahati, Assam","lat":26.1445,"lon":91.7362,"elev":55,"slope":18,"soil":"Alluvial/Loam","base_rain":155},
]

def risk_score(rainfall, intensity, slope, elevation, soil, landcover, drainage, historical):
    # Explainable weighted demo model. Replace with trained ML model later
    soil_factor = {
        "Clay/Loam": 0.75, "Laterite/Loam": 0.70, "Loam": 0.58,
        "Sandy Loam": 0.48, "Alluvial": 0.40
    }.get(soil, 0.55)
    land_factor = {"Dense Forest":0.20, "Agriculture":0.62, "Built-up":0.72, "Bare Land":0.90}.get(landcover,0.55)
    drainage_factor = {"Good":0.20, "Moderate":0.55, "Poor":0.90}.get(drainage,0.55)

    rain_component = min(rainfall/300, 1.0)
    intensity_component = min(intensity/60, 1.0)
    slope_component = min(slope/50, 1.0)
    elev_component = min(elevation/2000, 1.0)
    hist_component = min(historical/10, 1.0)

    raw = (
        0.28*rain_component +
        0.18*intensity_component +
        0.18*slope_component +
        0.07*elev_component +
        0.09*soil_factor +
        0.08*land_factor +
        0.07*drainage_factor +
        0.05*hist_component
    )
    score = round(min(99, max(1, raw*100)), 1)

    if score >= 70:
        level="HIGH"
        action="Issue early warning. Restrict movement in vulnerable slopes and inspect drainage/roads."
    elif score >= 45:
        level="MODERATE"
        action="Increase monitoring and prepare local response teams."
    else:
        level="LOW"
        action="Continue routine monitoring."

    return score, level, action

@app.route("/")
def index():
    return render_template("index.html", locations=LOCATIONS)

@app.route("/api/predict", methods=["POST"])
def predict():
    d=request.get_json(force=True)
    score, level, action = risk_score(
        float(d["rainfall"]), float(d["intensity"]), float(d["slope"]),
        float(d["elevation"]), d["soil"], d["landcover"], d["drainage"],
        float(d["historical"])
    )
    return jsonify({"score":score,"level":level,"action":action})

@app.route("/api/locations")
def locations():
    out=[]
    for x in LOCATIONS:
        # Generate deterministic demo conditions so markers stay stable during demo.
        seed=sum(ord(c) for c in x["name"])
        rng=random.Random(seed)
        rainfall=max(60, round(x["base_rain"] + rng.randint(-45,55)))
        intensity=max(8, round(rainfall/5 + rng.uniform(-8,8),1))
        score, level, action=risk_score(
            rainfall,intensity,x["slope"],x["elev"],x["soil"],
            rng.choice(["Dense Forest","Agriculture","Built-up","Bare Land"]),
            rng.choice(["Good","Moderate","Poor"]),rng.randint(0,10)
        )
        out.append({**x,"rainfall":rainfall,"intensity":intensity,
                    "score":score,"level":level})
    return jsonify(out)

if __name__ == "__main__":
    app.run(debug=True)
