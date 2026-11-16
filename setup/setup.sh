#!/usr/bin/env bash
# Sätter upp Supportfabriken i din Multica-workspace via Multica CLI.
#
#   ./setup/setup.sh                 kör på riktigt
#   DRY_RUN=1 ./setup/setup.sh       visar bara kommandona
#
# Valfria miljövariabler:
#   RUNTIME_ID=<id>     vilken runtime (dator + AI-verktyg) agenterna ska köra på
#   REPO_URL=<git-url>  koppla repot som projektresurs (annars kopplar du mappen i Desktop-appen)
#   SKIP_CONTEXT=1      skriv inte regelboken till workspace-kontexten
#   SKIP_ISSUES=1       skapa inga demo-uppdrag
#
# Kräver: multica (inloggad via `multica setup`), python3, zip.
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

DRY_RUN="${DRY_RUN:-0}"
PROJECT_TITLE="Supportfabriken"

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
steg "Regelboken → workspace-kontext (gäller alla agenter)"
if [[ "${SKIP_CONTEXT:-0}" == "1" ]]; then
  info "Hoppar över (SKIP_CONTEXT=1)."
else
  varn "Detta ersätter workspace-kontexten i den workspace du är inloggad i."
  svar="j"
  [[ "$DRY_RUN" == "1" ]] || read -r -p "  Fortsätta? [j/N] " svar
  if [[ "$svar" =~ ^[jJyY]$ ]]; then
    if [[ "$DRY_RUN" == "1" ]]; then
      info "\$ multica workspace update --context-stdin < regelbok/REGELBOK.md"
    else
      multica workspace update --context-stdin < regelbok/REGELBOK.md
    fi
  else
    info "Hoppar över. Klistra in regelboken under Settings → workspace context i stället."
  fi
fi

# ---------------------------------------------------------------------------
steg "Importerar skills"
# (macOS levereras med bash 3.2 – därför inga associativa arrayer)
skill_id_satt() { printf -v "SKILL_ID_${1//-/_}" '%s' "$2"; }
skill_id()      { local v="SKILL_ID_${1//-/_}"; printf '%s' "${!v:-}"; }
for dir in skills/*/; do
  namn="$(basename "$dir")"
  zipfil="$TMP/$namn.zip"
  (cd "$dir" && zip -qr "$zipfil" .)
  run multica skill import --file "$zipfil" --on-conflict overwrite >/dev/null || varn "Import av $namn misslyckades. Importera mappen manuellt i appen."
  if [[ "$DRY_RUN" == "1" ]]; then
    skill_id_satt "$namn" "DRY-$namn"
  else
    skill_id_satt "$namn" "$(multica skill list --output json 2>/dev/null | json_id "$namn" || true)"
  fi
  sid="$(skill_id "$namn")"
  info "$namn → ${sid:-(id hittades inte)}"
done

# ---------------------------------------------------------------------------
steg "Skapar agenter"
# namn | instruktionsfil | beskrivning | skills (kommaseparerade)
AGENTER=(
  "Intag|agenter/intag.md|Validera in: grindvakt som godkänner, avvisar eller eskalerar uppdrag.|validera-in"
  "Skribent|agenter/skribent.md|Arbetet: skriver hjälpartiklar utifrån underlag.|skriv-artikel"
  "Granskare|agenter/granskare.md|Validera ut: oberoende granskning, max 2 omtag, sedan eskalering.|granska"
  "Orkestrator|agenter/orkestrator.md|Bryter ner stora uppdrag i sub-issues (fraktalt).|"
)
befintliga="$( [[ "$DRY_RUN" == "1" ]] && echo '[]' || multica agent list --output json 2>/dev/null || echo '[]')"
for rad in "${AGENTER[@]}"; do
  IFS='|' read -r namn fil besk skills <<<"$rad"
  id="$(printf '%s' "$befintliga" | json_id "$namn" || true)"
  if [[ -n "$id" ]]; then
    varn "Agenten '$namn' finns redan ($id). Hoppar över skapandet. Uppdatera instruktionerna i appen vid behov."
  else
    id="$(run multica agent create --name "$namn" --runtime-id "$RUNTIME_ID" \
           --description "$besk" --instructions "$(cat "$fil")" --output json | json_id)"
    info "$namn skapad → $id"
  fi
  if [[ -n "$skills" && -n "$id" ]]; then
    ids=""
    IFS=',' read -ra lista <<<"$skills"
    for s in "${lista[@]}"; do sid="$(skill_id "$s")"; [[ -n "$sid" ]] && ids="${ids:+$ids,}$sid"; done
    if [[ -n "$ids" ]]; then
      run multica agent skills add "$id" --skill-ids "$ids" >/dev/null && info "  skills: $skills"
    else
      varn "  Hittade inga skill-ID:n för $namn. Koppla '$skills' manuellt i agentens Skills-flik."
    fi
  fi
done

# ---------------------------------------------------------------------------
steg "Skapar projektet '$PROJECT_TITLE'"
proj_args=(--title "$PROJECT_TITLE" --description "$(cat setup/projekt-beskrivning.md)" --output json)
[[ -n "${REPO_URL:-}" ]] && proj_args+=(--repo "$REPO_URL")
PROJECT_ID="$(run multica project create "${proj_args[@]}" | json_id)"
info "Projekt → $PROJECT_ID"
if [[ -z "${REPO_URL:-}" ]]; then
  varn "Inget REPO_URL angivet. Koppla den här mappen till projektet i Desktop-appen:"
  info "  Projektet → Resources → lägg till lokal mapp → $ROOT  (välj gärna läget 'worktree')"
fi

# ---------------------------------------------------------------------------
steg "Skapar demo-uppdrag (i Inkorg/backlog – inget startar ännu)"
if [[ "${SKIP_ISSUES:-0}" == "1" ]]; then
  info "Hoppar över (SKIP_ISSUES=1)."
else
  for f in demo-uppdrag/0*.md; do
    titel="$(head -n1 "$f" | sed 's/^# *//')"
    beskr="$TMP/$(basename "$f")"
    tail -n +2 "$f" > "$beskr"
    run multica issue create --title "$titel" --description-stdin --project "$PROJECT_ID" \
        --status backlog --output json < "$beskr" | json_id >/dev/null
    info "✓ $titel"
  done
fi

# ---------------------------------------------------------------------------
steg "Klart. Två saker kvar att göra i appen"
info "1. Bygg tavlan (workflow) enligt setup/WORKFLOW.md  (~5 min)"
info "2. Kör demon enligt setup/DEMO-MANUS.md"
