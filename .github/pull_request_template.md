## 📝 Description

What does this PR change?
Which ticket / issue does it address?

---

## 🔐 Security Invariants (MANDATORY)

[ ]  **Zero-Trust Authorization:** All data access is scoped to `current_user.id`. No client-supplied IDs are trusted (No IDOR/BOLA).

[ ]  **Input Rigor:** All inputs validated against strict schemas (e.g., Pydantic / Zod). No blind pass-through.

[ ]  **Mass Assignment Defense:** Sensitive fields (`role`, `subscription_status`, `credits`, `flags`) are explicitly blocked from client updates.

[ ]  **Session Model Integrity:** Access tokens are stateless; Refresh tokens are stored in a durable backend store (Postgres/Redis). NOT in-memory or frontend storage.

[ ]  **Logging Discipline:** No PII, Auth Tokens, or Raw Chat Content logged.

---

## 🔒 AI & Chat Safety (If Applicable)

[ ]  **Token Budgeting:** Input context and output limits enforced server-side before LLM calls.

[ ]  **Prompt Isolation:** System prompt is isolated from user input; no direct concatenation.

[ ]  **Kill Switch Awareness:** Logic respects the `AI_ENABLED` environment variable.

[ ]  **Billing Authority:** Usage/quota enforcement is calculated server-side; frontend is never trusted.

---

## 🛠️ Implementation Details

**Component:** (Auth / Chat / Billing / Infra / Other)

**Database Changes:** (Migrations run? New tables? Indexes?)

**External Dependencies:** (LLM, Stripe, Email, etc.)

**Failure Behavior:**

  • Auth / Billing failures → Fail Closed (Block access)

  • AI Provider failures → Degraded / Safe Response (No crash, no bypass)

---

## 🧪 Testing Performed

[ ]  **Happy Path Tested:** (e.g., successful login / message sent)

[ ]  **Negative / Adversarial Test:** (e.g., tried to access foreign UUID, used expired token, attempted quota bypass)

[ ]  **AuthZ Proof:** (Which middleware/dependency enforces ownership on these routes?)

[ ]  **Unit / Integration Tests:** Added or updated.

---

## ⚠️ Risk & Blast Radius

[ ]  **Critical Path:** Authentication / Session Handling

[ ]  **Revenue Path:** Billing / Credits / Stripe

[ ]  **Brand Risk:** AI Safety / Toxicity / Privacy

[ ]  **Data Integrity:** Deletion / Purge / Irreversibility

---

## 🧠 Security Owner Notes (Optional)

Is there anything specific you want the Security Owner to try to break?

**Focus testing on:**

• Auth / session handling

• BOLA / IDOR

• Mass assignment (e.g., isAdmin, wallet_balance, subscription_status)

• Chat / AI cost abuse (rate limits + token budgets)

• PII redaction & logging discipline

• XSS (render output as text-only)

• SSRF allowlisting
