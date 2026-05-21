# Codebase Memory: {{PROJECT_NAME}}
> Generated: {{DATE}} | Verified: {{DATE}} | Generator: codebase-memory skill v1
> Modules: {{MODULE_LINKS}}

---

## 1. PURPOSE & DOMAIN

{{PURPOSE}}

---

## 2. HIGH-LEVEL ARCHITECTURE

- **Style**: {{ARCHITECTURE_STYLE}}
- **Language(s)**: {{LANGUAGES}}
- **Entry points**: {{ENTRY_POINTS}}
- **Core data flow**: {{DATA_FLOW}}

```mermaid
graph TD
  {{MERMAID_DIAGRAM}}
```

---

## 3. DIRECTORY MAP

```
{{DIRECTORY_TREE}}
```

---

## 4. KEY DESIGN DECISIONS & PATTERNS

{{PATTERNS}}

---

## 5. CRITICAL DEPENDENCIES

| Library | Purpose | Key files |
|---------|---------|-----------|
{{DEPENDENCIES}}

---

## 6. MODULE REGISTRY

| Module | Path | Deep-dive |
|--------|------|-----------|
{{MODULE_REGISTRY}}

---

## 7. DATA MODELS (summary)

{{DATA_MODELS}}

(Full field detail → relevant module file)

---

## 8. GOTCHAS & NON-OBVIOUS BEHAVIOUR

{{GOTCHAS}}

---

## 9. AGENT TASK ROUTING HINTS

{{ROUTING_HINTS}}
- "Find class X / function Y" → memory/maps/file_index.json
- "Understand import ripple effects" → memory/maps/call_graph.json
