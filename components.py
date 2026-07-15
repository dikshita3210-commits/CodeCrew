

import re
import textwrap
import streamlit as st
from theme import CRITICAL, WARNING, INFO, ACCENT, BORDER, TEXT_SECONDARY



def html(content: str):
    st.markdown(textwrap.dedent(content).strip(), unsafe_allow_html=True)



_ICONS = {
    "summary": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h8M8 17h5"/></svg>',
    "chart": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 20V10M12 20V4M20 20v-7"/></svg>',
    "score": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>',
    "bug": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="7" y="8" width="10" height="10" rx="4"/><path d="M12 8V5M9 5h6M4 12H2M22 12h-2M5 17l-1.5 1.5M19 17l1.5 1.5M5 8l-1.5-1.5M19 8l1.5-1.5"/></svg>',
    "shield": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/></svg>',
    "code": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 6l-6 6 6 6M15 6l6 6-6 6"/></svg>',
}


def icon(name: str, color: str = ACCENT) -> str:
    svg = _ICONS.get(name, "")
    return f'<span style="color:{color}; display:inline-flex; vertical-align:-2px; margin-right:6px;">{svg}</span>'



def kpi_card(label: str, value, delta: str = None, delta_up: bool = True, accent: str = None):
    if delta:
        cls = "cc-kpi-delta-up" if delta_up else "cc-kpi-delta-down"
        arrow = "↑" if delta_up else "↓"
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'
    else:
        delta_html = '<div style="height:1px;"></div>'  # never a truly empty line

    accent_class = f" cc-accent-{accent}" if accent else ""
    html(f"""
        <div class="cc-card{accent_class}">
            <div class="cc-kpi-label">{label}</div>
            <div class="cc-kpi-value">{value}</div>{delta_html}
        </div>
    """)



def status_chip(status: str) -> str:
    status = (status or "").strip().lower()
    mapping = {
        "completed": "cc-chip-info",
        "in progress": "cc-chip-accent",
        "pending": "cc-chip-neutral",
        "failed": "cc-chip-critical",
    }
    css_class = mapping.get(status, "cc-chip-neutral")
    return f'<span class="cc-chip {css_class}">{status.title() or "—"}</span>'



def severity_badge(severity: str) -> str:
    severity = (severity or "").strip().lower()
    mapping = {
        "critical": "cc-chip-critical",
        "warning": "cc-chip-warning",
        "info": "cc-chip-info",
    }
    css_class = mapping.get(severity, "cc-chip-neutral")
    return f'<span class="cc-chip {css_class}">{severity.title() or "Note"}</span>'



def score_ring(score: int, label: str = "Good", size: int = 150):
    score = max(0, min(100, score))
    circumference = 2 * 3.14159 * 54
    offset = circumference * (1 - score / 100)

    if score >= 80:
        ring_color = INFO
    elif score >= 60:
        ring_color = "#D97706"
    else:
        ring_color = CRITICAL

    html(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <svg width="{size}" height="{size}" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="54" fill="none" stroke="{BORDER}" stroke-width="10"/>
                <circle cx="60" cy="60" r="54" fill="none" stroke="{ring_color}" stroke-width="10" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" stroke-linecap="round" transform="rotate(-90 60 60)"/>
                <text x="60" y="56" text-anchor="middle" font-size="26" font-weight="800" font-family="Inter" fill="#111827">{score}</text>
                <text x="60" y="76" text-anchor="middle" font-size="11" font-family="Inter" fill="#9CA3AF">/100</text>
            </svg>
            <div style="font-weight:600; color:{ring_color}; margin-top:4px; font-size:0.9rem;">{label}</div>
        </div>
    """)



def section_header(title: str, subtitle: str = None, icon_name: str = None):
    icon_html = icon(icon_name) if icon_name else ""
    sub_html = f'<div class="cc-section-sub">{subtitle}</div>' if subtitle else '<div style="height:1px;"></div>'
    html(f"""
        <div class="cc-section-title">{icon_html}{title}</div>{sub_html}
    """)



def page_heading(title: str, subtitle: str = None):
    sub_html = f'<div class="cc-page-sub">{subtitle}</div>' if subtitle else '<div style="height:1px;"></div>'
    html(f'<div class="cc-page-title">{title}</div>{sub_html}')



def topbar(breadcrumb: str, title: str, subtitle: str = None):
    sub_html = f'<div class="cc-page-sub">{subtitle}</div>' if subtitle else '<div style="height:1px;"></div>'
    html(f"""
        <div class="cc-topbar">
            <div>
                <div class="cc-breadcrumb">{breadcrumb}</div>
                <div class="cc-page-title">{title}</div>{sub_html}
            </div>
        </div>
    """)



def stat_pill(label: str, value, color: str = ACCENT):
    html(f"""
        <div class="cc-stat-pill">
            <div class="cc-stat-dot" style="background:{color};"></div>
            <div>
                <div class="cc-stat-value">{value}</div>
                <div class="cc-stat-label">{label}</div>
            </div>
        </div>
    """)



def agent_card(name: str, subtitle: str, stat_lines: list):
    items = "".join(f'<li style="margin-bottom:4px; font-size:0.85rem; color:{TEXT_SECONDARY};">{line}</li>' for line in stat_lines)
    html(f"""
        <div class="cc-card">
            <div style="font-weight:700; font-size:0.95rem; margin-bottom:2px;">{name}</div>
            <div class="cc-muted" style="margin-bottom:10px;">{subtitle}</div>
            <ul style="padding-left:18px; margin:0;">{items}</ul>
        </div>
    """)



def _parse_block(block: str) -> dict:
    def extract(pattern):
        m = re.search(pattern, block, re.IGNORECASE)
        return m.group(1).strip() if m else None

    severity = extract(r"severity:\s*(critical|warning|info)")
    file_line = extract(r"file/?line:\s*(.+)")
    issue = extract(r"issue:\s*(.+)")
    fix = extract(r"fix:\s*(.+)")

    if not severity:
        upper = block.upper()
        if "CRITICAL" in upper:
            severity = "critical"
        elif "WARNING" in upper:
            severity = "warning"
        elif "INFO" in upper:
            severity = "info"

    return {"severity": severity, "file_line": file_line, "issue": issue, "fix": fix, "raw": block}


def render_feedback(text: str, empty_message: str = "No findings returned."):
    if not text or not text.strip():
        html(f'<div class="cc-muted">{empty_message}</div>')
        return

    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if not blocks:
        blocks = [text.strip()]

    for block in blocks:
        parsed = _parse_block(block)
        severity = parsed["severity"] or "info"
        border_class = f"cc-issue-{severity}"
        badge = severity_badge(severity)

        if parsed["issue"]:
            meta = parsed["file_line"] or ""
            body = parsed["issue"]
            fix_html = f'<div class="cc-issue-fix">{parsed["fix"]}</div>' if parsed["fix"] else ""
            html(f"""
                <div class="cc-issue {border_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        {badge}
                        <span class="cc-issue-meta">{meta}</span>
                    </div>
                    <div class="cc-issue-body">{body}</div>{fix_html}
                </div>
            """)
        else:
            html(f"""
                <div class="cc-issue {border_class}">
                    <div style="margin-bottom:6px;">{badge}</div>
                    <div class="cc-issue-body">{parsed["raw"]}</div>
                </div>
            """)


def count_severities(text: str) -> dict:
    """Rough counts used for KPI cards / score calculation."""
    if not text:
        return {"critical": 0, "warning": 0, "info": 0}
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    counts = {"critical": 0, "warning": 0, "info": 0}
    for block in blocks:
        upper = block.upper()
        if "CRITICAL" in upper:
            counts["critical"] += 1
        elif "WARNING" in upper:
            counts["warning"] += 1
        elif "INFO" in upper:
            counts["info"] += 1
    return counts


def compute_score(bug_counts: dict, style_counts: dict) -> int:
    """Simple deterministic scoring: start at 100, dock points per finding.
    Not a claim of code quality precision — just enough to drive the ring UI."""
    score = 100
    for counts in (bug_counts, style_counts):
        score -= counts.get("critical", 0) * 15
        score -= counts.get("warning", 0) * 6
        score -= counts.get("info", 0) * 1
    return max(0, min(100, score))



def severity_bar_chart(bug_counts: dict, style_counts: dict):
    totals = {
        "critical": bug_counts.get("critical", 0) + style_counts.get("critical", 0),
        "warning": bug_counts.get("warning", 0) + style_counts.get("warning", 0),
        "info": bug_counts.get("info", 0) + style_counts.get("info", 0),
    }
    max_count = max(totals.values()) or 1
    colors = {"critical": CRITICAL, "warning": WARNING, "info": INFO}
    labels = {"critical": "Critical", "warning": "Warning", "info": "Info"}

    rows = ""
    for key in ("critical", "warning", "info"):
        pct = int((totals[key] / max_count) * 100) if max_count else 0
        rows += (
            f'<div class="cc-bar-row">'
            f'<div class="cc-bar-label">{labels[key]}</div>'
            f'<div class="cc-bar-track"><div class="cc-bar-fill" style="width:{pct}%; background:{colors[key]};"></div></div>'
            f'<div class="cc-bar-count">{totals[key]}</div>'
            f'</div>'
        )

    html(f'<div class="cc-card">{rows}</div>')
    return totals



def score_breakdown(bug_counts: dict, style_counts: dict, score: int):
    critical_total = bug_counts.get("critical", 0) + style_counts.get("critical", 0)
    warning_total = bug_counts.get("warning", 0) + style_counts.get("warning", 0)
    info_total = bug_counts.get("info", 0) + style_counts.get("info", 0)

    rows = [
        ("Base score", "100", TEXT_SECONDARY),
        (f"Critical findings ({critical_total} × -15)", f"-{critical_total * 15}", CRITICAL),
        (f"Warnings ({warning_total} × -6)", f"-{warning_total * 6}", WARNING),
        (f"Notes ({info_total} × -1)", f"-{info_total * 1}", INFO),
    ]
    items = ""
    for label, value, color in rows:
        items += (
            f'<div style="display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid {BORDER};">'
            f'<span style="font-size:0.84rem; color:{TEXT_SECONDARY};">{label}</span>'
            f'<span style="font-size:0.84rem; font-weight:700; color:{color};">{value}</span>'
            f'</div>'
        )
    items += (
        f'<div style="display:flex; justify-content:space-between; padding:12px 0 0 0;">'
        f'<span style="font-size:0.92rem; font-weight:700;">Final score</span>'
        f'<span style="font-size:0.92rem; font-weight:800; color:{ACCENT};">{score}/100</span>'
        f'</div>'
    )
    html(f'<div class="cc-card">{items}</div>')



def render_stepper(stages: list, current_index: int) -> str:
    rows = ""
    for i, stage in enumerate(stages):
        if i < current_index:
            step_icon, icon_cls, label_cls = "✓", "cc-step-icon-done", "cc-step-label-done"
        elif i == current_index:
            step_icon, icon_cls, label_cls = str(i + 1), "cc-step-icon-active", "cc-step-label-active"
        else:
            step_icon, icon_cls, label_cls = str(i + 1), "cc-step-icon-pending", "cc-step-label-pending"

        rows += (
            f'<div class="cc-step-row">'
            f'<div class="cc-step-icon {icon_cls}">{step_icon}</div>'
            f'<div class="{label_cls}">{stage}</div>'
            f'</div>'
        )
        if i < len(stages) - 1:
            rows += '<div class="cc-step-connector"></div>'

    return rows