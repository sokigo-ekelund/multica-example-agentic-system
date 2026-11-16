# Manuell setup (utan CLI, ca 15 min)

Använd den här guiden om du bara har Desktop-appen. Allt görs i Multicas gränssnitt.

## 1. Workspace och regelbok
1. Skapa gärna en ny workspace, till exempel *Fabrik-workshop*.
2. *Settings → workspace context:* klistra in hela innehållet i [`regelbok/REGELBOK.md`](../regelbok/REGELBOK.md).

## 2. Runtime
*Runtimes:* kontrollera att din dator och ditt AI-verktyg syns som **Online**. Om inte: starta verktyget
(till exempel `claude`) en gång i terminalen, logga in och starta om Multica.

## 3. Skills (3 st)
*Skills → Import from local:* välj mappen för varje skill:
- `skills/validera-in`
- `skills/skriv-artikel`
- `skills/granska`

## 4. Agenter (4 st)
*Agents → New agent.* Välj din runtime och klistra in innehållet i instruktionsfilen under **Instructions**.

| Namn (exakt) | Instruktioner | Skill |
|---|---|---|
| Intag | `agenter/intag.md` | validera-in |
| Skribent | `agenter/skribent.md` | skriv-artikel |
| Granskare | `agenter/granskare.md` | granska |
| Orkestrator | `agenter/orkestrator.md` | – |

Namnen måste stämma exakt. Agenterna använder dem för att lämna över till varandra.

> **Tips:** agenterna kan köra på *olika* AI-verktyg. Låt till exempel Skribent köra på Claude Code
> och Granskare på Codex. Då får du en granskare som verkligen är oberoende.

## 5. Projekt
*Projects → New project:* döp det till **Supportfabriken** och klistra in
[`setup/projekt-beskrivning.md`](projekt-beskrivning.md) som beskrivning. Koppla sedan den här mappen
under *Resources* (se [WORKFLOW.md](WORKFLOW.md), punkt 5).

## 6. Demo-uppdrag
Skapa ett issue per fil i `demo-uppdrag/` (01–04). Använd första raden som titel och resten som beskrivning.
Lägg dem i **Inkorg/Backlog**, så att inget startar förrän du flyttar dem.

## 7. Tavlan
Fortsätt med [WORKFLOW.md](WORKFLOW.md).
