# AI-Quantumlight

Flask/OpenAI-Prototyp mit Quantumlight-Oberfläche.

## Bereinigung
- `app.py` ist der einzige Backend-Einstiegspunkt.
- Der zuvor doppelte und beschädigte `main.py` wurde entfernt.
- Secrets werden ausschließlich über Umgebungsvariablen geladen.
- Der dreifache Base64-Transform ist ausdrücklich **keine Verschlüsselung** und wird nur als reversible Darstellung beibehalten.
- `index.html` bleibt als Frontend erhalten.

## Konfiguration
Benötigt: `OPENAI_API_KEY` und `SECRET_KEY`; optional `OPENAI_MODEL` und `PORT`.
