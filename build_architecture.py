"""Renders architecture diagrams for the offline crop-disease-detection app -> docs/architecture/*.png"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["font.family"] = "DejaVu Sans"

OUT = "docs/architecture"; os.makedirs(OUT, exist_ok=True)

# palette
C = dict(device="#2F4858", ui="#4C9F70", logic="#3D7EA6", ai="#C0504D",
         data="#E0A458", cloud="#8E8E8E", bg="#F7F9FA", txt="#1b1b1b")

def box(ax, x, y, w, h, title, sub="", fc="#4C9F70", tc="white", fs=11, subfs=8.5, r=0.04):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.0,rounding_size={r}",
                 linewidth=1.2, edgecolor="white", facecolor=fc, zorder=2))
    ax.text(x+w/2, y+h/2 + (0.018 if sub else 0), title, ha="center", va="center",
            fontsize=fs, fontweight="bold", color=tc, zorder=3)
    if sub:
        ax.text(x+w/2, y+h/2 - 0.055, sub, ha="center", va="center",
                fontsize=subfs, color=tc, zorder=3)

def arrow(ax, p1, p2, color="#2F4858", style="-|>", lw=1.8, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                 lw=lw, color=color, linestyle=ls, zorder=1,
                 connectionstyle="arc3,rad=0"))

def canvas(w=12, h=7):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.axis("off"); fig.patch.set_facecolor("white"); return fig, ax

# ============================================================
# 1. LAYERED SYSTEM ARCHITECTURE
# ============================================================
fig, ax = canvas(12, 7.6)
ax.text(0.5, 0.965, "Offline Crop-Disease Detection — System Architecture",
        ha="center", fontsize=15, fontweight="bold", color=C["txt"])
ax.text(0.5, 0.925, "All core functions run on the smartphone with no internet connection",
        ha="center", fontsize=10, color="#555", style="italic")

L, W = 0.06, 0.66          # left and width of the main stack
def layer(y, h, tag, fc, items):
    box(ax, L, y, W, h, "", fc=fc)
    ax.text(L+0.014, y+h-0.012, tag, ha="left", va="top", fontsize=8,
            fontweight="bold", color="white", alpha=0.95)
    n=len(items); iw=(W-0.04-(n-1)*0.015)/n; ih=h-0.058
    for k,it in enumerate(items):
        ix=L+0.02+k*(iw+0.015)
        ax.add_patch(FancyBboxPatch((ix, y+0.01), iw, ih,
                     boxstyle="round,pad=0.0,rounding_size=0.02",
                     facecolor="white", edgecolor="none", alpha=0.92, zorder=3))
        ax.text(ix+iw/2, y+0.01+ih/2, it, ha="center", va="center",
                fontsize=8.6, color=C["txt"], zorder=4)

layer(0.78, 0.115, "1 · PRESENTATION", C["ui"],
      ["Multilingual UI\n(English · Shona · Ndebele)", "Diagnosis &\nconfidence", "Treatment steps\n& alerts"])
layer(0.625, 0.115, "2 · APPLICATION LOGIC", C["logic"],
      ["Diagnosis\ncontroller", "Recommendation\nengine", "Predictive-alert\nscheduler", "History\nmanager"])
layer(0.47, 0.115, "3 · ON-DEVICE AI", C["ai"],
      ["Image preprocessing\n(square-crop · 224² · normalise)", "Quantised MobileNetV3\nCNN inference"])
layer(0.315, 0.115, "4 · LOCAL DATA", C["data"],
      ["Treatment\nknowledge base", "Bundled model\n(.tflite)", "Local history DB\n(SQLite)"])
layer(0.16, 0.115, "5 · DEVICE", C["device"],
      ["Smartphone camera", "CPU (no GPU needed)", "On-device storage"])

# vertical flow arrows between layers
for y in [0.78, 0.625, 0.47, 0.315]:
    arrow(ax, (L+W/2, y-0.003), (L+W/2, y-0.043), color="#2F4858", style="<|-|>")

# optional cloud (right side, dashed = only when online)
cx=0.79
box(ax, cx, 0.52, 0.16, 0.16, "Cloud", "(optional)", fc=C["cloud"], fs=11)
ax.text(cx+0.08, 0.50, "model updates ·\nanonymised samples", ha="center", va="top",
        fontsize=7.6, color="#555")
arrow(ax, (L+W, 0.6), (cx, 0.6), color="#8E8E8E", style="<|-|>", ls=(0,(4,3)))
ax.text((L+W+cx)/2, 0.63, "sync only\nwhen online", ha="center", fontsize=7.4,
        color="#8E8E8E", style="italic")
fig.savefig(f"{OUT}/01_system_architecture.png", dpi=150, bbox_inches="tight",
            facecolor="white"); plt.close(fig)

# ============================================================
# 2. INFERENCE & RECOMMENDATION PIPELINE
# ============================================================
fig, ax = canvas(12.5, 5.2)
ax.text(0.5, 0.95, "On-Device Inference & Recommendation Pipeline",
        ha="center", fontsize=15, fontweight="bold", color=C["txt"])

steps = [
    ("Capture", "photograph\naffected leaf", C["ui"]),
    ("Preprocess", "square-crop · 224²\n· normalise", C["logic"]),
    ("CNN inference", "MobileNetV3\n(on-device)", C["ai"]),
    ("Diagnosis", "class + confidence\n(softmax)", C["ai"]),
    ("Treatment", "knowledge-base\nlookup", C["data"]),
    ("Advice", "EN · SN · ND\nstep-by-step", C["ui"]),
]
n=len(steps); bw=0.142; gap=(1-0.05-n*bw)/(n-1); y=0.55; bh=0.26
xs=[]
for i,(t,s,c) in enumerate(steps):
    x=0.025+i*(bw+gap); xs.append(x)
    box(ax, x, y, bw, bh, t, s, fc=c, fs=10.5, subfs=8)
    if i>0: arrow(ax, (xs[i-1]+bw, y+bh/2), (x, y+bh/2))

# low-confidence branch
lc_x = xs[3]+bw/2
arrow(ax, (lc_x, y), (lc_x, 0.30), color="#b03a2e", style="-|>")
ax.text(lc_x+0.015, 0.42, "uncertain", fontsize=7.8, color="#b03a2e", style="italic")
box(ax, lc_x-0.16, 0.12, 0.32, 0.17, "Low confidence?",
    "prompt retake  ·  flag for extension worker", fc="#7B241C", fs=10, subfs=7.6)
ax.text(0.5, 0.88, "Runs end-to-end with no network — typical latency: a fraction of a second on a mid-range phone CPU",
        ha="center", fontsize=9, color="#555", style="italic")
fig.savefig(f"{OUT}/02_inference_pipeline.png", dpi=150, bbox_inches="tight",
            facecolor="white"); plt.close(fig)

# ============================================================
# 3. TRAIN -> DEPLOY (offline) LIFECYCLE
# ============================================================
fig, ax = canvas(12.5, 5.2)
ax.text(0.5, 0.95, "Model Lifecycle: Train in the Cloud → Run on the Phone",
        ha="center", fontsize=15, fontweight="bold", color=C["txt"])

# top band: offline-development (this repo)
ax.add_patch(FancyBboxPatch((0.03, 0.55), 0.6, 0.30, boxstyle="round,pad=0.0,rounding_size=0.03",
             facecolor=C["bg"], edgecolor="#3D7EA6", linewidth=1.4, zorder=0))
ax.text(0.33, 0.815, "DEVELOPMENT  (this repository — one-off, on a workstation)",
        ha="center", fontsize=9, fontweight="bold", color="#3D7EA6")
dev=[("Labelled\ndataset", C["data"]), ("Fine-tune\nMobileNetV3", C["ai"]),
     ("Evaluate\nAUC 0.989", C["logic"])]
for i,(t,c) in enumerate(dev):
    x=0.07+i*0.19; box(ax, x, 0.6, 0.15, 0.16, t, fc=c, fs=9.5)
    if i>0: arrow(ax, (0.07+(i-1)*0.19+0.15, 0.68), (x, 0.68))

# export step
box(ax, 0.69, 0.6, 0.26, 0.16, "Export", "quantise (INT8) →\n.tflite  (a few MB)", fc="#5B2C6F", fs=10, subfs=7.8)
arrow(ax, (0.07+2*0.19+0.15, 0.68), (0.69, 0.68))

# down to device
arrow(ax, (0.82, 0.6), (0.82, 0.45), color="#2F4858")
ax.text(0.84, 0.52, "bundled into the app (APK)", fontsize=8, color="#555", va="center")

# bottom band: on-device (offline)
ax.add_patch(FancyBboxPatch((0.03, 0.08), 0.92, 0.30, boxstyle="round,pad=0.0,rounding_size=0.03",
             facecolor="#EAF3EE", edgecolor=C["ui"], linewidth=1.4, zorder=0))
ax.text(0.49, 0.345, "ON DEVICE  (every farmer, repeatedly, fully offline)",
        ha="center", fontsize=9, fontweight="bold", color=C["ui"])
dep=[("Photo", C["logic"]), ("Preprocess", C["logic"]), ("CNN\ninference", C["ai"]),
     ("Diagnosis +\ntreatment", C["data"]), ("Localised\nadvice", C["ui"])]
for i,(t,c) in enumerate(dep):
    x=0.06+i*0.18; box(ax, x, 0.13, 0.14, 0.16, t, fc=c, fs=9.2)
    if i>0: arrow(ax, (0.06+(i-1)*0.18+0.14, 0.21), (x, 0.21))
fig.savefig(f"{OUT}/03_model_lifecycle.png", dpi=150, bbox_inches="tight",
            facecolor="white"); plt.close(fig)

print("wrote:", os.listdir(OUT))
