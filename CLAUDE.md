# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Komunikacija / Communication

**NAPOMENA**: Sva komunikacija sa korisnicima ovog projekta treba da bude na srpskom jeziku koristeći latinično pismo.

## Project Overview

BLBS AI Agent - kompletan AI sistem za analizu i generisanje izveštaja iz BusLogic Ticketing System (BLBS) baze podataka koristeći Claude Sonnet 4 model preko Google Vertex AI platforme.

## Arhitektura Projekta

```
├── web_app.py              # GLAVNA APLIKACIJA - web server
├── requirements.txt        # Python dependencies
├── config/
│   ├── config_manager.py         # MySQL konfiguracija (enkriptovana)
│   ├── vertex_config_manager.py  # Vertex AI konfiguracija (enkriptovana)
│   ├── blbs_config.json         # MySQL podatci (enkriptovano)
│   └── vertex_config.json       # Vertex AI podatci (enkriptovano)
├── database/
│   └── blbs_connector.py         # MySQL konektor za BLBS bazu
├── ai/
│   └── vertex_ai_manager.py      # Vertex AI + Claude Sonnet 4 integracija
├── utils/
│   └── encryption.py            # Enkriptovanje osetljivih podataka
├── templates/                   # HTML templates za web interfejs
│   ├── index.html              # Glavna stranica
│   ├── mysql.html              # MySQL konfiguracija
│   ├── vertex.html             # Vertex AI konfiguracija
│   └── reports.html            # AI izveštaji
└── ui/                         # Legacy desktop GUI (NE KORISTITI)
    └── tabbed_main_window.py   # Tkinter verzija (zastarela)
```

## Pokretanje Aplikacije

**VAŽNO**: Koristiti ISKLJUČIVO web interfejs. Desktop GUI verzije ne rade pouzdano.

```bash
# 1. Aktiviraj virtual environment
.venv\Scripts\activate

# 2. Instaliraj dependencies
pip install -r requirements.txt

# 3. Pokreni web aplikaciju
python web_app.py

# 4. Otvori browser na:
http://localhost:5000
```

## Konfiguracija Sistema

### 1. MySQL (BLBS baza)
- **Host/IP**: BLBS server IP adresa
- **Port**: 3306 (default MySQL)
- **Username/Password**: BLBS MySQL kredencijali
- **Database**: naziv BLBS baze podataka

### 2. Vertex AI (Claude Sonnet 4)
- **Project ID**: Google Cloud project ID
- **Region**: europe-west1 (preporučeno za Claude)
- **Service Account JSON**: putanja do Google Cloud service account fajla
- **Model**: claude-sonnet-4@20250514

### 3. Google Cloud Setup
Service Account mora imati sledeće role:
- `Vertex AI User`
- `AI Platform Admin` (opciono)

## Funkcionalnosti

### AI Izveštaji
Aplikacija koristi Claude Sonnet 4 da analizira SQL rezultate iz BLBS baze i generiše strukturirane izveštaje na srpskom jeziku.

**Tipovi izveštaja:**
- **Osnovni**: Kratak pregled podataka
- **Detaljni**: Duboka analiza sa preporukama  
- **Statistički**: Brojevi, procentuali, metrike
- **Trend analiza**: Vremenski obrasci i prognoze

### Primer workflow-a:
1. Korisnik unosi SQL upit u web interfejs
2. Aplikacija izvršava upit na BLBS bazi
3. Rezultati se šalju Claude Sonnet 4 modelu
4. Claude generiše strukturiran AI izveštaj na srpskom
5. Izveštaj se prikazuje u web interfejsu

## Bezbednost

- Svi osetljivi podaci (lozinke, tokeni) su enkriptovani
- Service Account JSON fajlovi se čuvaju lokalno
- MySQL konekcije koriste TLS enkriptovanje
- Vertex AI koristi OAuth 2.0 autentifikaciju

## Testiranje

```bash
# Test osnovnih komponenti
python test_simple.py

# Test Vertex AI konfiguracije
python test_vertex_simple.py
```

## Debugging

```bash
# Za debug web aplikacije
python debug_app.py

# Za minimalno testiranje GUI-ja
python minimal_test.py
```

## VAŽNE NAPOMENE

1. **NE koristiti desktop GUI verzije** (main.py, main_tabbed.py) - nisu stabilne
2. **Uvek koristiti web_app.py** za production
3. **Vertex AI troškovi** - Claude Sonnet 4 se naplaćuje po token-u
4. **Enkriptovani config fajlovi** se automatski kreiraju pri prvoj konfiguraciji
5. **Browser kompatibilnost**: Chrome, Firefox, Edge (moderne verzije)

## Model Information

- **AI Model**: Claude Sonnet 4 (claude-sonnet-4@20250514)
- **Provider**: Anthropic via Google Vertex AI
- **API**: streamRawPredict (Anthropic Messages format)
- **Language**: Srpski jezik, latinično pismo
- **Max tokens**: 1000 (konfigurabilno)

## Troubleshooting

**Problem sa Vertex AI konekcijom:**
- Proveriti Service Account dozvole
- Proveriti da li je Vertex AI API aktiviran
- Proveriti putanju do JSON fajla

**Problem sa MySQL konekcijom:**
- Proveriti network pristup BLBS serveru
- Proveriti MySQL kredencijale
- Proveriti da li MySQL server prima konekcije

**Web aplikacija se ne otvara:**
- Proveriti da li port 5000 nije zauzet
- Proveriti firewall settings
- Pokrenuti sa `python web_app.py` umesto drugih verzija