def get_css(theme="light"):
    if theme == "dark":
        v = dict(
            primary="#60A5FA", background="#06111F", surface="#0F1E33",
            surface_elevated="#172A45", border="#243B5A", text="#F8F4EA",
            muted_text="#A8B3C5", accent="#60A5FA", accent_soft="rgba(96,165,250,0.12)",
            success="#4ADE80", warning="#FACC15", danger="#F87171",
            shadow="0 1px 2px rgba(0,0,0,0.25), 0 8px 24px rgba(0,0,0,0.28)",
        )
    else:
        v = dict(
            primary="#0B1F3A", background="#F8F4EA", surface="#FFFDF8",
            surface_elevated="#FFFFFF", border="#E5DED0", text="#16243F",
            muted_text="#64748B", accent="#1D4ED8", accent_soft="rgba(29,78,216,0.08)",
            success="#16A34A", warning="#D97706", danger="#DC2626",
            shadow="0 1px 2px rgba(15,23,42,0.05), 0 8px 24px rgba(15,23,42,0.06)",
        )

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {{
  --primary: {v['primary']};
  --background: {v['background']};
  --surface: {v['surface']};
  --surface-elevated: {v['surface_elevated']};
  --border: {v['border']};
  --text: {v['text']};
  --muted-text: {v['muted_text']};
  --accent: {v['accent']};
  --accent-soft: {v['accent_soft']};
  --success: {v['success']};
  --warning: {v['warning']};
  --danger: {v['danger']};
  --shadow: {v['shadow']};
}}

.stApp {{ background: var(--background) !important; }}
.block-container {{ background: transparent !important; padding-top: 2.4rem !important; max-width: 1200px; }}

html, body, [class*="css"], .stApp, p, span, label, div {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--text);
}}

#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"],
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background: transparent; height: 0; }}

/* Chart toolbar (fullscreen / download icons) — make visible against custom backgrounds */
[data-testid="stElementToolbar"] {{
  background: var(--surface-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 2px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 2px !important;
}}
[data-testid="stElementToolbar"] button {{
  color: var(--muted-text) !important;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin: 0 !important;
}}
[data-testid="stElementToolbar"] button:hover {{
  color: var(--accent) !important;
  background: var(--accent-soft) !important;
}}
[data-testid="stElementToolbar"] svg {{
  fill: currentColor !important;
  stroke: currentColor !important;
  width: 16px !important;
  height: 16px !important;
}}

.cs-eyebrow {{
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 8px;
}}
.cs-title {{
  font-weight: 800;
  font-size: 2.15rem;
  line-height: 1.1;
  letter-spacing: -0.035em;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.cs-title .shield {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px; height: 42px;
  border-radius: 12px;
  background: var(--accent-soft);
  flex-shrink: 0;
}}
.cs-tagline {{
  font-size: 0.96rem;
  color: var(--muted-text);
  margin-top: 10px;
  max-width: 38rem;
  line-height: 1.55;
}}
.cs-rule {{ height: 1px; background: var(--border); margin: 20px 0 26px 0; }}

.cs-section-label {{
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--muted-text);
  margin: 20px 0 10px 0;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
  border: 1px solid var(--border) !important;
  border-radius: 16px !important;
  background: var(--surface) !important;
  box-shadow: var(--shadow);
  transition: border-color .18s ease, transform .18s ease;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
  border-color: color-mix(in srgb, var(--accent) 32%, var(--border));
  transform: translateY(-1px);
}}

.stSlider label, .stNumberInput label {{
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  color: var(--text) !important;
}}
.stSlider [data-baseweb="slider"] [role="slider"] {{
  background: var(--surface-elevated) !important;
  border: 2px solid var(--accent) !important;
  border-radius: 50% !important;
  height: 18px !important;
  width: 18px !important;
  box-shadow: 0 2px 8px rgba(37,99,235,0.28) !important;
}}
.stSlider [data-baseweb="slider"] [role="slider"]:hover {{
  box-shadow: 0 3px 12px rgba(37,99,235,0.38) !important;
}}
.stSlider [data-baseweb="slider"] > div > div {{ border-radius: 999px !important; }}
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {{
  background: var(--primary) !important;
  color: var(--background) !important;
  border-radius: 8px !important;
  padding: 2px 8px !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
}}
[data-testid="stTickBar"] {{ color: var(--muted-text) !important; }}

.stNumberInput input {{
  background: var(--surface-elevated) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  transition: border-color .15s ease, box-shadow .15s ease;
}}
.stNumberInput input:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-soft) !important;
}}

.stButton > button *, .stFormSubmitButton > button * {{ color: inherit !important; }}

.stFormSubmitButton > button {{
  background: var(--accent) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: 11px !important;
  padding: 0.7rem 1.4rem !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  width: 100%;
  box-shadow: 0 4px 14px rgba(37,99,235,0.22);
  transition: transform 0.08s ease, box-shadow 0.18s ease;
}}
.stFormSubmitButton > button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(37,99,235,0.30);
}}

.stButton > button {{
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 999px !important;
  padding: 0.4rem 0.9rem !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  width: 100%;
  box-shadow: none !important;
  transition: border-color .15s ease;
}}
.stButton > button:hover {{ border-color: var(--accent) !important; }}

.cs-result {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 26px 28px;
  margin: 0 0 14px 0;
  box-shadow: var(--shadow);
}}
.cs-prob-label {{
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--muted-text);
}}
.cs-prob-value {{
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 600;
  font-size: 3.4rem;
  line-height: 1;
  letter-spacing: -0.02em;
  margin: 6px 0 4px 0;
  font-variant-numeric: tabular-nums;
}}
.cs-pill {{
  display: inline-block;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.07em;
  padding: 6px 14px;
  border-radius: 999px;
  margin-top: 4px;
}}
.cs-pill-low  {{ background: color-mix(in srgb, var(--success) 15%, transparent); color: var(--success); border: 1px solid color-mix(in srgb, var(--success) 45%, transparent); }}
.cs-pill-med  {{ background: color-mix(in srgb, var(--warning) 16%, transparent); color: var(--warning); border: 1px solid color-mix(in srgb, var(--warning) 45%, transparent); }}
.cs-pill-high {{ background: color-mix(in srgb, var(--danger) 15%, transparent);  color: var(--danger);  border: 1px solid color-mix(in srgb, var(--danger) 45%, transparent); }}

.cs-bar-track {{
  height: 9px;
  background: var(--border);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 18px;
}}
.cs-bar-fill {{ height: 100%; border-radius: 999px; transition: width 0.6s cubic-bezier(.4,0,.2,1); }}
.cs-bar-caption {{ font-size: 0.72rem; color: var(--muted-text); margin-top: 8px; }}

.cs-why {{
  font-weight: 700;
  font-size: 1.15rem;
  margin: 26px 0 8px 0;
  letter-spacing: -0.01em;
}}

.cs-factor {{
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  margin-bottom: 8px;
  font-size: 0.88rem;
  transition: transform .15s ease;
}}
.cs-factor:hover {{ transform: translateX(2px); }}
.cs-factor.up   {{ border-left: 3px solid var(--danger); }}
.cs-factor.down {{ border-left: 3px solid var(--accent); }}
.cs-factor .dir  {{ font-weight: 800; width: 16px; text-align: center; }}
.cs-factor.up   .dir {{ color: var(--danger); }}
.cs-factor.down .dir {{ color: var(--accent); }}
.cs-factor .name {{ font-weight: 600; }}
.cs-factor .val  {{ margin-left: auto; font-family: 'IBM Plex Mono', monospace; font-size: 0.76rem; color: var(--muted-text); }}

.cs-empty {{
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: 18px;
  padding: 34px 28px;
  text-align: center;
  color: var(--muted-text);
  font-size: 0.92rem;
  line-height: 1.55;
}}
.cs-empty .ico {{ display: block; margin: 0 auto 12px auto; opacity: 0.7; }}

.cs-method {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 18px 20px;
  margin-top: 16px;
}}
.cs-method h4 {{
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--muted-text);
  margin: 0 0 10px 0;
}}
.cs-method-row {{
  display: flex; justify-content: space-between; gap: 12px;
  padding: 7px 0;
  border-top: 1px solid var(--border);
  font-size: 0.85rem;
}}
.cs-method-row:first-of-type {{ border-top: none; }}
.cs-method-row .k {{ color: var(--muted-text); }}
.cs-method-row .v {{ color: var(--text); font-weight: 600; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; }}

.cs-footer {{
  text-align: center;
  color: var(--muted-text);
  font-size: 0.78rem;
  margin-top: 44px;
  padding-top: 18px;
  border-top: 1px solid var(--border);
}}
.cs-footer .mono {{ color: var(--accent); font-weight: 600; }}
</style>
"""