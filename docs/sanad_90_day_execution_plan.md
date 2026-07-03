# Sanad Track-A Execution Plan — 90 Days
## Training, Benchmark, Evidence Publication & Commercial Deployment

**Owner:** Salim Al-Barami
**Start:** Monday, 6 July 2026 (Week 1) · **Day-90 Decision Gate:** Friday, 2 October 2026
**Companion document:** *SanadFinance-LLM: Unified Development Study* (referenced throughout as **UDS**; §-references point there)
**Operating protocol:** Claude builds and implements; Codex reviews and approves/rejects with exact fixes at every gate; Salim coordinates and is sole grader of gold data.

---

## 0. What This Plan Produces

By Day 90, five assets exist or the plan has honestly falsified itself:

1. **A trained Sanad reasoning adapter** (SFT + DPO on an 8–27B base) that passes — or measurably fails — the acceptance gate against prompted baselines.
2. **SanadBench** (Arabic name option: *al-Miʿyār*): a 200-case public benchmark for calibrated verification, with frontier-model baseline results — the category-defining asset that is valuable *even if the fine-tune loses*.
3. **Protected IP:** provisional patent filing(s) covering the three claim families of UDS §24.4, filed **before** any public disclosure.
4. **Published evidence:** arXiv technical report + benchmark release + eval harness, sequenced after IP protection.
5. **Commercial insertions:** the demo and evidence pack deployed into at least one live pursuit, with observed effect recorded.

**Hard commitments (non-negotiable rules of the plan):**

- **R-A:** No public disclosure of any kind (paper, benchmark, LinkedIn post, conference remark) before the provisional filing date. Publication is prior art against your own patents.
- **R-B:** The 50-case frozen evaluation set is created in Week 3, sealed, and never used for training, prompt tuning, or data debugging. Ever.
- **R-C:** Every gold record is human-verified field-by-field by you, even when AI-drafted. AI-assisted authoring is allowed; AI-graded gold is not.
- **R-D:** The acceptance gate (Phase 4) is reported as measured, including a loss. A negative result ships as a finding, not a secret.
- **R-E:** Day-90 decision is made from the pre-committed criteria in §8, not from enthusiasm on the day.

**Resource envelope (assumptions this plan is sized to):**

| Resource | Budget |
|---|---|
| Your time | 10–14 h/week hands-on + unattended overnight GPU runs (~150 h total across 13 weeks) |
| Hardware | RTX 5090 (32 GB VRAM), Threadripper 7960X, 256 GB RAM, NVMe (≥ 500 GB free for models/data/checkpoints) |
| Cash | Frontier API for synthesis & baselines: $400–800 · Provisional patent: $3–8K (consolidated, counsel-reviewed) · Optional cloud burst (H100 rental for 27B iteration): $0–300 · Tracking/infra: $0 (free tiers) → **Total: ~$4–9K** |

---

## 1. Phase 0 — Decisions & Environment (Week 0–1: Jul 3–12)

### Step 0.1 — Lock the scope decisions (Fri–Sat, 1 h)
Record these in the repo README on day one; changing them later restarts clocks:

- **D1 — Primary base candidates:** Qwen3-14B, Fanar-2-27B-Instruct, and one control (Qwen3-32B if it fits your iteration patience, else Llama-3.3-class). ALLaM enters later as a sovereign-deployment adapter target, not a Week-1 candidate.
- **D2 — Open/closed line (per UDS §24.4):** OPEN → SanadBench, eval harness, technical report, methodology (Part I of UDS, already your defensive-publication layer). CLOSED → gold training data D1–D3, trained adapters, source registry, derivation-rule weights/thresholds.
- **D3 — Language split:** 50/50 Arabic/English across all datasets and the benchmark. Arabic is the moat; do not let it become the afterthought.
- **D4 — Naming:** working names **SanadBench** (benchmark), **Sanad-R** (reasoning adapter). Final naming before publication, not before.

### Step 0.2 — Repository & tracking scaffold (Sat, 2 h)
```
sanad-core/            # PRIVATE (github.com/albarami/, mirror your burhan pattern)
  data/{d0,d1,d2,d3}/  # git-lfs or DVC; encrypted off-site backup
  train/               # configs, launch scripts
  eval/                # harness, graders, results
  registry/            # source registry seed (Postgres schema per UDS §9)
sanad-bench/           # starts PRIVATE, flips PUBLIC at Step 5.4
```
- Experiment tracking: Weights & Biases free tier (or local MLflow if you prefer zero external logging).
- Secrets hygiene: API keys in env vault; gold data never in prompts to third-party APIs except the synthesis flows you explicitly authorize.

### Step 0.3 — Training environment (Sat–Sun, 3–5 h incl. downloads)
Ubuntu 24.04 native (recommended) or WSL2. Blackwell (sm_120) requires current toolchains — install fresh, don't reuse an old env:

```bash
# Conda env
conda create -n sanad python=3.12 -y && conda activate sanad
# PyTorch: current stable with cu128+ wheels (Blackwell/sm_120 support)
pip install torch --index-url https://download.pytorch.org/whl/cu128
# Training stack
pip install "unsloth[cu128]" transformers datasets peft trl bitsandbytes accelerate
pip install llamafactory   # alternative trainer; QCRI post-trained Fanar-2 with it
# Serving & eval
pip install vllm openai anthropic google-genai pandas scipy
```

**Smoke tests (must all pass before Week 1 ends):**
1. `torch.cuda.get_device_capability()` returns `(12, 0)`; bf16 matmul runs.
2. Qwen3-14B loads 4-bit and generates.
3. Fanar-2-27B-Instruct loads 4-bit (~14–15 GB) and generates with its chat template, `<think>` mode on and off.
4. A 10-step QLoRA run completes on a toy dataset without OOM at 8K context (27B: batch 1, grad-accum 16, gradient checkpointing on).
5. vLLM serves one model and the eval harness can hit it.

*Known friction:* if flash-attention wheels fight sm_120, fall back to PyTorch SDPA (`attn_implementation="sdpa"`) — correctness first, speed later. Log every workaround in `ENVIRONMENT.md`; this becomes reusable IP for the SGEIP stack.

**Exit criteria Phase 0:** all five smoke tests green; repos live; decisions recorded. **Codex review: environment sign-off.**

---

## 2. Phase 1 — Pilot Gold + Base-Model Bake-off (Weeks 1–2: Jul 6–19)

### Step 1.1 — Author the 25-case pilot gold set (Week 1, ~6 h)
Method: **AI-drafted, human-graded** (rule R-C). For each case: you specify scenario skeleton (claim domain, sources, intended rules exercised) → Claude drafts the full record per UDS Appendix A/B → you correct every field and assign final grades → Codex spot-reviews 5 of 25 for derivation-trace validity.

Coverage requirement for the pilot (tracked in a coverage matrix from day one):
- All six R-rules exercised at least twice
- Both axes: at least one case per verdict band V1–V6
- Both defect families (shudhūdh, iʿlāl) seeded with ground truth
- 13 English / 12 Arabic
- At least 5 finance cases drawn from live-work patterns (spreading/variance shapes from the bank use case; ṣukūk certification per the Appendix A template)

### Step 1.2 — Build the eval harness v0 (Week 1–2, ~5 h)
A single Python entry point: `eval/run.py --model <endpoint> --suite pilot`. It must compute, per UDS §16:
- Axis-1 accuracy (exact / ±1 band), Axis-2 accuracy (exact / ±1 band)
- Derivation faithfulness (rubric: does the trace validly produce the verdict — LLM-judge scored with your rubric, 10% human-audited)
- Calibration: expected calibration error over verdict confidence, per band
- Escalation precision/recall; abstention correctness
- JSON-schema validity rate (a cheap, brutal early signal)

### Step 1.3 — Bake-off (Week 2, mostly unattended, ~4 h hands-on)
Run each base candidate three ways on the 25 pilot cases: (a) zero-shot with output schema only; (b) full methodology prompt (UDS Part I condensed to ~3K tokens) ; (c) methodology prompt + retrieval stub (registry facts pasted as evidence). Also run two frontier APIs under (b)+(c) as the ceiling reference.

**Selection rule (pre-committed):** primary base = best open model on (b)+(c) weighted per UDS §12.1, with Arabic performance double-weighted for tie-breaks. Expected outcome is Qwen3-14B or Fanar-2-27B as primary and the other as secondary adapter target — but let the numbers decide (UDS §12.2: selection is empirical, not declared).

**Exit criteria Phase 1:** bake-off table complete; primary + secondary base locked; harness runs end-to-end. **Codex review: bake-off memo (approve/reject with fixes).**

---

## 3. Phase 2 — Data Factory & Benchmark Construction (Weeks 2–5: Jul 13 – Aug 9)

### Step 2.1 — D0: Classical corpus preparation (Week 2, ~6 h + overnight jobs)
- Pull openly licensed graded-ḥadīth collections (isnād chains + classical gradings). Verify each corpus license before ingestion; record provenance in `data/d0/SOURCES.md`.
- Transform into instruction format: *given chain + narrator gradings → produce grade with reasoning*, in both directions (grade→justification and chain→grade). Target 5–10K formatted examples after dedup and quality filtering.
- Purpose discipline: D0 teaches the **form** of chain reasoning and grade vocabulary (UDS §14.1). Cap D0 at ≤ 40% of the SFT mix so financial specialization dominates.

### Step 2.2 — D1: Gold corpus to 200 cases (Weeks 2–4, ~25–35 h — the plan's largest human line-item)
- Protocol identical to Step 1.1 (AI-drafted, you-graded, Codex-audited at 10% sampling).
- Throughput target: 12–15 verified cases/week via 3 evening blocks; every case updates the coverage matrix (rules × bands × defect families × language × domain).
- **Week 3, Step 2.2a — SEAL THE FROZEN SET:** select 50 cases by stratified sampling across the coverage matrix, move to `eval/frozen/`, hash the directory, record the hash in the repo README. Rule R-B is now in force. Remaining 150 gold cases = training/dev pool.

### Step 2.3 — D2: Synthetic expansion (Weeks 3–4, ~8 h + API time)
- Generator: frontier API prompted with UDS Part I verbatim as constitution + 3 gold exemplars + a target cell from the coverage matrix (deliberate oversampling of band boundaries and defect cases, per UDS §14.3).
- Volume: generate ~4,000 → auto-validate (schema validity, derivation-trace reproduces verdict under R1–R6, no registry contradictions) → expect ~60–70% survival → you spot-check 5% → **target 2,500–3,000 curated D2 records.**
- Rejection rule: any case that merely paraphrases a gold case is discarded (embedding-similarity filter > 0.92 → reject).
- Cost estimate: $150–500 depending on model choice; log actuals.

### Step 2.4 — D3: Preference pairs for RLISF-as-DPO (Week 4–5, ~10 h)
- For 500–800 training-pool cases: generate two competing analyses (different temperature/model), you judge winner with **rule-referenced rationale + severity tag** per UDS §15.3. Where both are wrong, the gold answer becomes "chosen" and the better generation "rejected."
- Judgment throughput: ~25–35 pairs/hour with a side-by-side judging UI (Claude builds this in Week 3 — a 200-line local web app; do not judge in raw JSON).
- **Target: 600–1,000 pairs**, each an auditable RLISF record.

### Step 2.5 — SanadBench assembly (Weeks 3–5, ~10 h; runs parallel to D1)
The benchmark is a **separate artifact** from the frozen set — it will be public; the frozen set never will be.
- **Composition: 200 cases** — 100 Arabic / 100 English; stratified across V1–V6; ≥ 30 seeded-defect cases (15 shudhūdh, 15 iʿlāl-screen) with documented ground truth; ≥ 40 finance-domain, remainder cross-domain (health, labor, e-commerce per UDS §22) to establish generality.
- Authored under the same gold protocol; zero overlap with training pool or frozen set (hash-checked).
- **Metrics published with the benchmark:** dual-axis accuracy, derivation faithfulness, **expected calibration error** (the headline metric — the hypothesis is that frontier models verify confidently but miscalibratedly), abstention correctness, escalation quality.
- Package: HuggingFace dataset card + GitHub harness + baseline results table + one-command reproduction script. Keep the repo private until Step 5.4.

**Exit criteria Phase 2:** 150 training gold + 50 frozen (sealed) + ~2.5–3K D2 + 600–1K D3 + 200-case SanadBench assembled. Coverage matrix has no empty mandatory cells. **Codex review: data-quality audit on random 20-record sample per corpus.**

---

## 4. Phase 3 — Training Cycles (Weeks 5–8: Aug 3 – Aug 30)

### Step 3.1 — SFT run 1 (Week 5)
Config baseline (adjust per base model; log everything to W&B):

```yaml
method: qlora            # NF4 double-quant base, bf16 compute
lora: {r: 64, alpha: 128, dropout: 0.05, target: all-linear}
context: 8192            # 12-16K only if loss curves demand it
epochs: 2-3
lr: 1.5e-4, cosine, warmup 3%
batch: 1-4 (model-size dependent) × grad-accum to effective 16-32
mix: D1 gold ×3 oversample + D2 + D0 (≤40%) ; 50/50 ar/en enforced per batch
special: Fanar-2 → keep native chat template; train derivation as <think> trace,
         verdict JSON as answer; low LR end (1e-4) — heavily post-trained base
```
Planning throughput on the 5090 (estimates — measure and update Week 5): 14B ≈ 2.5–4K tok/s → full SFT overnight; 27B ≈ 1–1.5K tok/s → 1–2 nights. If 27B iteration exceeds 2 nights/run, burst one Series-of-runs to a rented H100 (~$2–3/h) rather than shrinking the experiment.

### Step 3.2 — Error-driven iteration loop (Weeks 5–7; 3–4 cycles)
After each run: evaluate on a 30-case **dev slice** from the training pool (never the frozen set) → build an error taxonomy (which R-rules fail; which bands confuse; Arabic vs English gap; schema breaks) → fix **data first, hyperparameters second** (80% of gains will come from gold-case additions targeting failure cells) → author 10–20 targeted gold cases → rerun. Each cycle ≈ 3–5 h human + 1–2 nights GPU.

### Step 3.3 — DPO (RLISF) run (Weeks 7–8)
- On top of best SFT adapter: β = 0.1–0.3 sweep (three short runs), lr 5e-6–2e-5, 1–2 epochs on D3.
- Guard-rails: after DPO, re-run the dev slice **plus** a 20-case general-capability sanity set (generic reasoning/instruction tasks) — if general capability regressed > 10%, lower β or mix 10% general SFT data into a brief recovery epoch.
- Output of phase: **Sanad-R v0.1** = merged adapter, plus Q4 GGUF export served in LM Studio/vLLM for the demo.

**Exit criteria Phase 3:** dev-slice performance plateaued across two consecutive cycles; Sanad-R v0.1 frozen and tagged. **Codex review: training-report approve/reject.**

---

## 5. Phase 4 — The Acceptance Gate (Weeks 8–9: Aug 24 – Sep 6)

### Step 4.1 — Pre-registration (before any frozen-set run)
Write `eval/GATE.md` committing to: contenders, metrics, thresholds, and the shipping rule. Contenders:
1. **Sanad-R v0.1** (fine-tune, minimal prompt)
2. Same base model + full methodology prompt + retrieval (**the bar to beat** — rule R-D)
3. Best frontier API + same prompt + retrieval (the ceiling reference)
4. Base model, zero-shot (the floor)

### Step 4.2 — Run once, on the frozen 50 + SanadBench-private
Thresholds (UDS §16 Track-A column): Axis-1 ≥ 80/95 (exact/±1) · Axis-2 ≥ 75/93 · derivation faithfulness ≥ 85 · calibration ≤ 7 pts · escalation P/R ≥ 75/90 · shudhūdh P/R ≥ 75/80 · iʿlāl screen recall ≥ 80 at ≤ 20% escalation · ar/en consistency ≥ 94.

### Step 4.3 — Verdict (pre-committed interpretation)
- **PASS (beats contender 2 on the weighted battery, meets thresholds):** the fine-tune ships as the Layer-2 engine; publication narrative = "methodology encodes into open weights and outperforms prompting."
- **PARTIAL (meets thresholds, ties contender 2):** ship prompt+RAG for product, keep the adapter for sovereign/residency deployments where APIs are non-deployable; narrative = "architecture-first."
- **FAIL (below thresholds):** per UDS §17 — Sanad ships as prompt+RAG governance methodology; the benchmark and frontier-calibration findings become the publication; fine-tuning returns to research track. **This outcome still produces assets 2–5 of §0.**

**Codex review: gate report is the single most scrutinized artifact of the program — approve/reject with exact fixes.**

---

## 6. Phase 5 — IP Protection → Evidence Publication (Weeks 9–11: Sep 1 – Sep 20)

**Sequencing law: 5.1 completes before 5.2–5.6 begin (rule R-A).**

### Step 5.1 — Provisional patent filing (Week 9; start counsel engagement in Week 6 so this doesn't slip)
- One **consolidated provisional** covering the three claim families of UDS §24.4: (i) isnād chain-of-transmission architecture for financial data verification; (ii) automated dual-axis jarḥ wa taʿdīl grading with registry dynamics; (iii) tawātur consensus with impossibility-of-collusion testing. Add (iv) the RLISF preference-audit record structure if counsel agrees it strengthens rather than dilutes.
- Process: you + Claude draft the technical specification from UDS Parts I–III (8–12 h of your time, mostly assembly); IP counsel reviews and files ($3–8K). Twelve-month clock to PCT/full filings starts at filing — diarize Month 11 for the conversion decision, funded or not.
- Trade-secret perimeter reaffirmed in writing the same week: gold data, adapter weights, thresholds (decision D2).

### Step 5.2 — Technical report (Week 9–10, ~12 h)
- Target: arXiv (cs.CL), 8–12 pages. Title shape: *"SanadBench: Calibrated Information Verification with a Classical Chain-of-Transmission Methodology."*
- Contents: methodology (condensed UDS Part I — this doubles as your defensive publication, §24.4), benchmark design, baseline results across frontier + open models, the fine-tuning result **whatever it was** (rule R-D), calibration analysis as the headline finding.
- Positioning rule: the paper sells the *benchmark and the finding*, never the closed product. If frontier models show high accuracy but poor calibration/abstention, that finding alone carries the paper.
- Authors: you; consider one academic co-author (DBA network / Islamic-finance or Arabic-NLP faculty) for venue credibility — their review costs a week, adds citation gravity.

### Step 5.3 — Peer-review track (Week 10, submissions; decisions arrive after Day 90)
- **NLP track:** Arabic-NLP workshop (WANLP-class) or ACL/EMNLP industry track — check current CFP deadlines the week you submit; arXiv preprint goes up regardless.
- **Islamic-finance track:** ISRA International Journal of Islamic Finance or JIABR-class journal for the methodology-application paper (longer cycle; drafts from the same material).
- **Conference talks:** leverage the existing platform record (Oxford AI Forum, UN HLPF lineage) — one abstract submitted to a GCC AI-governance venue.

### Step 5.4 — Benchmark release (Week 10, after arXiv is live)
Flip `sanad-bench` public: HF dataset + harness + leaderboard table + reproduction script + license (CC-BY for data, Apache-2.0 for code). Invite three external labs/teams to submit results in the first fortnight — a leaderboard with only your entries is a poster, not a standard.

### Step 5.5 — Demo & evidence pack (Week 10–11, ~8 h)
- **Live demo:** claim in → full SanadAssessment out (derivation trace + isnād visible), running locally on the workstation; 3-minute recorded version for asynchronous use.
- **Evidence pack v1:** one-page brief; gate report (Codex-approved); benchmark table; 6 deck slides matched to the SG template for direct insertion into pursuit decks.

### Step 5.6 — Narrative cadence (Weeks 10–13)
Three LinkedIn/article beats, in order: (1) the benchmark exists + headline calibration finding; (2) the methodology story (1,400 years → working system); (3) the sovereign angle (Sanad on Fanar/ALLaM — verification methodology on sovereign models). One beat per week; every beat links the arXiv paper, never the closed assets.

---

## 7. Phase 6 — Commercial Deployment of Evidence (Weeks 10–13: Sep 7 – Oct 2)

- **Insertion 1 — Bank pursuit:** Sanad governance layer (isnād audit trail, statement-class Axis-1 grading, R5 variance reconciliation, iʿlāl fraud screen) + fine-tuned Fanar NLG slide-set added to the financial-analytics proposal; demo offered in the technical evaluation session.
- **Insertion 2 — HUMAIN narrative:** Sanad-R on ALLaM positioned as the verification layer of the sovereign strategic-intelligence platform; evidence pack in the co-build deck; if gate = PASS, offer a scoped joint eval on their infrastructure.
- **Insertion 3 — IDIS v6.3:** wire Sanad-R (or the prompt+RAG engine, per gate outcome) as IDIS's verification brain for one full due-diligence case; record before/after analyst effort.
- **Measurement (feeds the Day-90 decision):** for each insertion log — did the asset get airtime; did a client/partner request a follow-up specifically about it; did it change deal state. Evidence of pull, not applause.

---

## 8. Day-90 Decision Gate (Fri, 2 Oct 2026)

Pre-committed matrix — score honestly, decide accordingly:

| Signal | GO (Track-B posture) | HOLD (product-layer posture) | STOP (methodology-only) |
|---|---|---|---|
| Acceptance gate | PASS | PARTIAL | FAIL twice after data iteration |
| SanadBench traction | External submissions or citations within 3 weeks of release | Downloads/interest, no submissions | Silence |
| Commercial pull | ≥ 1 deal visibly moved by the asset; partner requests deeper eval | Airtime but no state change | No airtime requested |
| Publication | Preprint live; venue submission in review | Preprint live | Not shipped (diagnose why) |
| Your conviction cost | You want the funded build **and** a vehicle/team path exists | Value real but belongs inside SG products | Better uses of the hours exist |

- **GO** → activate UDS Track B: seed conversations open with the evidence pack; CTO/Chief-Scholar searches begin; scholar-panel MoU outreach starts (UDS §19).
- **HOLD** → Sanad ships as the governance layer inside SG engagements (bank, IDIS, Fath); revisit venture question at the next natural trigger (e.g., HUMAIN co-build term sheet).
- **STOP** → publish the negative result honestly, keep the benchmark alive at low cost, redeploy the hours. The methodology retains full value as prompt+RAG governance — STOP kills the *training program*, not Sanad.

---

## 9. Operating Cadence, Risks, and Tracking

**Weekly rhythm:** Sunday 30-min plan + coverage-matrix review → Tue/Wed/Thu evening blocks (2–3 h each; authoring, judging, analysis) → overnight GPU runs queued before sleep → Friday 2–4 h deep block (training analysis, writing) → gate weeks: Codex review before the week closes.

**Risk register:**

| Risk | Likelihood | Mitigation | Trigger → Response |
|---|---|---|---|
| Blackwell tooling friction burns Week 0–1 | Medium | SDPA fallback; pinned versions in ENVIRONMENT.md | > 8 h lost → rent cloud H100 for training, keep 5090 for inference/demo |
| Gold-authoring bottleneck (the real schedule risk) | High | AI-drafted protocol; 12–15/week floor; coverage matrix prevents wasted cases | Two weeks < 10 cases → cut D1 target to 150, shift 25 planned cases into SanadBench authoring |
| Day-job crunch (HUMAIN/GADD/bank deadlines) | High | Phases 2–3 tolerate 1-week pauses; frozen-set seal and patent date do not slip | Pause ≥ 2 weeks → shift Day-90 gate accordingly; never compress Phase 4 or 5.1 |
| Gate FAIL | Medium | Pre-committed FAIL narrative (§5.3 of gate); benchmark carries publication | Execute PARTIAL/FAIL branch — assets 2–5 still ship |
| Publication scoop (someone releases a similar verification benchmark) | Low | Provisional filed Week 9; arXiv immediately after | Accelerate 5.2–5.4 by one week; differentiate on Arabic + calibration + classical grounding |
| 27B iteration too slow for the loop | Medium | 14B as iteration model, 27B as release candidate | > 2 nights/run → all iteration on 14B; single final 27B run |

**Definition of done, per artifact:** every deliverable in this plan is done only when (a) it exists in the repo, (b) its metrics/hash are logged, and (c) Codex has issued an approval. Anything else is in-progress.

---

## 10. First 72 Hours (so momentum starts tonight)

1. **Tonight (Fri):** create both repos; write README with the D1–D4 decisions; open the coverage-matrix sheet.
2. **Saturday:** environment build + smoke tests 1–5; start Qwen3-14B and Fanar-2-27B downloads overnight.
3. **Sunday:** author gold cases #1–3 with Claude (ṣukūk-certification template from UDS Appendix A first — it's already written); Codex reviews case #1's derivation trace; book the Week-6 IP-counsel intro call.

*End of plan.*
