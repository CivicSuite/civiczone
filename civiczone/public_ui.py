"""Static public UI shell for CivicZone's resident zoning lookup surface."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the accessible public-facing CivicZone lookup page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicZone Public Lookup</title>
<style>
  :root {
    --ink: #17231d;
    --muted: #5d675d;
    --paper: #fffaf0;
    --field: #f2ead8;
    --moss: #385f4c;
    --clay: #b2603f;
    --gold: #d8b45b;
    --line: #d7c8a8;
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    font-family: "Aptos", "Segoe UI", sans-serif;
    color: var(--ink);
    background:
      radial-gradient(circle at 12% 8%, rgba(216, 180, 91, .36), transparent 26rem),
      radial-gradient(circle at 88% 0%, rgba(56, 95, 76, .22), transparent 28rem),
      linear-gradient(135deg, #f8f1e4 0%, #efe1c8 100%);
  }
  a { color: #1f5b47; }
  .skip-link {
    position: absolute;
    left: 1rem;
    top: -4rem;
    z-index: 10;
    background: var(--ink);
    color: white;
    padding: .7rem 1rem;
    border-radius: 999px;
  }
  .skip-link:focus { top: 1rem; }
  header, main, footer { width: min(1120px, calc(100% - 32px)); margin: 0 auto; }
  header { padding: 48px 0 22px; }
  .eyebrow {
    margin: 0 0 12px;
    color: var(--moss);
    font-size: .78rem;
    font-weight: 800;
    letter-spacing: .18em;
    text-transform: uppercase;
  }
  h1 {
    max-width: 870px;
    margin: 0;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(2.9rem, 8vw, 6.4rem);
    line-height: .9;
    letter-spacing: -.06em;
  }
  .lede {
    max-width: 820px;
    margin: 22px 0 0;
    color: #314137;
    font-size: clamp(1.1rem, 2.4vw, 1.55rem);
    line-height: 1.55;
  }
  .banner {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 1rem;
    align-items: center;
    margin: 26px 0 36px;
    padding: 18px;
    border: 1px solid var(--line);
    border-radius: 24px;
    background: rgba(255, 250, 240, .78);
    box-shadow: 0 18px 42px rgba(55, 43, 22, .12);
  }
  .badge {
    display: inline-flex;
    width: fit-content;
    padding: .44rem .72rem;
    border-radius: 999px;
    background: var(--moss);
    color: white;
    font-weight: 800;
    font-size: .82rem;
  }
  .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 18px; }
  .card {
    grid-column: span 6;
    min-width: 0;
    padding: 24px;
    border: 1px solid var(--line);
    border-radius: 28px;
    background: rgba(255, 250, 240, .86);
    box-shadow: 0 18px 40px rgba(55, 43, 22, .10);
  }
  .card.large { grid-column: span 12; }
  h2, h3 { font-family: Georgia, "Times New Roman", serif; letter-spacing: -.03em; }
  h2 { margin: 0 0 14px; font-size: clamp(1.8rem, 4vw, 3rem); }
  h3 { margin: 0 0 10px; font-size: 1.35rem; }
  p { line-height: 1.65; }
  .sample-form {
    display: grid;
    gap: 12px;
    margin: 18px 0;
  }
  label { font-weight: 800; }
  input, textarea {
    width: 100%;
    border: 1px solid #c7b48d;
    border-radius: 16px;
    padding: .85rem 1rem;
    font: inherit;
  }
  input, textarea { background: var(--field); color: var(--ink); }
  .result {
    margin-top: 18px;
    padding: 18px;
    border-left: 6px solid var(--moss);
    border-radius: 18px;
    background: white;
  }
  .result.warning { border-left-color: var(--clay); }
  .result.empty { border-left-color: var(--gold); }
  .state-list {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 16px;
  }
  .state {
    min-height: 132px;
    padding: 14px;
    border: 1px solid var(--line);
    border-radius: 16px;
    background: rgba(255, 255, 255, .72);
  }
  .state strong { display: block; margin-bottom: 6px; }
  .kicker {
    color: var(--muted);
    font-size: .86rem;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  .facts { display: grid; gap: 10px; margin: 0; padding: 0; list-style: none; }
  .facts li { padding: 10px 0; border-top: 1px solid #eadfc8; }
  .notice {
    margin: 24px 0 0;
    padding: 18px;
    border: 1px dashed var(--clay);
    border-radius: 22px;
    background: rgba(178, 96, 63, .10);
  }
  footer { padding: 38px 0 56px; color: var(--muted); }
  :focus-visible { outline: 4px solid var(--gold); outline-offset: 3px; }
  @media (max-width: 760px) {
    header { padding-top: 34px; }
    .banner { grid-template-columns: 1fr; }
    .card { grid-column: span 12; padding: 20px; border-radius: 22px; }
    .state-list { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicZone resident lookup</p>
  <h1>Find zoning context before you ask for a ruling.</h1>
  <p class="lede">CivicZone helps residents and staff inspect parcel zoning context, cited use rules, dimensional standards, and escalation paths without turning informational guidance into an official determination.</p>
  <div class="banner" aria-label="Current product state">
    <div>
      <span class="badge">v1.0.0 cited zoning lookup + staff escalation</span>
      <p><strong>Available now:</strong> parcel lookup, zone and overlay context, cited use and dimensional rule cards, deterministic resident Q&amp;A, staff escalation, optional local persistence, staff workflow APIs, and local adversarial integration validation.</p>
    </div>
    <a href="/docs" aria-label="Open API documentation">API docs</a>
  </div>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Parcel lookup</p>
      <h2 id="lookup-title">123 Main St</h2>
      <form class="sample-form" aria-label="Sample parcel lookup form">
        <label for="parcel">Address or parcel number</label>
        <input id="parcel" name="parcel" value="123 Main St" aria-describedby="parcel-help">
        <p id="parcel-help">This example is pre-filled. Cities can load local parcel and rule records with CIVICZONE_PARCEL_RULE_DB_URL.</p>
      </form>
      <div class="result" role="status" aria-live="polite">
        <h3>R-2 Residential District</h3>
        <ul class="facts">
          <li><strong>Parcel:</strong> 100-200-300</li>
          <li><strong>Overlay:</strong> Historic District Overlay</li>
          <li><strong>Constraints:</strong> Historic review required for exterior alterations; ADU review may require planner confirmation.</li>
          <li><strong>Source:</strong> configured local zoning dataset or bundled municipal sample fixture.</li>
        </ul>
      </div>
    </article>

    <article class="card">
      <p class="kicker">Use rule</p>
      <h2>Accessory dwelling unit</h2>
      <div class="result">
        <h3>Conditional use review</h3>
        <p>In sample zone R-2, an accessory dwelling unit is shown as conditionally allowed.</p>
        <p><strong>Citation:</strong> Sample Zoning Code &sect; 18.20.040.</p>
      </div>
    </article>

    <article class="card large">
      <p class="kicker">User-visible states</p>
      <h2>Clear outcomes for residents</h2>
      <div class="state-list" aria-label="CivicZone user-visible states">
        <div class="state" role="status">
          <strong>Loading</strong>
          Checking the configured parcel and zoning-rule dataset.
        </div>
        <div class="state">
          <strong>Success</strong>
          Parcel context and citations are shown with an informational-only boundary.
        </div>
        <div class="state empty">
          <strong>Empty</strong>
          No parcel was found. Check the address or ask staff to load local parcel records.
        </div>
        <div class="state warning">
          <strong>Error or partial</strong>
          Missing citations, stale source data, or determination requests are routed to planning staff.
        </div>
      </div>
    </article>

    <article class="card">
      <p class="kicker">Dimensional rule</p>
      <h2>Front setback</h2>
      <div class="result">
        <h3>20 feet</h3>
        <p>Sample R-2 dimensional standards show a 20-foot front setback.</p>
        <p><strong>Citation:</strong> Sample Zoning Code &sect; 18.20.060.</p>
      </div>
    </article>

    <article class="card">
      <p class="kicker">Resident Q&amp;A</p>
      <h2>Answer only when cited</h2>
      <div class="result">
        <p><strong>Question:</strong> Can I build an ADU?</p>
        <p><strong>Answer:</strong> The sample code indicates ADUs require conditional use review in R-2. Contact planning staff before applying.</p>
        <p><strong>Citation:</strong> Sample Zoning Code &sect; 18.20.040.</p>
      </div>
    </article>

    <article class="card">
      <p class="kicker">Planner escalation</p>
      <h2>Judgment calls go to humans</h2>
      <div class="result warning">
        <p>Questions about variances, conditional use permits, appeals, nonconforming uses, and zoning determinations are routed to planner review.</p>
        <p>Staff-only precedent context is kept out of resident-facing answers.</p>
      </div>
    </article>
  </section>

  <section class="notice" aria-labelledby="boundary-title">
    <h2 id="boundary-title">Important boundaries</h2>
    <p>CivicZone does not provide legal advice, does not make a zoning determination, and does not replace your planning department. It provides cited informational context and routes judgment calls, missing citations, stale data, and official-decision requests to staff.</p>
    <p>If your question affects property rights, deadlines, permits, enforcement, variances, or appeals, contact municipal planning staff for an official decision.</p>
  </section>
</main>
<footer>
  <p>CivicZone is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p>
</footer>
</body>
</html>
"""
