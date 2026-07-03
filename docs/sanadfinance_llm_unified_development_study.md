# SanadFinance-LLM: Unified Development Study
## Methodology, System Architecture, Model Training Program & Business Plan

**Founder & CEO:** Salim Al-Barami
**Date:** July 2026
**Classification:** Confidential — Strategic Planning Document

---

## Executive Summary

**Vision.** Build the world's first AI foundation model for financial trust verification by operationalizing ʿIlm al-Ḥadīth — the 1,400-year-old Islamic science of information authentication — as a complete, auditable verification engine for modern financial intelligence. Phase 1 targets Islamic finance; Phase 2 extends to global financial services on the strength of transparency and explainability.

**Key innovation: the dual-axis grading system.** Classical ḥadīth science grades two distinct objects with two distinct instruments: narrators are graded through jarḥ wa taʿdīl (source criticism), and reports are graded through the ṣaḥīḥ–mawḍūʿ verdict ladder (which weighs the chain and the content together). SanadFinance-LLM implements both axes explicitly. Every information source carries a standing reliability grade on the six-level Thiqah hierarchy; every claim receives a verdict on the six-level Ṣaḥīḥ hierarchy, derived from the grades of its transmission chain, precision (ḍabṭ) assessment, multi-attestation (tawātur) analysis, anomaly (shudhūdh) detection, and hidden-defect (iʿlāl) screening. No existing financial AI system separates source standing from claim verdict, and none produces a complete, citable chain of transmission (isnād) for every output.

**Market opportunity.** Global financial services: $36.0T (2025). AI in financial services: $46.2B (2024) growing to $147.8B by 2030 at 21.4% CAGR. Islamic finance: $5.2T (2025) growing to a projected $9.75T by 2030 at 15–18% CAGR — a market whose dual-compliance requirement (conventional + Sharia) structurally favors a verification-first AI architecture.

**Development strategy: two tracks.**
- **Track A — Founder-executed prototype (Months 0–3, pre-seed).** A methodology-tuned 8–14B parameter model trained on founder workstation infrastructure (32GB-VRAM class GPU) using QLoRA supervised fine-tuning followed by preference-based RLISF (Reinforcement Learning from Islamic Scholar Feedback via direct preference optimization). Deliverable: a working Sanad reasoning engine, a gold evaluation set, and a live demonstration asset that materially de-risks the seed round.
- **Track B — Funded production program (Months 1–24, post-seed).** Scaled fine-tuning of a 32–70B class model on rented GPU clusters, full RLISF with a governed scholar panel, and the complete four-layer verification platform.

**Financial plan (Conservative Base Case).** ARR of $1.2M (Y1), $4.8M (Y2), $14.4M (Y3), $28.8M (Y4), $43.2M (Y5), with growth rates of 300% / 200% / 100% / 50% consistent with institutional-investor guidance ceilings. Cash-flow break-even at Month 42 (base), Month 44 (probability-weighted expected). Capital to break-even: ~$95M base case; risk-adjusted expected requirement: $100M; planning upper bound including growth capital: $130M; bear case: $165M.

**Probability-weighted scenario analysis:**

| Scenario | Year 5 ARR | Break-Even | Funding to Plan | Probability | Weighted ARR | Weighted Funding |
|---|---|---|---|---|---|---|
| Conservative | $18.0M | Month 60 | $140M | 20% | $3.6M | $28.0M |
| Base Case | $43.2M | Month 42 | $95M | 60% | $25.9M | $57.0M |
| Optimistic | $52.5M | Month 36 | $75M | 20% | $10.5M | $15.0M |
| **Expected Value** | **$40.0M** | **Month 44** | **$100M** | **100%** | **$40.0M** | **$100M** |

**Funding path.** Seed $15M at $35M pre-money (Months 1–3) → Series A $40M at $160M pre (Month 12, gated by the trigger matrix in §27) → Series B $25M at $280M pre (Month 18) → Series C $50M at $500M pre (Month 30). Target exit valuation: $2–3B (base) to $4–6B (optimistic) by Year 6.

**Founding team.**
- **Founder & CEO: Salim Al-Barami** — originator of the Sanad Trust Framework and the underlying ʿIlm al-Ḥadīth operationalization methodology (founder IP); track record delivering national-scale AI systems in GCC government and enterprise settings.
- **CTO:** to be recruited (LLM training and production ML infrastructure).
- **Chief Scholar:** to be recruited (uṣūl al-ḥadīth scholarship plus Islamic finance jurisprudence; chairs the scholar panel defined in §19).
- **CFO:** to be recruited at Series A.

---

## Table of Contents

**Part I — Classical Methodology**
1. Foundations of ʿIlm al-Ḥadīth for Information Verification
2. The Dual-Axis Grading System
3. Ḍabṭ — Precision Assessment
4. Tawātur — Multi-Attestation Consensus
5. Shudhūdh — Anomaly Detection
6. Iʿlāl — Hidden-Defect Screening
7. Operational Protocols

**Part II — System Architecture**
8. Four-Layer Verification System
9. Data Substrate: Source Registry & Isnād Ledger
10. Verification Pipeline & Output Schema
11. Graduated User Interfaces

**Part III — Model Development Program**
12. Foundation Model Selection
13. Two-Track Training Strategy
14. Training Data Architecture
15. RLISF — Reinforcement Learning from Islamic Scholar Feedback
16. Evaluation & Calibration Framework
17. Technical Fallback Strategy

**Part IV — Domain Implementation**
18. Islamic Finance Specialization
19. Scholar Panel Governance
20. Data Acquisition & Licensing
21. Regulatory Compliance & International Expansion Mapping
22. Beyond Finance: Healthcare, Labor, E-Commerce

**Part V — Business Plan**
23. Market Opportunity
24. Competitive Landscape, Moats & IP Strategy
25. Go-to-Market Strategy
26. Financial Model
27. Funding Strategy
28. Risk Management

**Part VI — Execution**
29. Integrated Roadmap
30. Success Metrics & KPIs

**Appendices**
A. Worked Gold Example — Complete Sanad Analysis
B. Training Record Schema (JSONL)

---

# Part I — Classical Methodology

## 1. Foundations of ʿIlm al-Ḥadīth for Information Verification

ʿIlm al-Ḥadīth is the most sophisticated information-verification system developed in pre-modern scholarship: fourteen centuries of systematic method for authenticating transmitted reports under uncertainty, with real stakes attached to error. Its evolution — from the scattered evaluative judgments of early critics such as Yaḥyā ibn Maʿīn and Aḥmad ibn Ḥanbal, through the systematizing breakthrough of Ibn Abī Ḥātim al-Rāzī (d. 327 AH), to the refined multi-level frameworks of Ibn al-Ṣalāḥ, al-Dhahabī, al-ʿIrāqī, Ibn Ḥajar al-ʿAsqalānī, al-Sakhāwī, and al-Suyūṭī — produced exactly the apparatus modern financial AI lacks: graded (not binary) reliability, explicit provenance, disciplined consensus standards, and expert-level defect detection.

Four core components carry into the financial domain:

1. **Isnād (chain of transmission).** Complete documentation of every link between an original source and the final recipient. *Financial application:* full provenance tracking from data origin (exchange filing, central bank release, newswire) through every processing agent to the final recommendation, recorded as an immutable, cryptographically verifiable audit trail.
2. **Jarḥ wa taʿdīl (source criticism).** Systematic evaluation of each transmitter's integrity, precision, and bias. *Financial application:* standing reliability grades for institutions, publications, analysts, and data vendors, maintained dynamically against their track records (Axis 1, §2.2).
3. **Matn analysis (content verification).** Examination of the report's content for internal coherence, external consistency, and plausibility. *Financial application:* cross-source consistency checking, contextual plausibility analysis, and reconciliation of conflicting figures.
4. **Tawātur (mass corroboration).** Recognition that some facts are attested by so many genuinely independent chains that coordinated fabrication is impossible. *Financial application:* consensus mechanisms with formal independence testing (§4).

The framework's transferability rests on a structural insight: the classical scholars were solving the general problem of *trusting information received through intermediaries whose reliability varies* — which is precisely the problem of modern financial data. The methodology is adopted here with its full nuance, not as terminology decoration.

## 2. The Dual-Axis Grading System

### 2.1 Two Objects, Two Instruments

Classical ḥadīth science never graded sources and reports on the same scale, because they are different epistemic objects:

- A **transmitter** (rāwī) has a standing reliability grade earned across their whole record — this is the province of jarḥ wa taʿdīl.
- A **report** (the ḥadīth itself) receives a verdict — ṣaḥīḥ, ḥasan, ḍaʿīf, mawḍūʿ — that weighs the specific chain behind it *and* the content itself, together.

A supremely reliable transmitter can still convey a defective report; a chain of merely acceptable transmitters can, with sufficient independent corroboration, support a sound conclusion. Collapsing the two axes into one scale destroys exactly the information that makes the classical method powerful.

SanadFinance-LLM therefore maintains two explicit axes:

- **Axis 1 — Source Reliability (the Thiqah hierarchy):** a standing grade attached to every source in the registry, updated continuously from track record.
- **Axis 2 — Claim Verdict (the Ṣaḥīḥ hierarchy):** a per-claim verdict derived from Axis-1 grades of the supporting chain plus ḍabṭ, tawātur, shudhūdh, and iʿlāl analysis.

The system's core reasoning task — and the core training objective for the model (Part III) — is the disciplined derivation of Axis-2 verdicts from Axis-1 evidence.

### 2.2 Axis 1 — Source Reliability Hierarchy (Jarḥ wa Taʿdīl)

Adapted from al-Suyūṭī's synthesis and Ibn Ḥajar's twelve-rank system, compressed to six operational levels plus a disqualification status. Score bands partition [40, 100]; sources scoring below 40 are disqualified.

| Level | Classical Grade | Score Band | Requirements | Financial Exemplars | Evidentiary Standing |
|---|---|---|---|---|---|
| **S1** | Athbatun Nās / Awthaqun Nās — "most established of people" | 90–100 | Unanimous expert recognition; near-zero error tolerance; supreme institutional authority; legally binding output | Central banks (Fed, ECB, SAMA, QCB) official communications; final regulatory rules (SEC, Basel Committee); Big Four–audited statements with unqualified opinions | Standalone sufficient for routine decisions; anchor evidence for critical decisions |
| **S2** | Thiqah Thābit — "reliable and firm" | 80–89 | Near-zero error rate across long record; consistency across independent transmissions; broad expert endorsement | Tier-1 bank official disclosures; government treasuries; major rating agency institutional assessments | Primary evidence |
| **S3** | Thiqah — "reliable" | 70–79 | High consistency with rare, isolated errors; general consensus on reliability; clear editorial/method­ological process | Established financial media with editorial oversight (WSJ, FT, Bloomberg editorial); major research houses (McKinsey, BCG); recognized research institutions | Primary evidence; corroboration preferred for high-stakes use |
| **S4** | Ṣadūq — "truthful" (but requiring examination) | 60–69 | Fundamental honesty with structural conflicts of interest or occasional reliability issues; admissible only with recorded examination | Underwriter research on covered issuers; corporate investor relations and earnings guidance; industry association position papers | Admissible with mandatory conflict disclosure and cross-verification |
| **S5** | Shaykh — "respectable" | 50–59 | Acceptable general standing; content is opinion, preliminary, or unvalidated | Expert commentary and op-eds; academic working papers; conference presentations; regulatory comment letters | Supporting evidence only |
| **S6** | Maqbūl — "acceptable" (minimum threshold) | 40–49 | No proof against reliability, but no established record | New market entrants; fintech startups without track record; aggregated social-media sentiment | Corroboration (mutābaʿāt) only; never load-bearing |
| **—** | Matrūk — "abandoned" (disqualified) | < 40 | Demonstrated dishonesty, manipulation, or fabrication history | Known pump-and-dump promoters; discredited analysts; fabrication-history outlets and anonymous channels | Excluded from evidence; retained in registry as fraud-signal input |

**Sub-classifications preserved from the classical apparatus:**
- **Maqbūl vs. Layyin:** a Maqbūl source may serve corroborating functions; a Layyin source may not serve even that function. The registry records the distinction so that borderline sources are not silently promoted into corroboration roles.
- **Ṣadūq yahim ("truthful but errs"):** a Ṣadūq source with a documented error pattern in a specific domain carries a domain-scoped demotion — its grade is reduced only within the domains where the pattern is established.
- **Grade dynamics:** grades are earned and lost. Every verified outcome updates the source's record (ḍabṭ metrics, §3); sustained deterioration triggers automatic demotion review, and any confirmed fabrication moves a source directly to Matrūk regardless of prior standing.

### 2.3 Axis 2 — Claim Verdict Hierarchy (Ṣaḥīḥ Ladder)

Verdict bands partition [0, 100] with no overlaps. The verdict attaches to a *claim in context*, never to a source.

| Level | Classical Verdict | Score Band | Meaning | Approved Uses |
|---|---|---|---|---|
| **V1** | Ṣaḥīḥ — authentic | 90–100 | Unbroken high-grade chain; ḍabṭ sound; no unresolved anomaly or defect; corroborated or anchored by S1 evidence | Critical financial decisions; regulatory reporting; high-stakes execution |
| **V2** | Ḥasan — good | 75–89 | Sound overall with minor chain weakness (e.g., strongest support is S3, or an S2 chain with a minor ḍabṭ deduction) | Standard investment analysis; routine compliance; operational decisions |
| **V3** | Ḥasan li-Ghayrihi — good by corroboration | 60–74 | Individually weak supports elevated by genuinely independent convergence | Market sentiment and trend conclusions; screening outputs pending confirmation |
| **V4** | Ḍaʿīf — weak | 35–59 | Chain or content defects; usable only as context or hypothesis | Preliminary research; hypothesis generation; background context |
| **V5** | Ḍaʿīf Jiddan — very weak | 10–34 | Severe credibility problems | Contrarian indicators; manipulation-pattern inputs only |
| **V6** | Mawḍūʿ — fabricated | 0–9 | Demonstrably false or manipulative | Fraud alerts; provenance forensics; system security |

**Elevation mechanism (the li-ghayrihi principle).** Classical method allows corroboration to raise a verdict: a ḥasan report supported by independent parallel chains becomes ṣaḥīḥ li-ghayrihi; a ḍaʿīf report with genuinely independent support may rise to ḥasan li-ghayrihi. The system encodes this as a *derivation operation* (rule R2 below) rather than as additional classes, preserving the six-level ladder while capturing the full classical logic.

### 2.4 Verdict Derivation Rules

The verdict function is deterministic in structure, with model judgment applied inside each rule — never in place of the rules.

- **R1 — Weakest-link anchor.** A claim's base verdict is anchored to the weakest necessary link in its strongest supporting chain: an unbroken chain terminating in S1 anchors at V1; strongest support S2 anchors at V1–V2 boundary; S3 anchors at V2; S4 anchors at V3–V4 boundary; S5/S6 support alone anchors at V4. A chain is only as strong as its weakest necessary transmitter.
- **R2 — Elevation by corroboration.** Independent parallel attestation (mutābaʿāt) from at least two additional sources graded S4 or above, passing the independence tests of §4.3, raises the verdict by at most one band. Claims meeting full tawātur criteria (§4) map directly to V1 with score ≥ 95, irrespective of individual chain grades — this is the classical rule that mutawātir knowledge is certain independent of narrator grading.
- **R3 — Demotion by defect.** A confirmed shudhūdh finding (§5) caps the verdict at V4. A confirmed iʿlāl finding (§6) demotes per defect class, to V6 for fabrication-class defects. An *unresolved* iʿlāl screening flag caps the verdict at V2 and forces escalation (§7).
- **R4 — Ḍabṭ modifiers.** Composite ḍabṭ scores (§3) adjust the verdict score by up to ±5 points *within* a band. Ḍabṭ alone never crosses a band boundary; only R2 and R3 move bands.
- **R5 — Conflict resolution.** When sources conflict on content, reconciliation is attempted first (differing scope, timing, rounding, or definition). If reconciliation fails, the higher-Axis-1 chain prevails and the opposing report is evaluated for shudhūdh. The resolution basis is always recorded in the isnād documentation.
- **R6 — Temporal validity.** Every verdict carries a validity horizon derived from the claim's decay class (real-time market data decays in minutes; audited annual figures decay over quarters). Expired verdicts revert to "re-verify" status rather than silently persisting.

**Output contract.** Every assessment emits: per-source Axis-1 grades used, the derivation trace (which rules fired and why), the Axis-2 verdict with numeric score and confidence interval, the complete isnād, the validity horizon, and an escalation flag. The full schema appears in §10 and Appendix B.

## 3. Ḍabṭ — Precision Assessment

### 3.1 Classical Definition and Financial Translation

Ḍabṭ is the precision with which a transmitter preserves and conveys information without distortion. Classical critics assessed it through four methods, each with a direct modern analogue:

| Classical Method | Classical Practice | Financial Application |
|---|---|---|
| Murāqaba (direct observation) | Documented lifestyle, teachers, travel, conduct | Institutional history, leadership record, operational transparency |
| Istijwāb (targeted questioning) | Testing recall of sources and details | Methodology audits, data-source verification, process documentation review |
| Talqīn (examination tests) | Presenting altered material to test detection | Stress testing, red-team scenario injection, manipulation-detection drills |
| Muqārana (source–text comparison) | Comparing written records against oral transmission | Cross-referencing automated feeds against primary documents and manual processes |

### 3.2 Four Assessment Dimensions

Each registered source carries a ḍabṭ profile scored across four dimensions:

1. **Ḍabṭ al-Ṣadr (cognitive/track-record precision):** historical accuracy rates, consistency across repeated reporting, error frequency, and crisis-period performance (accuracy under stress is weighted separately from calm-market accuracy).
2. **Ḍabṭ al-Kitāb (documentation precision):** methodology disclosure, citation completeness, audit-trail quality, version control, and correction protocols — how a source handles its own errors is itself graded.
3. **Ḍabṭ al-ʿAmal (operational/transmission precision):** content fidelity through the source's pipeline, ability to distinguish confidence levels, and speed and transparency of error recognition.
4. **Temporal precision:** freshness, update cadence, and decay resistance — how well the source's information retains accuracy over its stated horizon.

**Composite weighting (default policy parameters, tunable per deployment):** temporal 30%, contextual 25%, methodological 20%, historical track record 15%, cross-validation accuracy 10%.

### 3.3 Temporal Decay Model

Verdicts and ḍabṭ contributions decay by information class, following the classical recognition that transmission reliability degrades with distance from the source event:

```python
DECAY_FACTORS = {
    "real_time":  1.00,   # live market data within validity window
    "daily":      0.98,
    "weekly":     0.95,
    "monthly":    0.90,
    "quarterly":  0.85,
    "annual":     0.80,
}

def temporal_precision(base_accuracy: float, horizon: str,
                       aging_resistance: float) -> float:
    """Ḍabṭ temporal component. aging_resistance in [0,1] rewards
    sources whose historical accuracy persists over long horizons."""
    decay = DECAY_FACTORS[horizon] * (1 + 0.1 * aging_resistance)
    return min(base_accuracy * decay, 1.0)
```

### 3.4 Contextual Precision

Ḍabṭ is context-scoped, not global. The registry maintains separate precision records per market regime (bull, bear, high-volatility, crisis), per sector, per geography, per instrument class, and — for Islamic finance — per compliance function (Sharia screening accuracy, ṣukūk analysis, halal-investment classification). A source that is S2 for GCC sovereign data may be effectively S4 for equity sentiment; the scoped record prevents halo effects.

## 4. Tawātur — Multi-Attestation Consensus

### 4.1 The Governing Standard: Quality Over Count

Classical scholars debated numeric thresholds for tawātur — positions ranged from 4+ to 70 narrators — but the Ḥanafī position, adopted here as the governing standard, holds that **no fixed number suffices or is required**: tawātur obtains when independent attestation makes coordinated fabrication impossible and certainty (ʿilm) results. Numbers are evidence of independence, not a substitute for it.

**Operationalization: qualitative test with configurable floors.** The system enforces minimum attestation floors as guardrails — default 5 independent sources for tawātur lafẓī and 7 for tawātur maʿnawī, configurable per decision context — but floors are *necessary, never sufficient*. Tawātur status is granted only when the impossibility-of-collusion test (§4.3) passes. This preserves classical honesty about the standard's qualitative core (the scholars themselves acknowledged its irreducibly judgmental element) while giving deployments a tunable safety parameter.

### 4.2 Tawātur Types

| Type | Definition | Financial Application | Verdict Effect |
|---|---|---|---|
| **Tawātur Lafẓī** (verbal/exact) | Identical or near-identical content across independent chains | Market prices, exchange rates, official announcements, regulatory text | Direct V1 mapping (≥ 95) for the exact datum |
| **Tawātur Maʿnawī** (semantic) | Convergent meaning through varied expressions, via implicative (dalālah iltizāmiyyah) or partial (dalālah taḍammuniyyah) indication | Market sentiment, trend confirmation, governance assessments | Direct V1 mapping for the shared semantic core; specifics graded separately |
| **Tawātur Ṭabaqah** (generation-to-generation) | Group-to-group transmission across time | Institutional consensus sustained across reporting periods | Strengthens R2 elevation |
| **Tawātur ʿAmal** (practice-based) | Consecutive performance evidence | Persistent market-behavior patterns, settled operational conventions | Strengthens R2 elevation |
| **Tawātur Qadr Mushtarak** (common-core) | Individually varied reports whose shared core reaches tawātur | Divergent analyst reports agreeing on a directional fact | V1 for the common core only |

### 4.3 Impossibility-of-Collusion Test

Independence is scored across five dimensions; tawātur requires passing on all of them, not averaging across them:

1. **Institutional independence** — distinct ownership, affiliation, and incentive structures (a filing and the filer's own IR release are one chain, not two).
2. **Geographic/jurisdictional independence** — distinct regulatory and market environments.
3. **Temporal independence** — attestations arising without a coordination window (timestamp and propagation analysis).
4. **Methodological independence** — different analytical routes to the same conclusion.
5. **Informational independence** — no shared upstream single source (syndicated wire copy republished by fifty outlets is one attestation).

The fifth dimension is the dominant failure mode in modern media and is tested first: the system traces every attestation to its upstream origin through the isnād ledger before counting it.

## 5. Shudhūdh — Anomaly Detection

**Definition.** A report from an otherwise reliable source that contradicts stronger or more numerous sources in a way that cannot be reconciled.

**Detection principles, preserved from the classical method:**
- **Comparative, never isolated.** Shudhūdh cannot be detected by inspecting a report alone; it requires systematic comparison across the relevant corpus. Layer 2 of the architecture (§8) exists for this purpose.
- **Reconciliation first.** Apparent conflicts are first tested for harmonization — differing scope, timing, rounding, definitions, or reporting bases. Only irreconcilable opposition is shudhūdh.
- **Hierarchy governs.** When reconciliation fails, precedence follows Axis-1 strength (rule R5), with contextual judgment on domain expertise — an S3 sector specialist may outweigh an S2 generalist within its specialty.
- **Expert judgment retained.** Subtle anomaly assessment is flagged for Layer 3 review rather than resolved mechanically when confidence is low.

**Modern detection stack:** statistical outlier analysis with contextual weighting; contradiction detection against higher-reliability consensus; historical-pattern deviation analysis; and manipulation-indicator correlation (a shādh report that benefits an identifiable position is escalated as a potential fraud signal, not merely discounted).

## 6. Iʿlāl — Hidden-Defect Screening

### 6.1 The Classical Ceiling

Iʿlāl is the detection of defects that "appear sound but thorough research reveals a disparaging factor" (Ibn al-Ṣalāḥ) — misattributed chains, chronologically impossible links, grafted content, subtle alterations. The classical literature is unambiguous that this is the rarest expertise in the entire science: very few critics in fourteen centuries attained it, and it resists reduction to mechanical procedure.

The system design honors that ceiling. **The model performs iʿlāl *screening* — surfacing candidate hidden defects with evidence — and human experts perform iʿlāl *adjudication*.** Claims of fully automated hidden-defect detection would misrepresent both the methodology and the achievable state of the art; the commitment made to customers and regulators is high-recall screening plus governed expert review, which is also the more defensible product.

### 6.2 Defect Taxonomy

**In the chain (isnād):** misclassified continuity (a broken chain presented as connected); false attribution; chronological impossibility (data "confirmed" before its purported source event); chain grafting (authentic provenance attached to fabricated content — the signature of sophisticated financial disinformation).

**In the content (matn):** unauthorized additions by intermediaries; subtle numerical or wording alterations; content mixing (elements of separate authentic reports fused into a misleading composite).

### 6.3 Screening Stack

Surface authenticity verification → deep contextual inconsistency analysis → subtle pattern-violation detection (trained on seeded-defect corpora, §14) → relationship and incentive analysis (network analysis of source relationships, timing analysis for coordination, economic-incentive mapping) → expert heuristics encoded from the scholar panel. Any positive screen caps the verdict at V2 and routes to Layer 3 (rule R3).

**Performance commitments:** screening recall ≥ 85% on seeded-defect evaluation sets at ≤ 20% escalation rate (v0 target), with expert-agreement precision measured and published quarterly. Autonomous adjudication accuracy is a research aspiration tracked internally, not a marketed capability.

## 7. Operational Protocols

### 7.1 Time-Tiered Response

| Tier | Latency | Scope | Method | Escalation |
|---|---|---|---|---|
| 1 | < 30 s | Routine data from established sources | Layer 1 automated screening | Automatic on anomaly or low confidence |
| 2 | 30 s – 5 min | Breaking news, earnings, important decisions | Layer 2 comparative analysis + consensus | On unresolved conflict or iʿlāl flag |
| 3 | 5 – 60 min | High-stakes decisions, complex compliance | Layer 3 expert review with full documentation | Peer review below confidence threshold |
| 4 | 1 h + | Suspected fraud, major regulatory issues, systemic questions | Deep investigation, multi-expert validation, external consultation | Board/regulator notification protocols |

### 7.2 Conflict and Disagreement Resolution

- **Source conflicts:** rule R5 with mandatory reconciliation attempt and documented resolution basis.
- **Expert disagreements:** structured escalation with independent peer review; majority and minority opinions both recorded (the classical practice of preserving ikhtilāf rather than erasing it).
- **Temporal conflicts:** recency preferred within a decay class; track record preferred across classes; trend analysis distinguishes systematic change from noise.

### 7.3 Quality Assurance and Continuous Improvement

Accuracy tracking against realized outcomes; systematic error and near-miss review; user feedback integration; quarterly expert calibration sessions to keep human graders consistent; ongoing incorporation of classical scholarship research; and versioned methodology documentation so that every historical verdict remains interpretable under the rules that produced it.

---

# Part II — System Architecture

## 8. Four-Layer Verification System

| Layer | Function | Latency | Coverage | Components |
|---|---|---|---|---|
| **1 — Automated Screening** | Axis-1 lookup, basic anomaly scan, rapid confidence scoring, auto-escalation | Real-time (< 30 s) | ~90% of volume | Source registry, screening classifier, threshold logic |
| **2 — Comparative Analysis** | Corpus gathering, tawātur assessment, shudhūdh detection, conflict analysis, verdict derivation (R1–R6) | Near-real-time (30 s – 5 min) | ~8% of volume | SanadFinance-LLM reasoning engine, retrieval over the comparison corpus, independence tracer |
| **3 — Expert Review** | Iʿlāl adjudication, nuanced judgment, peer review, contested-case resolution | Minutes to hours | ~2% of volume | Scholar/analyst interface, peer-review coordination, decision documentation |
| **4 — Continuous Learning** | Outcome tracking, pattern updates, model refinement, expert-feedback integration | Ongoing | All decisions | Outcome database, retraining pipeline, calibration monitoring |

Escalation is monotone: any layer may push upward; no layer may suppress a flag from below. The fine-tuned model (Part III) *is* the Layer-2 reasoning engine; Layers 1 and 3 bound it with deterministic screening below and human authority above.

## 9. Data Substrate: Source Registry & Isnād Ledger

**Design principle: facts live in the substrate; reasoning lives in the model.** Language models are unreliable stores of provenance facts and will fabricate chains if asked to recall them. All registry and provenance data is therefore retrieved and supplied to the model as evidence at inference time — the model never asserts a chain it was not shown.

**Source Registry (relational store, PostgreSQL-class):**
- Source identities with Axis-1 grade, grade history, and review triggers
- Scoped ḍabṭ profiles (per regime, sector, geography, instrument, compliance function)
- Conflict-of-interest maps (ownership, mandates, coverage relationships)
- Error and correction ledger per source
- Layyin/Maqbūl flags, Ṣadūq-yahim domain scopes, Matrūk blacklist with rationale

**Isnād Ledger (graph store, Neo4j-class):**
- Every claim as a node; every transmission hop as a typed, timestamped edge
- Upstream-origin tracing for informational-independence testing (§4.3)
- Append-only with cryptographic hashing per hop — the "blockchain-inspired" property that makes chains auditable without a distributed ledger's overhead
- Relationship graph among sources for iʿlāl network analysis

**Comparison Corpus (retrieval layer):** indexed recent reporting across registered sources, embedding-indexed for semantic retrieval, feeding Layer-2 shudhūdh comparison and tawātur counting.

## 10. Verification Pipeline & Output Schema

**Pipeline (executed by Layer 2 for each claim):**
1. Ingest claim; resolve or construct its isnād from the ledger.
2. Retrieve Axis-1 grades and scoped ḍabṭ profiles for every chain link.
3. Retrieve the comparison corpus for the claim's topic.
4. Assess tawātur: count attestations, trace upstream origins, run the five independence tests.
5. Detect shudhūdh: attempt reconciliation of conflicts; classify irreconcilables.
6. Run the iʿlāl screen.
7. Derive the verdict via R1–R6; compute confidence interval and validity horizon.
8. Emit the SanadAssessment record; escalate if flagged.

**SanadAssessment record (abbreviated; full schema in Appendix B):**

```json
{
  "claim_id": "…",
  "claim_text": "…",
  "verdict": {"grade": "sahih", "band": "V1", "score": 91,
               "confidence_interval": [87, 95], "valid_until": "…"},
  "sources": [{"source_id": "…", "axis1_grade": "S1", "axis1_score": 94,
                "dabt": {"composite": 0.93, "scope_notes": "…"},
                "role": "anchor | corroboration | rejected"}],
  "tawatur": {"status": "none | lafzi | manawi | …",
               "independent_chains": 2, "independence_tests": {"…": true}},
  "shudhudh_findings": [{"conflicting_claim": "…", "reconciliation": "…",
                          "resolution": "…"}],
  "ilal_screen": {"flag": false, "candidates": []},
  "derivation_trace": ["R1: anchor S1 → V1 base 92", "R4: dabt −1 → 91"],
  "isnad": ["origin → hop → hop → assessment"],
  "escalation": {"required": false, "layer": null, "reason": null}
}
```

## 11. Graduated User Interfaces

- **Executive level:** verdict, confidence, actionable recommendation, risk flags — decision support with minimal apparatus.
- **Professional level:** full source analysis, comparative data, derivation trace, historical context.
- **Expert level:** complete analytical detail, iʿlāl screening evidence, peer-review tooling, methodology transparency, and override controls with mandatory justification capture (overrides feed Layer 4).

---

# Part III — Model Development Program

## 12. Foundation Model Selection

### 12.1 Evaluation Framework

| Criterion | Weight | Rationale |
|---|---|---|
| Arabic–English capability | 25% | Classical methodology sources and GCC deployment demand native-quality Arabic |
| Financial domain knowledge | 20% | Reduces training burden; improves zero-shot floor |
| Multi-step reasoning | 20% | Verdict derivation is structured multi-stage reasoning |
| Fine-tuning flexibility (open weights) | 15% | The methodology *is* the differentiation; it must live in weights we control |
| Operational efficiency | 10% | Self-hosted economics govern gross margin |
| Explainability & compliance posture | 10% | Financial regulation requires traceable decisions |

### 12.2 Candidate Landscape (2026)

| Model family | Sizes of interest | Arabic | Reasoning | License posture | Assessment |
|---|---|---|---|---|---|
| **Qwen (2.5 / 3)** | 8B, 14B, 32B, 72B | Excellent among open models | Strong, incl. reasoning-tuned variants | Permissive on most sizes | **Primary Track-A base; leading Track-B candidate** |
| **ALLaM (SDAIA)** | Available Arabic-first sizes | Arabic-first, sovereign pedigree | Good | Regional/sovereign terms | **Strategic adapter target for Saudi deployments; sovereign-AI narrative** |
| **Fanar (QCRI)** | Arabic-centric sizes | Arabic-centric, Qatari pedigree | Good | Regional terms | Strategic adapter target for Qatar deployments |
| **Llama (3.3 / 4)** | 8B–70B class | Good multilingual | Strong | Community license, commercially usable | Strong alternative base; largest tooling ecosystem |
| **Jais 2 (Core42)** | Arabic-native sizes | Native Arabic | Moderate | Open variants available | Arabic-specialist role in production ensemble |
| **Falcon 3 / H1 (TII)** | Small–mid sizes | Good | Good | Permissive | Regional secondary option |
| **Frontier APIs (Claude, GPT, Gemini)** | — | Strong | Strongest | API only | Synthetic-data generation and optional reasoning tier in hybrid deployments; never a verdict authority outside the Sanad pipeline |

**Selection is empirical, not declared:** the evaluation battery of §16 is run over the shortlist before each training phase, and the base model is whichever wins under the weighted criteria at that time. Model choice is a point-in-time decision revisited at every phase gate; this document fixes the *process*, not a perpetual winner.

### 12.3 Production Ensemble Architecture

- **Core reasoning model:** methodology-tuned 32–70B open-weights model (Layer-2 engine).
- **Arabic specialist:** Arabic-native model for classical-text processing and Arabic-first customer deployments.
- **Fast screener:** small (≤ 8B) distilled model for Layer-1 routine screening at low cost.
- **Consensus mechanism:** for critical decisions, ensemble agreement is required before a V1 verdict is issued without human review.

## 13. Two-Track Training Strategy

### 13.1 Track A — Founder-Executed Prototype (Months 0–3)

**Objective.** Prove that the dual-axis methodology encodes into model weights; produce a working Sanad reasoning adapter deployable into adjacent platforms; create the demonstration and evaluation assets that de-risk the seed round.

**Hardware envelope.** Single-workstation class: 32 GB VRAM GPU (RTX 5090 class), 24-core+ CPU, 256 GB system RAM. All Track-A methods are chosen to fit this envelope with headroom.

**Method.**
- **Base:** 8–14B open-weights model per §12.2 (4-bit NF4 quantized base for training).
- **Stage A1 — Supervised fine-tuning (QLoRA):** LoRA rank 32–64 on attention and MLP projections, bf16 compute, context 8–16K, 2–3 epochs over the SFT corpus (§14). Wall-clock: hours per run, enabling daily iteration.
- **Stage A2 — RLISF via direct preference optimization:** DPO (β ≈ 0.1–0.3) over scholar preference pairs (§15). DPO is chosen deliberately: it delivers preference alignment with a single policy model in memory, where PPO-style RLHF would require policy, reference, and reward models simultaneously resident — infeasible in 32 GB and unnecessary at prototype scale.
- **Packaging:** adapters merged, quantized to GGUF, served locally (LM Studio / llama.cpp / vLLM) as the Layer-2 engine of the prototype pipeline.

**Acceptance gate.** The fine-tune ships only if it beats the same base model driven by the full methodology prompt plus retrieval on the identical evaluation battery (§16). If prompting-plus-RAG wins, that result is itself reported to investors — the architecture works either way; the gate protects intellectual honesty about *where* the methodology lives.

**Deliverables.** Trained adapter; gold dataset (versioned); evaluation report; live demo: claim in → full SanadAssessment out, with visible derivation trace and isnād.

### 13.2 Track B — Funded Production Program (Months 1–24)

The production program restates the four-stage training design at scale:

- **Stage B1 — Domain-integrated SFT (Months 4–9).** Folded domain adaptation: Islamic finance corpus, regulatory standards, and methodology examples trained jointly at 32–70B scale on rented clusters (8× H100-class nodes; rented, not owned — GPU pricing is re-quoted at execution and stress-tested per §26.5). Full-parameter or high-rank LoRA per compute economics at the time.
- **Stage B2 — Full RLISF (Months 8–14).** Scholar panel supplies graded assessments and preference judgments at volume (§15.2); preference optimization scaled via DPO/GRPO-class methods, with a learned reward model introduced only if pairwise data volume justifies it.
- **Stage B3 — Multi-madhab calibration (Months 12–16).** Dedicated data slice and evaluation gate: consistent rulings where schools agree; explicit, correctly attributed divergence flags where they differ; jurisdiction-configurable defaults.
- **Stage B4 — Distillation & deployment (Months 14–18).** Distill the fast screener; harden the ensemble; complete regulatory documentation of the training process itself (increasingly required under AI-act-class regimes, §21).

## 14. Training Data Architecture

### 14.1 Corpora

| Corpus | Content | Scale | Cost | Role |
|---|---|---|---|---|
| **D0 — Classical graded corpus** | Openly licensed ḥadīth collections with isnād chains and scholarly gradings | 10⁴–10⁵ examples | ~$0 (open licenses) | Teaches the *form* of chain reasoning and grade vocabulary before financial specialization — the highest-leverage free asset in the program |
| **D1 — Gold financial cases** | Hand-authored verification cases: claim + sources + full dual-axis analysis, authored and graded by the founder in Track A and by the scholar panel in Track B | 150–300 (Track A) → 5K+ (Track B) | Founder time → panel budget (§19) | Ground truth; evaluation held-out set drawn exclusively from here |
| **D2 — Curated synthetic expansion** | Frontier-model-generated cases prompted with this document as the constitution, then ruthlessly human-curated; includes seeded shudhūdh and iʿlāl defects with known ground truth | 2–5K (Track A) → 50K+ (Track B) | API + curation time | Volume, coverage of edge cases, defect-detection training |
| **D3 — Preference pairs** | Better-of-two analyses of the same case, judged by scholar (founder in Track A; panel in Track B) | 500–2K (Track A) → 25K+ (Track B) | Judgment time | RLISF signal |
| **D4 — Production corpora (Track B)** | Licensed financial data, AAOIFI standards, regulatory archives, fatāwā collections, annotated transactions | Per §20 licensing plan | $2.4M/yr + $850K setup | Domain depth and compliance-annotation supervision |

### 14.2 Label Discipline

Every training example carries dual-axis labels under the schema of Appendix B. Three rules protect label quality: (a) Axis-1 grades in training data must match the registry — no example may contradict the source registry's grade for a real source; (b) every verdict must be reproducible from the stated evidence via R1–R6 — an annotator who cannot write the derivation trace may not assign the verdict; (c) inter-annotator agreement is measured on a shared calibration slice before any annotator's labels enter the corpus (Track B), with the founder's Track-A labels serving as the initial calibration standard.

### 14.3 Synthetic Generation Protocol

Generation prompts embed Part I of this document verbatim as the constitution. Every synthetic case is checked for: derivation-trace validity (rules actually support the verdict), band-boundary coverage (deliberate oversampling near boundaries where classifiers fail), defect realism (seeded iʿlāl cases modeled on documented manipulation patterns), and linguistic balance (Arabic and English cases at parity for the bilingual-consistency KPI). Synthetic data that merely paraphrases gold cases is rejected; the target is coverage, not volume.

## 15. RLISF — Reinforcement Learning from Islamic Scholar Feedback

### 15.1 The Concept

RLISF is the program's signature training innovation: preference optimization in which the reward signal is qualified scholarly judgment applied through the classical methodology, rather than generic human preference. The scholar is not rating helpfulness; the scholar is rating *fidelity to the verification method* — did the analysis grade sources correctly, attempt reconciliation before declaring shudhūdh, respect the weakest-link rule, refuse to assert an unshown chain.

### 15.2 Implementation by Track

- **Track A:** the founder, acting as the scholar of record, produces pairwise judgments (D3) applied via DPO. This is full RLISF in miniature — the same signal, one judge, direct optimization.
- **Track B:** the governed panel (§19) supplies volume judgments through purpose-built annotation interfaces designed to minimize scholar technology burden. Preference data is collected with madhab attribution so Stage B3 calibration can measure and manage school-level variation rather than averaging it away. Optimization scales through DPO/GRPO-class methods; a learned reward model is introduced only when pairwise volume and diversity justify the added machinery.

### 15.3 Judgment Protocol

Each preference judgment records: the winning analysis, the specific rule violations or excellences that decided it, and a severity tag. This turns every preference pair into an interpretable audit record — and gives Layer 4 the error taxonomy it needs for targeted retraining.

## 16. Evaluation & Calibration Framework

All metrics are computed on held-out gold data (D1) never seen in training, with the following battery run at every phase gate:

| Metric | Target (Track A) | Target (Production) |
|---|---|---|
| Axis-1 grading accuracy (exact band / within one band) | ≥ 80% / ≥ 95% | ≥ 90% / ≥ 98% |
| Axis-2 verdict accuracy (exact band / within one band) | ≥ 75% / ≥ 93% | ≥ 88% / ≥ 97% |
| Derivation faithfulness (trace validly supports verdict, rubric-scored) | ≥ 85% | ≥ 94% |
| Tawātur judgment agreement (incl. independence-test correctness) | ≥ 80% | ≥ 85% |
| Shudhūdh detection precision / recall on seeded anomalies | ≥ 75% / ≥ 80% | ≥ 85% / ≥ 88% |
| Iʿlāl screening recall at ≤ 20% escalation rate | ≥ 80% | ≥ 85% |
| Calibration error (confidence vs. realized accuracy, per band) | ≤ 7 pts | ≤ 5 pts |
| Multi-madhab consistency (agreement where schools agree; correct divergence-flagging where they differ) | ≥ 85% | ≥ 90% |
| Arabic–English consistency (same case, both languages) | ≥ 94% | ≥ 97% |
| Escalation precision / recall (flags the right 10%) | ≥ 75% / ≥ 90% | ≥ 85% / ≥ 95% |

**Standing baseline requirement.** Every fine-tuned checkpoint is benchmarked against (a) its own base model with full methodology prompt + retrieval and (b) the best available frontier API with the same prompt + retrieval. Shipping requires beating (a); the gap to (b) is tracked as the distillation opportunity.

## 17. Technical Fallback Strategy

| Trigger | Condition | Response |
|---|---|---|
| Checkpoint gate failure | Fine-tune fails the §13.1 acceptance gate after two data-quality iterations | Ship prompting-plus-RAG architecture on the same pipeline; continue fine-tuning research off the critical path |
| RLISF underperformance (Track B) | Stage B2 accuracy below SFT-only baseline at Week 8 review | Revert to SFT-only production model (expected 3–5 point accuracy cost); redirect scholar budget from preference volume to gold-case volume |
| Base-model discontinuity | Chosen base family license or availability changes | Re-run §12 selection; adapters and data are base-portable by design (no base-specific formats in the corpus) |
| Scholar-panel assembly delay | Panel below quorum at Month 6 | Founder + minimum 3 committed scholars operate an interim panel; $800K reserve activates contract annotation; academic partnership channel opens as an alternative feedback source |
| Infrastructure cost shock | GPU costs breach the 2× stress scenario (§26.5) | Shift production inference mix toward the distilled screener; renegotiate reserved capacity; pass through infrastructure premiums on top-tier SLAs |

---

# Part IV — Domain Implementation

## 18. Islamic Finance Specialization

### 18.1 Dual-Compliance Verification

Islamic financial institutions carry a structural burden no conventional competitor shares: every decision must satisfy conventional regulation *and* Sharia governance. SanadFinance-LLM treats this as one verification problem with two rule sets, sharing the same isnād, the same source registry, and the same verdict discipline.

### 18.2 Evidence Standards by Ruling Class

| Ruling class | Required standard | Rationale |
|---|---|---|
| Fundamental permissibility determinations (core ḥalāl/ḥarām) | **Tawātur-level scholarly consensus** | Foundational rulings demand the highest classical evidence standard; the system will not synthesize a novel core ruling from sub-tawātur evidence |
| Instrument-level compliance (ṣukūk structures, murābaḥa terms, screening) | **Ṣaḥīḥ-level verdict** on the compliance chain, anchored in recognized standards (AAOIFI) and panel-validated precedent | Routine but consequential; auditable chain to standards required |
| Operational screening (portfolio filters, transaction monitoring) | **Ḥasan-level or better**, with automatic escalation of borderline cases | Volume operations with human backstop |

Where recognized schools genuinely differ, the system returns the divergence explicitly with madhab attribution and applies the deployment jurisdiction's configured default — it never averages across schools into a ruling no school holds (Stage B3 calibration, §13.2).

### 18.3 Compliance Workflow Products

The MVP product (§25) is transaction-level Sharia compliance verification with full isnād documentation: every compliance determination traceable from transaction attributes through standards citations and panel precedent to the verdict — the audit artifact Sharia boards, external auditors, and regulators each currently reconstruct manually.

## 19. Scholar Panel Governance

### 19.1 Composition

The panel is specified by role and qualification; individual appointments proceed through due-diligence and formal MoU execution during Months 1–2 post-seed.

**Primary panel — seven seats:**
- 2 × Ḥanafī-tradition scholars (largest global school)
- 2 × Shāfiʿī-tradition scholars (Southeast Asia weight)
- 1 × Mālikī-tradition scholar (North/West Africa representation)
- 1 × Ḥanbalī-tradition scholar (Gulf focus)
- 1 × Jaʿfarī-tradition scholar (comprehensive market coverage)

**Qualification criteria per seat:** recognized ijāzah-level training in uṣūl al-ḥadīth or uṣūl al-fiqh; standing in a recognized standards or fatwā body (AAOIFI, IFSB, national Sharia authorities) or equivalent academic chair; published scholarship; no unresolved conflicts with competing Islamic-finance AI ventures. The panel chair additionally requires cross-madhab standing sufficient to mediate Tier-2 disagreements.

**Supporting structure:** 6 junior scholars (Tier-2 review throughput and annotation volume), 4 regional advisors (jurisdiction-specific practice), and a pre-approved reserve list of 3 external senior authorities for Tier-3 consultation.

### 19.2 Engagement Terms

- **Commitment:** minimum 10 hours/month per primary-panel seat; 85% attendance at quarterly in-person sessions (Gulf / Kuala Lumpur rotation).
- **Compensation:** $50K annually plus 0.25% equity vesting over 4 years per primary seat; senior-scholar total program cost within the $3.2M annual panel budget (primary panel $350K per senior seat fully loaded, junior network $180K, regional advisors $150K, training and tooling $500K).
- **Authority:** final approval rights over the methodology implementation (Part I as applied); co-authorship on academic output; formal endorsements for enterprise sales.
- **Protections:** non-compete within Islamic-finance AI verification; documented-opinion rights (minority positions are published internally, never erased).

### 19.3 Decision Rules and Conflict Resolution

- **Consensus requirement:** 5/7 for definitive methodology rulings; 4/7 or below is recorded as "Disputed — multiple views" and surfaced as such to customers, with the conservative interpretation as the system default.
- **Tier 1 — technical disagreements (~60% of conflicts):** 48-hour virtual resolution under rotating senior-scholar leadership; all rulings logged to the panel knowledge base.
- **Tier 2 — jurisprudential differences (~30%):** two-week review with classical-source consultation, chair-mediated; strongest consensus implemented with minority opinion documented.
- **Tier 3 — fundamental methodology disputes (~10%):** 30-day full-panel review; external authority consultation from the reserve list; formal standards-body consultation for major questions; parallel-approach implementation with transparent customer disclosure where consensus is impossible.
- **SLA:** 48 hours (Tier 1), 7 days (Tier 2), 30 days (Tier 3); the escalation hierarchy is designed to make deadlock structurally impossible.

### 19.4 Panel as Data Engine

Beyond governance, the panel is the RLISF supply chain: graded gold cases (D1), preference judgments (D3), calibration sessions that keep grader agreement measurable, and the quarterly review of all Islamic content in the corpus. Annotation interfaces are purpose-built to scholar workflows; scholars grade cases, not JSON.

## 20. Data Acquisition & Licensing

**Annual data budget: $2.4M; initial setup: $850K.**

| Category | Components | Annual Cost |
|---|---|---|
| Islamic-finance regulatory data | AAOIFI standards database ($85K); central-bank publications across 12 jurisdictions ($120K); IMF/World Bank/IFSB country reports ($65K); regulatory filing archives ($200K) | $470K |
| Commercial financial data | Primary market-data terminal/feed licensing ($480K); secondary/backup feed ($350K); credit and market data ($180K); Islamic-finance database ($95K) | $1,105K |
| Islamic scholarly content | Contemporary fatāwā collections ($80K); scholarly journal archives ($45K); Arabic–English translation services ($200K); classical-text digitization ($150K one-time, in setup) | $325K |
| Proprietary data development | Scholar interview program ($300K); primary research ($180K); validation studies ($120K); historical case-study development ($90K) | $690K |
| **Openly licensed classical corpora (D0)** | Graded ḥadīth collections with isnād chains under open licenses | **$0** |

**Risk management:** multi-vendor agreements against single-source dependency; tiered licensing scaled to customer growth; regional providers per target market; contractual fallback feeds for critical data. **Quality assurance:** minimum three-source cross-validation for registry-critical facts; quarterly panel review of all Islamic content; automated integrity monitoring; full version control so every historical verdict remains reproducible against the data that produced it.

## 21. Regulatory Compliance & International Expansion Mapping

### 21.1 Compliance-by-Architecture

The system's native outputs — complete decision provenance, source attribution with reliability basis, documented human-review involvement, statistical foundations for every confidence score — are the artifacts financial AI regulation increasingly demands. Compliance documentation is a byproduct of the verification method, not a parallel workstream. Standing integrations target IFRS/GAAP reporting contexts, Basel-framework risk documentation, AAOIFI and IFSB standards, and AI-specific regimes (EU AI Act high-risk classification, NIST AI RMF alignment).

### 21.2 Market-Entry Regulatory Map

| Market | Launch | Key Regimes | Path & Cost | Timeline |
|---|---|---|---|---|
| **UAE/GCC** | Month 18 | CBUAE AI guidance, DFSA framework, emirate-level licensing | Fintech fast-track; local Islamic-bank partnerships; ~$1.1M | 4–6 months |
| **Singapore** | Month 20 | MAS AI governance framework | Regulatory sandbox (6-month test); ~S$800K; ASEAN hub | 8–10 months |
| **Malaysia** | Month 22 | BNM guidelines; established Sharia-governance regime | Expedited Islamic-fintech path; ~$280K; local-ownership structuring assessed | 6–8 months |
| **United Kingdom** | Month 28 | FCA AI guidelines, PRA framework | FCA sandbox (12-month); ~£1.8M | 10–12 months |
| **European Union** | Month 24 (prep) | EU AI Act high-risk classification, MiFID II, GDPR | Conformity assessment, CE marking, EU data residency; ~€2.8M | ~18 months |
| **United States** | Month 30 | SEC/FINRA/OCC guidance; state banking licensure (NY, CA, TX) | Principles-based readiness + state licensing; ~$3.2M | 12–15 months |
| **Indonesia** | Month 36 | Developing AI governance; OJK | Partner-led entry with local banks; ~$450K | ~12 months |
| **Pakistan** | Month 40 | Central-bank fintech framework in development | Government-partnership entry; ~$320K | ~15 months |

**Total international expansion investment:** $18.5M over 24 months, with a standing 30% timeline buffer, a $2.5M annual multi-jurisdiction legal reserve, and a dedicated regulatory-monitoring function. Sequencing principle: Islamic-finance-advantage markets first (GCC, Malaysia, Singapore), regulatory-clarity markets second (UK, EU), scale-justifies-complexity markets third (US, Indonesia).

## 22. Beyond Finance: Healthcare, Labor, E-Commerce

The methodology is domain-general; the registry contents and evidence standards are domain-specific. Post-Phase-2 expansion candidates, in priority order of regulatory pull:

- **Healthcare:** evidence-hierarchy integration (trial grades map naturally onto the verdict ladder); patient-safety-critical claims held to tawātur-level standards; currency weighting for fast-moving clinical literature.
- **Labor & employment:** regulatory-compliance verification across jurisdictions; bias and fairness screening as a shudhūdh specialization; institutional-source prioritization for safety-critical information.
- **E-commerce & consumer protection:** product-claim and review authenticity at volume; manipulation detection as the iʿlāl specialization; real-time assessment tiers matched to marketplace dynamics.

Each expansion reuses the full stack — registry, ledger, pipeline, model — with a domain rule-pack and domain gold data; the marginal cost of a new domain is data and calibration, not architecture.

---

# Part V — Business Plan

## 23. Market Opportunity

### 23.1 Market Sizing

- **Global financial services (2025):** $36.0T — banking & capital markets $16.9T, insurance $8.6T, asset management $5.4T, fintech & digital $5.1T.
- **AI in financial services:** $46.2B (2024) → $147.8B (2030), 21.4% CAGR — risk & fraud 35%, algorithmic trading 28%, customer service & advisory 22%, regulatory compliance 15%.
- **Islamic finance (Phase-1 focus):** $5.2T (2025) → projected $9.75T (2030), 15–18% CAGR. Composition: Islamic banking $3.43T (66%), ṣukūk $1.04T (20%), Islamic funds $416B (8%), takāful $312B (6%). Geography: GCC 42% ($2.18T), Southeast Asia 31% ($1.61T), MENA ex-GCC 15% ($780B), other 12% ($624B).
- **Serviceable addressable market:** Phase 1 (Years 1–3) $35.2B — Islamic banking AI verification $24.1B, fintech/investment $7.6B, regulatory & compliance services $3.5B. Phase 2 (Years 4–7) $32.6B — global investment banks $24.8B, ESG asset managers $7.0B, RegTech $0.8B. **Combined 7-year SAM: $67.8B.**

### 23.2 Pain Points → Solutions

| Market pain | Cost of status quo | SanadFinance-LLM answer |
|---|---|---|
| Unexplainable AI decisions; regulators demand audit trails | Blocked AI adoption in regulated functions | Complete isnād per recommendation; derivation traces built for audit |
| No standard for source credibility; data-quality failures | ~$3.1T estimated annual global losses to poor data quality | Registry-governed Axis-1 grading with track-record dynamics |
| Dual-compliance burden in Islamic finance | Manual Sharia processes; avg. $274M annual multi-jurisdiction compliance cost at large institutions | One pipeline, two rule-sets; standards-anchored compliance verdicts |
| Confidence scores without epistemology | Ungrounded risk attribution | Dual-axis verdicts with calibration guarantees (§16) |

## 24. Competitive Landscape, Moats & IP Strategy

### 24.1 Incumbents and Gaps

| Player | Strength | Gap SanadFinance-LLM exploits | Price point |
|---|---|---|---|
| Bloomberg (terminal + AI) | Data breadth, incumbency | No epistemological method; black-box AI; no Islamic specialization | $24–30K/terminal/yr |
| Refinitiv/LSEG | Analytics, compliance tooling | Rule-based compliance without chain-of-transmission | $22–25K/yr |
| FactSet | Portfolio analytics | No source-reliability grading; thin Islamic coverage | $12–18K/user/yr |
| Kensho (S&P) | Event-driven ML | Confidence scores without methodological basis | Enterprise |
| AlphaSense | AI document search | Search, not verification; no reliability scoring | $1.8K+/user/yr |
| Islamic-fintech specialists | Domain focus | Manual processes; no verification AI; limited scale | Consultancy-priced |

**Positioning:** "The only financial AI with 1,400 years of verification methodology." Pricing is a capability premium, not a discount play: enterprise contracts around $120K+ against $24K terminals, justified by compliance-grade explainability, dual-compliance coverage, and audit-ready output.

### 24.2 Competitive Response Readiness

- **Bloomberg-class response (18–24 months to integrate Islamic verification):** counter with 12-month speed-to-market on the MVP, 3+ core patent filings, 20+ flagship banks under 3-year contracts, and exclusive advisory lock-up of the leading scholar network before incumbent entry.
- **Refinitiv-class response (12–18 months):** counter on epistemological depth vs. rule-tables, first regulatory approvals in 2+ jurisdictions, and deep workflow integration raising switching costs.
- **S&P/Kensho-class response (24–36 months):** counter on scholarly legitimacy that cannot be acquired quickly, and target 70%+ Islamic-finance-AI share before entry.
- **Startup competition:** counter on talent, 2+ years of accumulated customer feedback, multi-jurisdiction certifications, and funding cadence.
- **Standing posture:** quarterly competitive-intelligence reviews, early-warning triggers on patent filings and key hires, and a 90-day response playbook.

### 24.3 Defensive Moats

Methodology depth (scholarship + AI expertise co-resident in one team); the proprietary source-reliability database compounding with usage; network effects (verification accuracy improves with customer volume through Layer 4); regulatory certifications as switching costs; and exclusive scholar relationships.

### 24.4 IP Strategy

- **Patents (file Months 3–6; ~$350K Year 1, $700K over three years):** (1) isnād architecture for financial data verification (chain-of-transmission tracking); (2) automated jarḥ wa taʿdīl source-criticism system (dual-axis grading with registry dynamics); (3) tawātur consensus mechanism (impossibility-of-collusion testing). Jurisdictions: US, EU, GCC via PCT, plus Malaysia/Singapore for core filings.
- **Trade secrets:** scholar-feedback training corpus; scoring weights and thresholds; customer integration patterns; jurisdiction compliance mappings — protected by comprehensive NDAs, need-to-know segmentation (no single employee holds complete system knowledge), and quarterly audits.
- **Defensive publication:** general methodology papers and standards-body contributions (AAOIFI collaboration) establishing prior art and academic legitimacy without implementation disclosure.
- **Founder IP:** the Sanad Trust Framework and the ʿIlm al-Ḥadīth operationalization methodology originate as founder intellectual property, assigned to the company at incorporation under standard founder-IP terms.

## 25. Go-to-Market Strategy

### 25.1 MVP Beachhead (Months 1–18): One Product, One Segment

**Product:** Islamic Banking Compliance Verification — transaction-level, real-time Sharia compliance verdicts with full isnād documentation. **Target:** the top 50 Islamic banks, concentrated in UAE, Saudi Arabia, and Malaysia. **Contract:** $40–120K ACV SaaS during the beachhead. **Discipline:** no product diversification (no API tiers, no licensing plays) until the beachhead proves out at **$8M ARR and 95%+ customer satisfaction**. Rationale: concentrated engineering and sales force on one perfected offering; simplified market education for a novel methodology; deep anchor-customer case studies; RLISF validated at scale before broader application.

### 25.2 Paid Proof-of-Concept Model

- **Structure:** 30–45-day paid POCs — $25K base (setup + integration) plus a transaction-volume fee of 5 basis points per $1,000 verified, targeting ≥ $500M verification volume per pilot; typical pilot revenue $50–75K.
- **Economics:** direct pilot cost $35–45K → pilot-phase gross margin 40–50%; the pilot program is cash-positive in aggregate (~+$500–750K across the first cohort).
- **Conversion:** POC success criteria ($500M+ volume, 95% accuracy threshold) trigger a committed 18-month minimum subscription.
- **Rationale:** paid POCs validate genuine intent, compress the sales cycle, prove usage with transaction volume rather than promises, and eliminate free-pilot cash drag.

### 25.3 Sales Capacity Model

| Period | Headcount | Avg quota/AE | Win rate | Closes/month | Cumulative customers |
|---|---|---|---|---|---|
| Months 1–6 | 2 AE + 1 SDR | $1.5M | 15% | 1.5 | 9 |
| Months 7–12 | 4 AE + 2 SDR | $2.0M | 25% | 4.0 | 33 |
| Months 13–18 | 6 AE + 3 SDR | $2.5M | 30% | 7.5 | 78 |
| Months 19–24 | 8 AE + 4 SDR | $2.8M | 35% | 11.2 | 145 |
| Months 25–36 | 10 AE + 5 SDR | $3.0M | 40% | 16.7 | 225+ |

Assumptions: 9–15-month sales cycles compressing with references; 6-month AE ramp; 15–20 named accounts per AE territory. Against the 144-customer break-even requirement (§26.3), the model carries a ~56% capacity buffer at Month 36.

### 25.4 Scholar Referral Program

$10K grant per successful customer introduction (signed contract within 12 months), targeting 100+ standards-body scholars, professors, and industry authorities; 0.5% equity bonus at 3+ successful referrals. Expected contribution: 30–40% of pipeline, 3–4-month sales-cycle compression, 15–20-point win-rate lift on referred deals — at $10K per referral against a $65K flagship-segment CAC.

### 25.5 Channels, Segments, and Phase-2 Expansion

- **Segments (post-beachhead):** Islamic banks ($250K–2M deals, 9–15-month cycles); ṣukūk issuers and Islamic capital markets ($500K–5M, 12–18 months); Islamic fintech (API-led, $50–500K, 3–6 months).
- **Partners:** cloud co-sell (Azure, AWS, Oracle), Big-Four Islamic-finance practices, core-banking integrators (Temenos, Path Solutions, regional SIs). Partner margins: 15–20% of first-year ACV (implementation), 10% (referral), 5% revenue share (technology); ~$750K annual partner budget.
- **Phase 2 (Months 19–42):** positioning evolves from "the Islamic finance AI platform" to "the world's most transparent financial AI," targeting ESG-mandated institutions, regulation-heavy financial services, and alternative-investment due diligence, with regional hubs in London, New York, and Singapore per the §21.2 sequence.
- **Onboarding:** 90-day structured program (integration → configuration and training → validated production), one CSM per major bank, 24/7 support in Arabic, English, and Bahasa; training investment $75–150K per institution.

## 26. Financial Model

*All figures below are the Conservative Base Case unless labeled otherwise; scenario weights per the Executive Summary table.*

### 26.1 Revenue Plan

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| **ARR** | $1.2M | $4.8M | $14.4M | $28.8M | $43.2M |
| **Growth** | — | 300% | 200% | 100% | 50% |

Growth ceilings follow institutional-investor guidance (300% maximum early-stage, decaying to mature-SaaS rates). Optimistic case: $2M → $8M → $20M → $35M → $52.5M. Conservative case: $0.8M → $2.4M → $6.0M → $12.0M → $18.0M.

Revenue mix during the beachhead is deliberately single-product SaaS plus POC fees; the multi-tier revenue architecture (usage-priced API at $0.05–1.00/call, enterprise SaaS at $2.5–12K/user/month, platform licensing at $250K–2M, professional services) activates progressively after the $8M-ARR beachhead gate.

### 26.2 Cost Structure

**Year-1 operating expenses: $14.1M** — R&D & engineering $4.2M (30%); Islamic scholarship program $3.2M (23%); data licensing & acquisition $2.4M (17%); sales & marketing $1.5M (11%); G&A $1.4M (10%); cloud & GPU infrastructure $1.4M (10%). Years 2–3 opex: $23.0M and $28.0M respectively (scaled per the burn bridge below, and inclusive of the §26.5 infrastructure stress base case).

### 26.3 Cash Burn vs. ARR Bridge

| | Y1 | Y2 | Y3 |
|---|---|---|---|
| ARR | $1.2M | $4.8M | $14.4M |
| Net cash burn | $14.1M | $18.2M | $24.8M |
| ARR coverage of burn | 8.5% | 26.4% | 58.1% |
| Runway instrument | $15M Seed | $40M Series A | Series B + path to break-even |
| Next-raise trigger | Month 9 (≤ $4M runway) | Month 18 (≤ $8M runway) | Month 30 (profitability path) |

**Break-even:** Month 42 (Q2 Y4) cash-flow positive at $28.8M ARR against ~$26M expenses; Month 45 EBITDA-positive; Month 48 net-profitable. Probability-weighted expected break-even: Month 44. Customer count at break-even: **144 customers at $200K average steady-state ACV.**

### 26.4 Unit Economics & Gross-Margin Progression

- **CAC by segment:** flagship Islamic banks $65K (MVP focus); regional banks $35K (post-MVP); smaller institutions $15K (Year 3+).
- **LTV:** $320K average on a conservative 3-year tenure → **MVP LTV/CAC 4.9:1**, blended 7.8:1 by Years 2–3, 12.8:1 in the optimistic retention scenario.
- **Cohort gross margins:** pilot cohort 40–50% (paid-POC economics); Year-1 cohort 46% ($120K ACV, $65K direct cost — high-touch onboarding); Year-2 cohort 75% ($180K ACV, $45K direct); steady state 82.5% ($200K ACV, $35K direct — 10% scholar time, optimized data costs).
- **Blended company gross margin:** 25% (Y1) → 62% (Y2) → 78% (Y3) → 82% (Y4+). Margin composition honestly includes data licensing (~12% of revenue), scholar program (~8%), customer success (~7%), and infrastructure (~5%) — the 65% margin assumed at break-even is the conservative planning figure, with 82% the operational-maturity ceiling.
- **Sensitivities:** ±10% customer-acquisition rate = ±3 months to break-even; ±$50K ACV = ±4 months; ±20% churn = ±6 months.

### 26.5 Infrastructure & Treasury Stress Scenarios

GPU economics are re-quoted at execution (hardware generations and rental pricing move faster than planning documents); the model therefore stress-tests *multiples*, not vendor price cards. The scaling curve runs development cluster → early production → scale ramp → full production, sized to a 1,000-RPS concurrent load at < 2s P95 latency, with the distilled Layer-1 screener absorbing routine volume.

| Scenario | GPU cost multiple | Break-even impact | Gross-margin impact | Funding impact |
|---|---|---|---|---|
| Base | 1× | Month 42 | 65% at break-even | $95M to plan |
| High-performance (P95 > 3s or > 2,000 RPS) | 2× | +6 months | −7 pts | +$20M buffer |
| Extreme (multi-region + data-residency builds) | 3× | +12 months | −13 pts | +$45M buffer |

Mitigations: small-model routing for routine queries; regional edge clusters where residency demands them; cloud-partnership credits; infrastructure pass-through pricing on premium SLAs.

**FX & treasury.** Revenue currencies at Year 3: USD 40%, EUR 25%, GBP 15%, MYR/SGD 10%, AED/SAR 10%; net exposure $15–25M annually by Year 3. VaR-based hedging budget: $150K (Y1) → $320K (Y2) → $450K (Y3), plus a $200K extreme-scenario reserve. Instruments are Sharia-compliant throughout — waʿd-based forwards and commodity structures, no speculative derivatives — with the hedging program itself panel-reviewed. Limits: ≤ 20% of quarterly revenue unhedged; VaR ≤ 3% of cash reserves at 95% confidence; monthly FX reporting.

## 27. Funding Strategy

### 27.1 Rounds

| Round | Timing | Amount | Pre-money | Primary uses | Investor profile |
|---|---|---|---|---|---|
| **Seed** | Months 1–3 | $15M | $35M | Team formation, Track-B program launch, scholar MoUs, POC cohort; covers Y1 opex $14.1M + $0.9M buffer (~12–15-month runway, extended by POC revenue) | Islamic-finance VCs, AI seed funds, strategic angels |
| **Series A** | Month 12 | $40M | $160M | Product scaling, sales expansion, scholar-network scaling, international preparation | Tier-1 VC + strategic financial investors |
| **Series B** | Month 18 | $25M | $280M | Global expansion, advanced R&D, strategic partnerships | Growth equity + strategic bank investors |
| **Series C** | Month 30 | $50M | $500M | International expansion, acquisitions, advanced research; exit preparation | Late-stage funds, sovereign wealth funds |

**Capital definitions (used consistently):** capital to break-even, base case ≈ **$95M**; risk-adjusted expected requirement **$100M**; full planned raise path including growth capital **$130M** (planning upper bound); bear case including a $35M emergency bridge **$165M** over 54 months.

### 27.2 Series-A Trigger Matrix ($160M pre-money gate)

| KPI | Threshold | Rationale |
|---|---|---|
| Revenue traction | $4.8M ARR run-rate | Product-market fit proven |
| Customer base | 15+ enterprise customers | Concentration risk reduced |
| Logo quality | 3+ tier-1 Islamic banks | Market-leadership validation |
| Gross margin | > 65% sustained on post-pilot cohorts | SaaS-grade unit economics |
| LTV/CAC | > 5:1 proven | Sustainable growth economics |
| Regulatory | Approvals/sandbox admissions in 2+ jurisdictions | Execution risk removed |
| Technical | ≥ 90% verdict accuracy, < 2s P95 | Production readiness |
| Team | CTO + Chief Scholar hired | Key-person de-risking |
| IP | 2+ patents filed | Moat established |
| Validation | Scholar panel operational at quorum | Methodology legitimacy secured |

Valuation bridge: ~12× ARR base ($57.6M) plus growth premium to $160M, against 15–25× comparables for specialized AI/fintech at Series A; full trigger achievement is modeled as removing ~80% of execution risk from the seed-stage position.

### 27.3 Dilution & Downside Honesty

Base-case cumulative founder dilution across the $130M path at planned valuations: **65–75%**; bear case with down-rounds: **75–85%**, with $130M+ in liquidation preferences ahead of common and probable board-control demands from Series B onward. Mitigations pursued from the seed stage: revenue-based financing for 20–30% of later capital needs; strategic-investor valuation premiums (15–25% from Islamic-finance strategics); milestone-staged releases; weighted-average anti-dilution on early rounds; founder-vesting acceleration on defined milestones. FX exposure on valuation: −15–20% in a major-devaluation bear case, +10–15% on emerging-currency strength.

## 28. Risk Management

| Risk | Assessment | Mitigation | Contingency |
|---|---|---|---|
| **Market adoption** — slower Islamic-finance AI uptake | Sales cycles already modeled at 9–15 months; conservative case models 12–24 | Paid-POC validation; scholar-referral channel; regulator co-engagement | Opex reduction path; dual-track conventional-ESG positioning |
| **Competitive** — incumbent integration or acquisition plays | Bloomberg-class 18–24 months; Refinitiv-class 12–18 | Speed to market, patents, contract lock-ups, scholar exclusivity (§24.2) | Strategic partnership or acquisition optionality |
| **Regulatory** — AI-regulation shifts | Multi-jurisdiction complexity is also the moat | Compliance-by-architecture; sandboxes; $2.5M legal reserve; 30% timeline buffers | Pivot weight toward pure audit/compliance products |
| **Technical** — training-program shortfalls | Bounded by §17 fallback ladder | Standing baseline gates; base-portable data assets | Prompting-plus-RAG ships on the same pipeline |
| **Scholar network** — assembly delay or competitive bidding on marquee scholars | Advisory costs could inflate 2–3× under competition | Role-based recruitment across a deep bench; equity alignment; $800K annotation reserve | Interim 3-scholar quorum + academic partnerships |
| **Funding** — market windows | Cadence triggers at Months 9/18/30 | 18-month post-round runway discipline; multiple investor relationships | Bridge from insiders; revenue-based financing |
| **Key person** — founder concentration pre-team | Highest at pre-seed | CTO and Chief Scholar as first hires; documented methodology (this document) as institutional memory | Board-approved succession protocol at Series A |
| **International execution** — management bandwidth across 4+ markets | Explicitly acknowledged as high-execution-risk | Sequential entry, country managers hired 6 months ahead, pilot-first per market | Delay US/EU by 12–18 months without touching the beachhead |

---

# Part VI — Execution

## 29. Integrated Roadmap

**Track A — Months 0–3 (pre-seed, founder-executed):**
Unified specification (this document) → gold dataset D1 authored and versioned → D0 classical-corpus preparation → SFT + DPO prototype trained on workstation infrastructure → evaluation report against the §16 battery → live demonstration pipeline (claim in, SanadAssessment out). **Exit criterion:** demo-grade Layer-2 engine plus evaluation evidence sufficient for seed diligence.

**Phase 1 — Foundation (Months 1–6, post-seed):**
Source registry and isnād ledger in production; Layer-1 screening live; scholar-panel MoUs executed and first methodology validation review held; patent filings; first paid POCs signed. **Targets:** registry covering all MVP-relevant source classes; Axis-1 grading accuracy ≥ 85% on registry-backed screening; POC pipeline ≥ 5 flagship banks.

**Phase 2 — Advanced Analysis (Months 7–12):**
Layer-2 comparative engine and tawātur/independence tracer in production; Layer-3 expert-review workflow with full audit trail; 15-bank flagship POC cohort executing; POC→subscription conversions; Series-A trigger matrix achieved. **Targets:** consensus-assessment accuracy ≥ 85%; pilot conversion ≥ 60%; $4.8M ARR run-rate at Month 12.

**Phase 3 — Production Model (Months 13–18):**
Track-B Stages B1–B3: scaled fine-tuning, full RLISF with the panel, multi-madhab calibration; iʿlāl screening at production recall; Layer-4 continuous learning live; Series B. **Targets:** production evaluation battery passed (§16 production column); 78 cumulative customers.

**Phase 4 — Production Launch & Expansion (Months 19–24):**
Full platform GA with 99.9% availability engineering; compliance certifications (SOC 2, ISO 27001) complete; GCC/Singapore/Malaysia market entries per §21.2; Islamic-finance premium features; beachhead gate ($8M ARR) unlocks product diversification. **Targets:** 145 cumulative customers by Month 24; Phase-2 GTM preparation complete.

## 30. Success Metrics & KPIs

**Technical (production targets; Track-A prototype targets in §16):** verdict accuracy ≥ 88% exact-band / ≥ 97% within-one; Sharia-compliance issue detection ≥ 98%; Arabic–English consistency ≥ 97%; methodology-application faithfulness ≥ 94%; calibration within 5 points per band; response ≤ 2s standard / ≤ 10s complex; ≥ 1,000 concurrent verifications; 99.9% uptime; 100% of decisions with complete isnād; iʿlāl screening recall ≥ 85% at ≤ 20% escalation; system error rate < 0.1%; recovery < 15 minutes.

**Islamic-finance compliance:** basic ḥalāl/ḥarām classification ≥ 99%; complex-instrument analysis ≥ 95%; intra-madhab consistency ≥ 97%; cross-madhab handling per §16; contemporary-fatwā integration ≥ 95%; AAOIFI-standards alignment 100%; panel satisfaction ≥ 95% and panel endorsement of system accuracy ≥ 90%; 60% reduction in scholar time per complex ruling.

**Business:** ARR per §26.1; MRR growth ≥ 15% monthly through Month 18; net revenue retention ≥ 110%; gross retention ≥ 95%; CAC payback < 12 months; LTV/CAC ≥ 5:1 (MVP segment) trending to ≥ 7.5:1 blended; NPS ≥ 70; implementation success ≥ 95% within 90 days; expansion revenue ≥ 30% of total by Year 3; verified transaction volume ≥ $100B cumulative by Month 36.

**Customer ROI commitments (the basis of value pricing):** 40–60% compliance-cost reduction; ~70% faster verification cycles; ~80% audit-preparation time reduction; target ≥ 300% customer ROI within 18 months of deployment.

---

## Conclusion

SanadFinance-LLM operationalizes the most rigorous information-verification tradition in scholarly history as working financial infrastructure. The dual-axis grading system carries the classical method's full discipline — sources judged as sources, claims judged as claims, verdicts derived by explicit rules from documented chains — into a domain whose regulatory direction increasingly demands exactly these properties. The two-track development strategy converts that methodology into evidence before it asks for capital: a founder-built prototype proves the encoding, and the funded program scales it under scholarly governance into the definitive verification platform for Islamic finance and, from that beachhead, for transparent financial AI globally.

The opportunity is a $5.2T market growing at 15–18% annually whose defining constraint — dual compliance under scrutiny — is precisely what this architecture answers, defended by moats (scholarship, registry data, certifications, patents) that compound with time and are structurally difficult for incumbents to replicate. Success is measured on four ledgers at once: technical performance, jurisprudential fidelity, commercial results, and the trust of scholars, regulators, customers, and investors — and the system is designed so that the same artifact, the documented chain of transmission, satisfies all four.

---

# Appendix A — Worked Gold Example: Complete Sanad Analysis

**Scenario.** Four reports arrive within one hour concerning a GCC-listed issuer's ṣukūk program:

1. The national exchange's official disclosure portal publishes the issuer's filing: ṣukūk issuance of **$450M** received Sharia-compliance certification from the issuer's Sharia supervisory board.
2. The issuer's investor-relations release announces the certification, stating the program size as **$500M**.
3. An established regional financial daily reports the certification, citing "$500M" and attributing the figure to the company's announcement.
4. An anonymous Telegram channel with no track record claims the certification was **rejected** and the filing is a cover-up.

**Step 1 — Axis-1 resolution (registry lookup).**
Exchange disclosure portal: **S1 (94)** — regulatory filing channel, near-zero error history. Issuer IR: **S4 (63)** — fundamentally truthful, structural self-interest, ṣadūq-class examination required. Regional daily: **S3 (74)** — editorial oversight, sound record. Telegram channel: **Matrūk (< 40)** — anonymous, zero track record, and the registry's manipulation-pattern check matches short-and-distort timing signatures.

**Step 2 — Isnād tracing and informational independence.**
The daily's figure traces upstream to the IR release (informational-independence test fails between sources 2 and 3 on the *amount*: one chain, not two). The filing (1) and the IR release (2) share an institutional origin — one institutional chain for the *event*. The daily's independent editorial confirmation of the *event* (it verified the filing's existence directly with the exchange) constitutes a second chain for the event only.

**Step 3 — Matn analysis and reconciliation (R5).**
Conflict: $450M (S1) vs. $500M (S4, echoed by S3). Reconciliation attempt: program size vs. tranche size, rounding, or announcement-vs-filing scope. The filing text specifies total program size $450M; the IR figure has no reconcilable basis. Resolution: **S1 prevails**; the $500M figure is recorded as an IR error (ṣadūq yahim pattern logged against the issuer's IR ḍabṭ profile; the daily's ḍabṭ record notes uncritical single-source transmission).

**Step 4 — Tawātur assessment.**
Event attestation: two independent chains (filing; editorial verification). Below the lafẓī floor (5) and, more decisively, insufficient independence diversity — **no tawātur**. R2 elevation available (≥ 2 independent supports at ≥ S4): applicable to the *event*.

**Step 5 — Shudhūdh analysis.**
The rejection claim (4) opposes stronger sources irreconcilably → shudhūdh established. Source is Matrūk → excluded from evidence, and the manipulation-timing match escalates a **fraud-signal alert** (Tier-4 protocol) rather than a mere discount.

**Step 6 — Iʿlāl screen.**
No chronological impossibility (filing precedes IR precedes press); no grafting signatures; no unresolved candidates. Screen clear.

**Step 7 — Verdict derivation.**
*Event (certification granted):* R1 — anchor S1 → V1 base 92. R2 — independent S3 corroboration confirms (already V1; recorded). R4 — ḍabṭ composite strong → 92. **Verdict: Ṣaḥīḥ (V1, 92), CI [88, 96].**
*Amount ($450M):* R1 — anchor S1 → V1 base 92; R5 conflict resolved with documented basis; R4 minor deduction for ecosystem noise → **Ṣaḥīḥ (V1, 90), CI [86, 94]**, note attached: "$500M circulating figure is an issuer-IR error."
*Rejection claim:* Matrūk source, shudhūdh, manipulation signature → **Mawḍūʿ (V6, 3)** with fraud alert issued.
Validity horizon: event verdict — until superseding filing; amount — until program amendment filing.

**Step 8 — Emission.** Full SanadAssessment records issued for all three claims with derivation traces and complete isnād; no Layer-3 escalation required (all rules resolved deterministically); fraud alert routed per Tier-4 protocol; two ḍabṭ-profile updates written to the registry.

*This example is the canonical template for D1 gold authoring: every case must exercise at least one rule beyond R1, and the corpus as a whole must cover all rules, all bands on both axes, and both defect families.*

---

# Appendix B — Training Record Schema (JSONL)

One record per line; `input` is what the model sees, `target` is the supervised completion, `meta` never enters the context.

```json
{
  "record_id": "gold-0147",
  "split": "train",
  "language": "en",
  "input": {
    "claim": "Issuer X's $500M sukuk program received Sharia certification.",
    "sources": [
      {"source_id": "exch-qa-01", "type": "regulatory_filing",
       "axis1_grade": "S1", "axis1_score": 94,
       "dabt_profile": {"composite": 0.95, "scope": "gcc_fixed_income"},
       "content": "…filing text…", "timestamp": "…"},
      {"source_id": "issuer-x-ir", "type": "corporate_ir",
       "axis1_grade": "S4", "axis1_score": 63,
       "conflict_flags": ["self_interested_party"],
       "content": "…release text…", "timestamp": "…"},
      {"source_id": "daily-gulf-fin", "type": "financial_media",
       "axis1_grade": "S3", "axis1_score": 74,
       "upstream_trace": ["issuer-x-ir"],
       "content": "…article text…", "timestamp": "…"},
      {"source_id": "tg-anon-4417", "type": "anonymous_channel",
       "axis1_grade": "MATRUK", "axis1_score": 12,
       "registry_flags": ["no_track_record", "manipulation_pattern_match"],
       "content": "…post text…", "timestamp": "…"}
    ],
    "context": {"jurisdiction": "QA", "madhab_default": "hanafi",
                 "decision_tier": 2}
  },
  "target": {
    "analysis": "…full staged reasoning: axis-1 confirmation, isnād and independence tracing, matn reconciliation, tawātur assessment, shudhūdh finding, iʿlāl screen…",
    "verdicts": [
      {"claim": "certification granted", "grade": "sahih", "band": "V1",
       "score": 92, "confidence_interval": [88, 96],
       "derivation_trace": ["R1: S1 anchor → V1(92)",
                              "R2: independent S3 corroboration (event)",
                              "R4: dabt composite, no change"],
       "valid_until": "superseding_filing"},
      {"claim": "program size", "value": "$450M", "grade": "sahih",
       "band": "V1", "score": 90, "confidence_interval": [86, 94],
       "derivation_trace": ["R1: S1 anchor → V1(92)",
                              "R5: conflict vs $500M resolved, S1 prevails",
                              "R4: −2 ecosystem noise"],
       "notes": "$500M figure is issuer-IR error; single upstream chain"},
      {"claim": "certification rejected", "grade": "mawdu", "band": "V6",
       "score": 3,
       "derivation_trace": ["Matrūk source excluded",
                              "Shudhūdh vs S1/S3 irreconcilable",
                              "Manipulation signature → fraud alert"]}
    ],
    "registry_updates": [
      {"source_id": "issuer-x-ir", "action": "log_error",
       "pattern": "saduq_yahim:program_size"},
      {"source_id": "daily-gulf-fin", "action": "log_note",
       "pattern": "uncritical_single_source_transmission"}
    ],
    "escalation": {"required": false,
                    "fraud_alert": {"issued": true, "tier": 4}}
  },
  "meta": {
    "author": "founder", "annotation_date": "…",
    "rules_exercised": ["R1", "R2", "R4", "R5"],
    "defects_seeded": ["shudhudh"],
    "review_status": "gold_approved",
    "preference_pair_ids": []
  }
}
```

**Field disciplines.** `axis1_grade` must match the live registry for real sources (synthetic sources are namespaced `syn-*`). Every verdict must list `derivation_trace` entries sufficient to reproduce the band from the rules — records failing trace validation are rejected at ingest. `rules_exercised` and `defects_seeded` drive corpus-coverage dashboards so that data gaps, not intuition, dictate the next authoring sprint. Preference pairs (D3) reference two full records sharing an `input` hash and add a `judgment` block: winner, rule-referenced rationale, severity tag, and judge identity — the audit trail that makes RLISF itself verifiable.

---

*End of document.*
