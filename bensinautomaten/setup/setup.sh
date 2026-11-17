#!/usr/bin/env bash
# Sätter upp Bensinautomaten som ett eget projekt i din Multica-workspace via Multica CLI.
#
#   ./bensinautomaten/setup/setup.sh              kör på riktigt
#   DRY_RUN=1 ./bensinautomaten/setup/setup.sh    visar bara kommandona
#
# Valfria miljövariabler:
#   RUNTIME_ID=<id>   vilken runtime (dator + AI-verktyg) agenterna ska köra på
#   SKIP_ISSUES=1     skapa inga demotankningar
#
# Regelboken läggs i projektbeskrivningen, inte i workspace-kontexten. Då kan Bensinautomaten
# och Supportfabriken ligga i samma workspace utan att deras regler blandas ihop.
#
# Kräver: multica (inloggad via `multica setup`), python3, zip.
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

DRY_RUN="${DRY_RUN:-0}"
PROJECT_TITLE="Bensinautomaten"

steg() { printf '\n\033[1;36m▶ %s\033[0m\n' "$*"; }
info() { printf '  %s\n' "$*"; }
varn() { printf '  \033[1;33m⚠ %s\033[0m\n' "$*"; }

run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    { printf '  $ %q' "$1"; shift; for a in "$@"; do
        if [[ ${#a} -gt 60 ]]; then printf ' %q' "${a:0:57}..."; else printf ' %q' "$a"; fi
      done; printf '\n'; } >&2
    echo '{"id":"DRY-RUN-ID"}'
  else
    "$@"
  fi
}

# Hämtar "id" ur JSON på stdin. Med ett namn som argument letas objektet med det namnet upp i en lista.
json_id() {
  python3 -I -c '
import json, sys
namn = sys.argv[1] if len(sys.argv) > 1 else None
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if isinstance(d, dict):
    for k in ("data", "items", "skills", "agents", "results"):
        if isinstance(d.get(k), list):
            d = d[k]; break
if isinstance(d, dict):
    d = [d]
for o in d:
    if isinstance(o, dict) and (namn is None or o.get("name") == namn or o.get("title") == namn):
        print(o.get("id", "")); break
' "$@"
}

# ---------------------------------------------------------------------------
steg "Kontrollerar förutsättningar"
for cmd in multica python3 zip; do
  [[ "$cmd" == multica && "$DRY_RUN" == "1" ]] && continue
  command -v "$cmd" >/dev/null || { echo "Saknar '$cmd'. Se README.md."; exit 1; }
done
[[ "$DRY_RUN" == "1" ]] && info "DRY_RUN=1: inget skapas på riktigt."
python3 skills/automat/scripts/automat.py oppna >/dev/null && info "automat.py fungerar."

# ---------------------------------------------------------------------------
steg "Väljer runtime (dator + AI-verktyg)"
if [[ -z "${RUNTIME_ID:-}" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    RUNTIME_ID="DRY-RUN-RUNTIME"
  else
    multica runtime list || true
    read -r -p "  Klistra in ID för den runtime agenterna ska använda: " RUNTIME_ID
  fi
fi
[[ -n "$RUNTIME_ID" ]] || { echo "Ingen runtime vald."; exit 1; }
info "Runtime: $RUNTIME_ID"

# ---------------------------------------------------------------------------
steg "Importerar skillen automat"
zipfil="$TMP/automat.zip"
(cd skills/automat && zip -qr "$zipfil" . -x '*/__pycache__/*')
run multica skill import --file "$zipfil" --on-conflict overwrite >/dev/null || varn "Importen misslyckades. Importera mappen skills/automat manuellt i appen."
if [[ "$DRY_RUN" == "1" ]]; then
  SKILL_ID="DRY-automat"
else
  SKILL_ID="$(multica skill list --output json 2>/dev/null | json_id automat || true)"
fi
info "automat → ${SKILL_ID:-(id hittades inte)}"

# ---------------------------------------------------------------------------
steg "Skapar agenter"
# namn | instruktionsfil | beskrivning
AGENTER=(
  "Terminal|agenter/terminal.md|Kortterminal (validera in): kontrollerar kort och PIN och reserverar belopp."
  "Pump|agenter/pump.md|Pump (arbetet): tankar inom reservationen och erbjuder spolarvätska."
  "Kassa|agenter/kassa.md|Kassa (validera ut): slutbelopp, hävning och kvitto. Eskalerar avvikelser."
)
befintliga="$( [[ "$DRY_RUN" == "1" ]] && echo '[]' || multica agent list --output json 2>/dev/null || echo '[]')"
for rad in "${AGENTER[@]}"; do
  IFS='|' read -r namn fil besk <<<"$rad"
  id="$(printf '%s' "$befintliga" | json_id "$namn" || true)"
  if [[ -n "$id" ]]; then
    varn "Agenten '$namn' finns redan ($id). Hoppar över skapandet. Uppdatera instruktionerna i appen vid behov."
  else
    id="$(run multica agent create --name "$namn" --runtime-id "$RUNTIME_ID" \
           --description "$besk" --instructions "$(cat "$fil")" --output json | json_id)"
    info "$namn skapad → $id"
  fi
  if [[ -n "$SKILL_ID" && -n "$id" ]]; then
    run multica agent skills add "$id" --skill-ids "$SKILL_ID" >/dev/null && info "  skill: automat"
  else
    varn "  Koppla skillen 'automat' manuellt i agentens Skills-flik."
  fi
done

# ---------------------------------------------------------------------------
steg "Skapar projektet '$PROJECT_TITLE' (med regelboken i beskrivningen)"
beskrivning="$(cat setup/projekt-beskrivning.md; echo; cat regelbok/REGELBOK.md)"
PROJECT_ID="$(run multica project create --title "$PROJECT_TITLE" --description "$beskrivning" --output json | json_id)"
info "Projekt → $PROJECT_ID"
varn "Koppla mappen till projektet i Desktop-appen:"
info "  Projektet → Resources → Local folders → Choose folder… → $ROOT"
info "  Välj läget 'Edit directly' (in place). Tankningarna delar tillstånd i tillstand/,"
info "  så 'Run in parallel' (worktree) fungerar inte för Bensinautomaten."

# ---------------------------------------------------------------------------
steg "Skapar demotankningar (i Kö/backlog – inget startar ännu)"
if [[ "${SKIP_ISSUES:-0}" == "1" ]]; then
  info "Hoppar över (SKIP_ISSUES=1)."
else
  for f in demo-tankningar/0*.md; do
    titel="$(head -n1 "$f" | sed 's/^# *//')"
    beskr="$TMP/$(basename "$f")"
    # Bara uppgifterna följer med. Raderna efter '---' är facit för den som demonstrerar.
    tail -n +2 "$f" | awk '/^---$/ {exit} {print}' > "$beskr"
    run multica issue create --title "$titel" --description-stdin --project "$PROJECT_ID" \
        --status backlog --output json < "$beskr" | json_id >/dev/null
    info "✓ $titel"
  done
fi

# ---------------------------------------------------------------------------
steg "Klart. Två saker kvar att göra i appen"
info "1. Bygg tavlan (workflow) enligt setup/WORKFLOW.md  (~5 min)"
info "2. Kör demon enligt setup/DEMO-MANUS.md"
info "Inför varje genrep: python3 skills/automat/scripts/automat.py nollstall --ja"
