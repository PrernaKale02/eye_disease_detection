# ============================================================
# keywords_config.py
# Keyword maps for all 4 eye diseases:
#   DR       (5 classes: 0-4)
#   DME      (3 classes: 0-2)
#   Glaucoma (2 classes: 0-1)
#   Cataract (4 classes: 0-3)
# ============================================================


# ────────────────────────────────────────────────────────────
# 1. DIABETIC RETINOPATHY  (class 0-4)
# ────────────────────────────────────────────────────────────
DR_KEYWORD_MAP = {
    0: {  # No DR
        "base":       ["clear retinal vessels", "no lesions detected",
                       "healthy optic disc", "normal macula"],
        "macula":     ["normal foveal reflex", "clear central vision zone"],
        "optic_disc": ["healthy disc margins", "normal cup-to-disc ratio"],
        "peripheral": ["no peripheral hemorrhages", "clean peripheral vessels"],
        "superior":   ["no superior vessel abnormalities"],
        "inferior":   ["no inferior lesions"],
    },
    1: {  # Mild NPDR
        "base":       ["microaneurysms", "dot hemorrhages", "early vessel changes"],
        "macula":     ["peri-foveal microaneurysms", "macular proximity lesions"],
        "optic_disc": ["peripapillary hemorrhages", "disc-margin vessel changes"],
        "peripheral": ["scattered peripheral microaneurysms"],
        "superior":   ["superior quadrant dot hemorrhages"],
        "inferior":   ["inferior retinal microaneurysms"],
    },
    2: {  # Moderate NPDR
        "base":       ["microaneurysms", "intraretinal hemorrhages",
                       "hard exudates", "cotton-wool spots"],
        "macula":     ["macular hard exudates", "CSME risk", "foveal threat"],
        "optic_disc": ["peripapillary hard exudates", "nerve fiber layer hemorrhages"],
        "peripheral": ["blot hemorrhages", "venous beading"],
        "superior":   ["superior flame-shaped hemorrhages"],
        "inferior":   ["inferior IRMA"],
    },
    3: {  # Severe NPDR
        "base":       ["extensive hemorrhages", "venous beading",
                       "IRMA", "cotton-wool spots"],
        "macula":     ["macular ischemia", "severe macular edema"],
        "optic_disc": ["disc neovascularization risk", "peripapillary IRMA"],
        "peripheral": ["4-quadrant hemorrhages", "extensive peripheral IRMA"],
        "superior":   ["superior venous beading"],
        "inferior":   ["inferior vessel occlusion signs"],
    },
    4: {  # Proliferative DR (PDR)
        "base":       ["neovascularization", "fibrous proliferation",
                       "vitreous hemorrhage risk", "retinal traction"],
        "macula":     ["tractional macular detachment risk", "NVD near disc"],
        "optic_disc": ["neovascularization of the disc (NVD)",
                       "disc fibrovascular proliferation"],
        "peripheral": ["neovascularization elsewhere (NVE)", "pre-retinal hemorrhage"],
        "superior":   ["superior fibrovascular membranes"],
        "inferior":   ["inferior retinal traction"],
    },
}

DR_CLASS_NAMES = ["No DR", "Mild NPDR", "Moderate NPDR", "Severe NPDR", "PDR"]

DR_EXPLANATION_TEMPLATES = {
    0: ("The retinal image shows no signs of diabetic retinopathy. "
        "Analysis reveals {kw}. "
        "Grad-CAM heatmap confirms no abnormal activation in critical retinal zones."),
    1: ("Mild NPDR detected with {conf:.0%} confidence. "
        "The heatmap highlights the {zones}, identifying {kw}. "
        "These are early microvascular changes, not immediately sight-threatening."),
    2: ("Moderate NPDR detected with {conf:.0%} confidence. "
        "Grad-CAM focuses on the {zones}, identifying {kw}. "
        "Progressive microvascular damage — closer monitoring required."),
    3: ("Severe NPDR detected with {conf:.0%} confidence. "
        "Extensive activation across the {zones} corresponds to {kw}. "
        "High risk (>50%) of progression to PDR within 1 year."),
    4: ("PDR detected with {conf:.0%} confidence — most sight-threatening stage. "
        "Critical activation in the {zones} driven by {kw}. "
        "Immediate ophthalmological intervention essential."),
}

DR_RISK_INFO = {
    0: {"level": "No risk",       "color": "#639922"},
    1: {"level": "Low risk",      "color": "#BA7517"},
    2: {"level": "Moderate risk", "color": "#EF9F27"},
    3: {"level": "High risk",     "color": "#E24B4A"},
    4: {"level": "Severe risk",   "color": "#A32D2D"},
}

DR_CLINICAL_ADVICE = {
    0: "Routine annual screening. Maintain HbA1c < 7%.",
    1: "Repeat screening in 9-12 months. Optimize glycemic and BP control.",
    2: "Ophthalmology referral within 3 months. Monitor for macular edema.",
    3: "Urgent referral within 1 month. Consider pan-retinal photocoagulation (PRP).",
    4: "IMMEDIATE referral. Laser / anti-VEGF / vitrectomy to prevent blindness.",
}


# ────────────────────────────────────────────────────────────
# 2. DIABETIC MACULAR EDEMA — DME  (class 0-2)
# ────────────────────────────────────────────────────────────
DME_KEYWORD_MAP = {
    0: {  # No DME
        "base":       ["no macular thickening", "normal central retinal thickness",
                       "dry macula", "no subretinal fluid"],
        "macula":     ["normal foveal contour", "intact photoreceptor layer",
                       "no intraretinal cysts", "normal OCT profile"],
        "optic_disc": ["no peripapillary edema", "normal disc appearance"],
        "peripheral": ["no peripheral exudative changes"],
        "superior":   ["no superior macular fluid"],
        "inferior":   ["no inferior subretinal fluid"],
    },
    1: {  # Mild / Non-center-involving DME
        "base":       ["mild macular thickening", "hard exudates near macula",
                       "early intraretinal fluid", "non-center-involving edema"],
        "macula":     ["parafoveal hard exudates", "mild foveal thickening",
                       "early cystoid changes", "peri-foveal fluid pockets"],
        "optic_disc": ["peripapillary exudates", "mild disc vessel leakage"],
        "peripheral": ["exudate rings near vascular arcades"],
        "superior":   ["superior arcade hard exudates"],
        "inferior":   ["inferior macular hard exudate deposits"],
    },
    2: {  # Severe / Center-involving DME
        "base":       ["center-involving macular edema", "severe retinal thickening",
                       "cystoid macular edema (CME)", "subretinal fluid accumulation"],
        "macula":     ["foveal cysts", "disrupted ellipsoid zone",
                       "subfoveal fluid", "loss of foveal depression",
                       "hyperreflective foci at fovea"],
        "optic_disc": ["disc neovascularization-associated edema",
                       "peripapillary fluid leakage"],
        "peripheral": ["circumferential hard exudate rings",
                       "diffuse retinal thickening at arcades"],
        "superior":   ["superior foveal fluid extension"],
        "inferior":   ["inferior retinal detachment risk from fluid"],
    },
}

DME_CLASS_NAMES = ["No DME", "Mild DME", "Severe DME"]

DME_EXPLANATION_TEMPLATES = {
    0: ("No diabetic macular edema detected. "
        "The macular region appears normal with {kw}. "
        "Grad-CAM shows no pathological activation in the foveal zone."),
    1: ("Mild DME detected with {conf:.0%} confidence. "
        "Heatmap highlights the {zones}, revealing {kw}. "
        "Central vision is not yet compromised but requires close monitoring."),
    2: ("Severe center-involving DME detected with {conf:.0%} confidence. "
        "Critical Grad-CAM activation at the {zones} corresponding to {kw}. "
        "Immediate anti-VEGF or laser treatment required to prevent vision loss."),
}

DME_RISK_INFO = {
    0: {"level": "No risk",       "color": "#639922"},
    1: {"level": "Moderate risk", "color": "#EF9F27"},
    2: {"level": "Severe risk",   "color": "#A32D2D"},
}

DME_CLINICAL_ADVICE = {
    0: "No treatment needed. Annual dilated eye exam recommended.",
    1: "Ophthalmology review in 1-3 months. Optimize blood sugar and blood pressure.",
    2: "URGENT: Anti-VEGF injections (ranibizumab/bevacizumab) or focal laser. Refer immediately.",
}


# ────────────────────────────────────────────────────────────
# 3. GLAUCOMA  (class 0=No Glaucoma, 1=Glaucoma)
# ────────────────────────────────────────────────────────────
GLAUCOMA_KEYWORD_MAP = {
    0: {  # No Glaucoma
        "base":       ["normal optic disc", "normal cup-to-disc ratio (CDR < 0.5)",
                       "intact neuroretinal rim", "no disc pallor"],
        "macula":     ["no glaucomatous macular defect", "normal ganglion cell layer"],
        "optic_disc": ["healthy optic disc margins", "pink neuroretinal rim",
                       "normal CDR", "no disc hemorrhage", "no notching"],
        "peripheral": ["full peripheral visual field", "no arcuate nerve fiber loss"],
        "superior":   ["intact superior neuroretinal rim"],
        "inferior":   ["intact inferior neuroretinal rim"],
    },
    1: {  # Glaucoma
        "base":       ["enlarged cup-to-disc ratio (CDR > 0.6)", "optic nerve cupping",
                       "neuroretinal rim thinning", "disc pallor"],
        "macula":     ["macular ganglion cell complex thinning",
                       "glaucomatous macular damage", "central visual field defect"],
        "optic_disc": ["vertical CDR enlargement", "disc hemorrhage (Drance hemorrhage)",
                       "inferior/superior notching", "nasal shifting of vessels",
                       "bean-pot cupping", "laminar dot sign",
                       "peripapillary atrophy (PPA)"],
        "peripheral": ["retinal nerve fiber layer (RNFL) defect",
                       "arcuate scotoma pattern", "peripheral field loss"],
        "superior":   ["superior RNFL thinning", "inferior arcuate nerve fiber defect"],
        "inferior":   ["inferior RNFL thinning", "superior visual field loss",
                       "inferior notching of rim"],
    },
}

GLAUCOMA_CLASS_NAMES = ["No Glaucoma", "Glaucoma"]

GLAUCOMA_EXPLANATION_TEMPLATES = {
    0: ("No glaucoma detected. "
        "The optic disc appears healthy with {kw}. "
        "Grad-CAM shows no abnormal activation around the disc."),
    1: ("Glaucoma detected with {conf:.0%} confidence. "
        "Grad-CAM strongly activates the {zones}, revealing {kw}. "
        "These structural changes indicate progressive optic nerve damage."),
}

GLAUCOMA_RISK_INFO = {
    0: {"level": "No risk", "color": "#639922"},
    1: {"level": "Moderate risk", "color": "#EF9F27"}
}

GLAUCOMA_CLINICAL_ADVICE = {
    0: "Routine annual IOP check. Baseline optic disc photography recommended.",
    1: ("URGENT: IOP measurement, visual field test, OCT of optic nerve. "
        "Start IOP-lowering therapy (eye drops / laser trabeculoplasty / surgery)."),
}


# ────────────────────────────────────────────────────────────
# 4. CATARACT  (class 0-1)
# ────────────────────────────────────────────────────────────
CATARACT_KEYWORD_MAP = {
    0: {
        "base": ["clear lens", "no lens opacity"],
        "macula": ["clear macular view"],
        "optic_disc": ["clearly visible optic disc"],
    },

    1: {
        "base": ["lens opacity", "reduced lens transparency"],
        "macula": ["hazy macular view"],
        "optic_disc": ["reduced fundus clarity"],
    }
}

CATARACT_CLASS_NAMES = ["No Cataract", "Cataract Detected"]

CATARACT_EXPLANATION_TEMPLATES = {
    0: ("No cataract detected. "
        "The lens appears transparent with {kw}. "
        "Grad-CAM shows no opacity-related activation patterns."),

    1: ("Cataract detected with {conf:.0%} confidence. "
        "Grad-CAM highlights lens opacity patterns corresponding to {kw}. "
        "Clinical evaluation recommended to determine cataract severity.")
}

CATARACT_RISK_INFO = {
    0: {"level": "No risk", "color": "#639922"},
    1: {"level": "Moderate risk", "color": "#EF9F27"}
}

CATARACT_CLINICAL_ADVICE = {
    0: "No intervention needed. Routine eye exam in 1-2 years.",
    1: "Monitor every 6 months. Updated glasses prescription. Avoid bright glare.",
    2: "Cataract surgery (phacoemulsification + IOL) recommended. Refer to ophthalmologist.",
    3: "URGENT surgery required. Risk of phacolytic glaucoma and spontaneous rupture.",
}


# ────────────────────────────────────────────────────────────
# SHARED ZONE DESCRIPTIONS
# ────────────────────────────────────────────────────────────
ZONE_DESCRIPTIONS = {
    "macula":     "macular region (central vision area)",
    "optic_disc": "optic disc region",
    "peripheral": "peripheral retina",
    "superior":   "superior retinal quadrant",
    "inferior":   "inferior retinal quadrant",
}


# ────────────────────────────────────────────────────────────
# MASTER DISEASE CONFIG — used by pipeline to route correctly
# ────────────────────────────────────────────────────────────
DISEASE_CONFIG = {
    "Diabetic Retinopathy": {
        "keyword_map": DR_KEYWORD_MAP,
        "class_names": DR_CLASS_NAMES,
        "templates":   DR_EXPLANATION_TEMPLATES,
        "risk_info":   DR_RISK_INFO,
        "clinical":    DR_CLINICAL_ADVICE,
        "model_key":   "dr",
        "preprocess":  "resnet",
        "last_conv":   "conv5_block3_out",
        "framework":   "tensorflow",
    },
    "Diabetic Macular Edema": {
        "keyword_map": DME_KEYWORD_MAP,
        "class_names": DME_CLASS_NAMES,
        "templates":   DME_EXPLANATION_TEMPLATES,
        "risk_info":   DME_RISK_INFO,
        "clinical":    DME_CLINICAL_ADVICE,
        "model_key":   "dme",
        "preprocess":  "resnet",
        "last_conv":   None,          # PyTorch — uses features[-1]
        "framework":   "pytorch",
    },
    "Glaucoma": {
        "keyword_map": GLAUCOMA_KEYWORD_MAP,
        "class_names": GLAUCOMA_CLASS_NAMES,
        "templates":   GLAUCOMA_EXPLANATION_TEMPLATES,
        "risk_info":   GLAUCOMA_RISK_INFO,
        "clinical":    GLAUCOMA_CLINICAL_ADVICE,
        "model_key":   "glaucoma",
        "preprocess":  "efficientnet",
        "last_conv":   "top_conv",
        "framework":   "tensorflow",
    },
    "Cataract": {
        "keyword_map": CATARACT_KEYWORD_MAP,
        "class_names": CATARACT_CLASS_NAMES,
        "templates":   CATARACT_EXPLANATION_TEMPLATES,
        "risk_info":   CATARACT_RISK_INFO,
        "clinical":    CATARACT_CLINICAL_ADVICE,
        "model_key":   "cataract",
        "preprocess":  "efficientnet",
        "last_conv":   "top_conv",
        "framework":   "tensorflow",
    },
}


if __name__ == "__main__":
    print("✅ keywords_config.py loaded — 4 diseases configured.")
    for d, cfg in DISEASE_CONFIG.items():
        print(f"   {d:<28} {len(cfg['class_names'])} classes: {cfg['class_names']}")
