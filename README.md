# When is mosquito season in your city?
### Climate suitability for *Ae. aegypti* and *Ae. albopictus* across 1,421 cities worldwide

> **Tableau Public dashboard** · **ERA5 climate data** · **1991–2020 climate normals**

[![Dashboard](https://img.shields.io/badge/dashboard-Tableau%20Public-orange.svg)](https://public.tableau.com/app/profile/andr.s.lill8311/viz/Whenismosquitoseasoninyourcity/Dashboard)
[![Data](https://img.shields.io/badge/data-ERA5%20%2B%20Kraemer-green.svg)](./data)
[![Notebook](https://img.shields.io/badge/notebook-validation-blueviolet.svg)](./notebooks/methodology_and_validation.ipynb)

The validation notebook documents the external comparison against Kraemer et al. (2015) occurrence records, including Mann-Whitney U, Cohen's d, and ROC/AUC analysis.

---

## Overview

1,421 cities × 12 months × 2 species = 34,104 monthly suitability estimates.

Which months are most suitable for mosquito activity, given a city's typical climate? Here we model climate-based suitability for *Ae. aegypti* and *Ae. albopictus* across cities with populations ≥ 500,000.

**Important:** Scores represent *climate suitability only*, not confirmed mosquito presence, disease risk, or actual population abundance. City level elevation is included as contextual information. Elevation differences within cities, microclimates, urban heat islands, and local habitat availability are not captured.

---

## Dashboard


🔗 **[Tableau Public Dashboard](https://public.tableau.com/app/profile/andr.s.lill8311/viz/Whenismosquitoseasoninyourcity/Dashboard?publish=yes)**

---

## Views
- **KPI: Season length**: Number of months above the selected suitability threshold
- **KPI: Peak month**: Month with the highest suitability score for the selected city and species
- **Season Bar**: Binary active/inactive months based on a user-defined threshold
- **Suitability Window (Heatmap)**: Continuous suitability score (0–1) across 12 months
- **Season Map**: World map showing which cities are in season for the selected month and species
- **Monthly suitability profile**: Monthly suitability score for the selected city vs. the top 10 cities
  by season length, ties broken by population, at similar latitudes, with a dynamic season threshold reference line
- **Cities same country**: Season length comparison with cities in the same country

**Controls:**
- City dropdown
- Species: *Ae. aegypti* / *Ae. albopictus*
- Season threshold: 0.2 (Early) / 0.3 (Moderate) / 0.4 (Strict)

---

## Species

*Ae. aegypti* and *Ae. albopictus* are the most epidemiologically important mosquito vectors of human arboviral diseases globally (Mordecai et al. 2017). Together, they drive transmission of dengue, Zika, chikungunya (CHIKV), and urban yellow fever across tropical, subtropical, and increasingly temperate regions. *Ae. albopictus*, in particular, has expanded rapidly into Europe over recent decades (Bonizzoni et al. 2013; Simonin 2025), with climate projections suggesting further northward expansion by mid-century (Laporta et al. 2023), making seasonal suitability modelling increasingly relevant for public health planning in previously low-risk regions.

| Species | Notes |
|---|---|
| *Ae. aegypti* | Predominantly tropical/subtropical distribution. |
| *Ae. albopictus* | Broader thermal tolerance; invasive range expansion into temperate regions including Europe. |

---

## Suitability Model

Suitability is a multiplicative score (0–1):

```
Suitability Score (aegypti)    = TempScore × VPDScore
Suitability Score (albopictus) = TempScore × VPDScore × PhotoFactor*

*PhotoFactor applied only outside the tropics (|lat| ≥ 23.5°)
```

### Temperature suitability (TempScore)
Triangular thermal curve: 0 at Tmin/Tmax, 1 at Topt, linear between.

Parameters from Doeurk et al. 2025 (female adult survival):

| Species | Tmin (°C) | Topt (°C) | Tmax (°C) |
|---|---|---|---|
| *Ae. aegypti* | 14.97 | 27.1 | 39.15 |
| *Ae. albopictus* | 11.02 | 24.5 | 38.07 |

### Desiccation stress 
Linearized vapour pressure deficit (VPD) suitability based on Schmidt et al. 2018:
- VPD ≤ 1.0 kPa - score = 1.0
- VPD ≥ 3.0 kPa - score = 0.0
- Linear between

VPD is derived from ERA5 temperature and dewpoint using the Magnus approximation.

### Photoperiod (PhotoFactor • *Ae. albopictus* only)
Applied **only outside the tropics (|lat| ≥ 23.5°)** as a proxy for diapause pressure. In tropical/subtropical latitudes, daylength is less seasonal and diapause is not a dominant driver, so PhotoFactor = 1.0 there.

Outside the tropics (Medlock et al. 2006; Lacour et al. 2015):
- Daylength < 11.25h → 0.0
- 11.25–13.5h → 0.5
- ≥ 13.5h → 1.0

In temperate cities, midsummer suitability for *Ae. albopictus* can drop below the season threshold even while temperatures remain high. This reflects two interacting processes: daylength falling below the diapause photoperiod threshold (≈ 13.5 h, Lacour et al. 2015) and increased desiccation stress under high VPD. Consequently, in some cities (e.g. Murcia, Athens or Damascus), September can show higher suitability than August, as slightly cooler temperatures nearer the temperature optimum (24.5°C) and recovering humidity together restore conditions above the season threshold.

### Precipitation
Precipitation is included as contextual information only and does not contribute to the suitability score. The score is based on temperature suitability and vapour pressure deficit, with an additional photoperiod factor for *Ae. albopictus* outside the tropics.

---

## Data Sources

| Dataset | Source | Period | Notes |
|---|---|---|---|
| Climate normals | ERA5 monthly means [Hersbach et al. 2023](https://doi.org/10.24381/cds.f17050d7) | 1991–2020 | WMO standard period |
| City list | [SimpleMaps World Cities Basic v1.901](https://simplemaps.com/data/world-cities) | 2024 | Filtered: population ≥ 500,000. License: CC BY 4.0 |
| Elevation | [Open-Elevation API](https://open-elevation.com) | — | City-level, metres above sea level |


## Model Parameters

| Parameter | Source | Notes |
|---|---|---|
| Temperature suitability | Doeurk et al. 2025 | Female adult survival curve |
| VPD linearization | Schmidt et al. 2018 | |
| Photoperiod gate | Lacour et al. 2015; Medlock et al. 2006 | Temperate *Ae. albopictus* populations |
---

## Repository Structure

```
├── data/
│   └── mosquito_suitability.csv              # Pre-computed dataset (1,421 cities × 12 months)
│   └── kraemer_occurrences.csv               # Pre-processed from Kraemer et al. (2015); used for validation
├── notebooks/
│   ├── mosquito_suitability_pipeline.ipynb   # ERA5 data pipeline and suitability model
│   └── methodology_and_validation.ipynb      # External validation against Kraemer et al. (2015)
├── .gitattributes
├── requirements.txt
└── README.md
```
---

## Reproducing the Data Pipeline

**Requirements:** Python 3.10+, and the following packages: `numpy`, `pandas`, `xarray`, `tqdm`, plus CDS API access.

The processed output (mosquito_suitability.csv) is included in the repository. Running the full pipeline is only necessary if you want to reproduce or modify the data processing steps.

**ERA5 download:**
1. Register at [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu)
2. Accept the ERA5 license
3. Download `reanalysis-era5-single-levels-monthly-means`, variables: `2m_temperature`, `2m_dewpoint_temperature`, `total_precipitation`, period 1991–2020

**Run:**
1. Open `mosquito_suitability_pipeline.ipynb` in Google Colab
2. Update the file paths in the CONFIG section (Section 2 and Section 4) to match your local environment or Google Drive mount point
3. Run all cells sequentially (note: ERA5 data is returned in Kelvin and m/day. Unit conversion is handled in the notebook)
4. The pipeline generates a Tableau-ready CSV (city × month).

---

## Model Validation

### Seasonal windows: comparison with Tegar et al. 2026

The seasonal suitability windows used are broadly consistent with an independent transmission risk model for *Ae. albopictus*-borne CHIKV in Europe (Tegar et al. 2026, J. R. Soc. Interface). Using a temperature-dependent R₀ model derived from PRISMA-guided empirical data on extrinsic incubation period and vector competence, Tegar et al. identify Germany and surrounding central European countries as moderately risky zones with 3–5 months of transmission suitability (May–September). In our model, at the Moderate threshold (0.3), major German cities show season lengths of 3 months, with peak activity falling in July, sitting at the lower end of the 3–5 month range identified by Tegar et al. At the Early warning threshold (0.2), more continental cities such as Berlin, Frankfurt, and Munich extend to 4 months, while at the Strict threshold (0.4), northern cities such as Hamburg contract to 2 months. This threshold sensitivity is expected, as season boundaries are determined by months where climatic suitability falls close to the threshold value.

Notably, Tegar et al. estimate a minimum cut-off temperature for CHIKV transmission by *Ae. albopictus* of 13.84°C (95% CI: 10.7–17.4°C), broadly consistent with the Tmin of 11.02°C used here for general activity suitability (Doeurk et al. 2025). The lower Tmin in this project reflects that mosquito activity begins at temperatures below those required for virus transmission.

One limitation worth noting: the temperature optimum used here (Topt = 24.5°C) is derived from *female survival* in Doeurk et al. 2025, a single life-history trait. Tegar et al. find an optimum for CHIKV transmission of 25.63°C, integrating multiple traits (EIP, vector competence, biting rate, survival) into a full R₀ model. Doeurk et al. also report that blood-feeding rates in *Ae. albopictus* peak at 25°C, slightly above the survival optimum. This suggests the suitability curve used here may be marginally conservative around the peak, as it does not integrate biting rate or transmission competence. A multi-trait Topt closer to 25–26°C could be more appropriate for a transmission-oriented model.


Bildschirmfoto 2026-03-28 um 22.54.51.png
SIND DIE badges richtig positioniert?

22:55
Ja, die Badges sehen gut positioniert aus — aber es gibt eine kleine semantische Ungereimtheit:

Die Badges sind in zwei Gruppen aufgeteilt: "data" und "notebook" fungieren als Label für die farbigen Badges daneben. Das ist ein gängiges Muster und sieht sauber aus.

Allerdings: "validation" hat kein vorangestelltes Label-Badge. Das fühlt sich etwas inkonsistent an — entweder sollte es ein graues Label davor geben (z.B. "method" · validation), oder "validation" wird in die "notebook"-Gruppe aufgenommen, falls es sich auf das Validierungs-Notebook bezieht.

Aktuelles Schema:

dashboard · Tableau Public
data · ERA5 + Kraemer
notebook · validation
Das wäre die sauberste Lösung — wenn "validation" das Validierungs-Notebook meint, gehört es genau dort hin.

ja genau. validation ist das validierungs notebook

22:55
Dann ist die Struktur genau richtig so:

dashboard · Tableau Public
data · ERA5 + Kraemer
notebook · validation
Passt.


# When is mosquito season in your city? ### Climate suitability for *Ae. aegypti* and *Ae. albopictus* across 1,421 cities worldwide > **Tableau Public dashboard** · **ERA5 climate data** · **1991–2020 climate normals** [![Dashboard](https://img.shields.io/badge/dashboard-Tableau%20Public-orange.s

pasted

und wie war dein rating für das readme nochmal?

22:56
Ich hatte das README noch nicht bewertet — das ist das erste Mal, dass ich den vollständigen Text sehe.

Lass mich kurz drüberschauen und dann ein ehrliches Rating geben.

Rating: 8.5/10

Sehr stark insgesamt. Was gut funktioniert:

Die Modellbeschreibung ist fachlich präzise und gut strukturiert — Tmin/Topt/Tmax-Tabellen, VPD-Linearisierung, PhotoFactor-Logik alles klar dargestellt
Der Validierungsabschnitt ist ungewöhnlich gründlich für ein Portfolio-Projekt und hebt das README deutlich über den Durchschnitt
Limitations-Sektion ist ehrlich und zeigt wissenschaftliche Reife (São Paulo/Rio de Janeiro edge case ist ein gutes Beispiel)
Referenzliste ist vollständig und konsistent formatiert
Zwei Punkte, die ich abziehe:

1. Inkonsistenz im Validation-Abschnitt: Am Ende von "Validation against Kraemer" steht notebooks/validation_kraemer.ipynb, aber im Repository Structure steht methodology_and_validation.ipynb. Einer der beiden Namen stimmt nicht.

2. ECDC-Datum ist zukunftsgerichtet: Die ECDC-Links sind mit "June 2025" datiert, aber das Projekt ist von 2026 — entweder sind das echte Links aus der Zukunft (dann passt es), oder das Datum sollte geprüft werden.

Sonst: publikationsreif.

1: korrigiert: Because Kraemer is a presence only dataset with uneven geographic coverage, this should be interpreted as relative validation rather than proof of true absence. Full methodology and validation code: noteboks/methodology_and_validation.ipynb

ECDC-Datum ist zukunftsgerichtet: Die ECDC-Links sind mit "June 2025" datiert, aber das Projekt ist von 2026 — entweder sind das echte Links aus der Zukunft (dann passt es), oder das Datum sollte geprüft werden??? was meinst du??? die ecdc links sind vom letzten jaht? die maps... und jetzt ist 2026..
22:58
Ja, du hast völlig recht — ich hatte das falsch gedacht. Die ECDC-Karten wurden im Juni 2025 veröffentlicht, das README wurde 2026 geschrieben, und du verlinkst auf diese 2025-Karten. Das ist korrekt und macht Sinn — genau wie man eine Publikation von 2023 zitiert, auch wenn man 2026 schreibt.

Kein Problem dort. Streich den Punkt.

Rating bleibt bei 8.5/10, nur wegen des notebooks/ Tippfehlers im Kraemer-Satz — noteboks/ statt notebooks/.

Because Kraemer is a presence only dataset with uneven geographic coverage, this should be interpreted as relative validation rather than proof of true absence. Full methodology and validation code: notebooks/methodology_and_validation.ipynb

22:58
Perfekt, jetzt stimmt alles. 8.5/10 hält.

und warum nicht höher?

22:59
Gute Frage. Ehrlich gesagt ist der Abzug von 1.5 Punkten etwas pauschal — lass mich konkreter sein.

Ein echter Kritikpunkt bleibt:

"Notebook" Badge vs. README-Text: Der Badge verlinkt auf methodology_and_validation.ipynb, aber im Abschnitt "Views" wird das Notebook nie erwähnt — der Leser muss selbst verstehen, dass das Validierungs-Notebook ein separates Artefakt ist. Ein kurzer Satz unter "Dashboard" oder "Repository Structure" der das Notebook explizit kontextualisiert würde helfen.

Ansonsten — wenn ich ehrlich bin — ist das README für ein Portfolio-Projekt außergewöhnlich gut. Die meisten Data-Analyst-Portfolios haben zwei Sätze und einen Screenshot. Hier gibt es eine vollständige Methodenbeschreibung, externe Validierung mit AUC-Werten, Limitations die echte wissenschaftliche Reflexion zeigen, und eine Referenzliste die einer Publikation würdig wäre.

Ich würde es auf 9/10 korrigieren. Der halbe Punkt Abzug bleibt für kleinere strukturelle Ungereimtheiten — z.B. dass "Midsummer suitability dips" als eigener Unterabschnitt etwas verloren wirkt zwischen den Modellparametern.

"Midsummer suitability dips" als eigener Unterabschnitt etwas verloren wirkt zwischen den Modellparametern

das stört mich auch ... was mache ich da um das zu korrigieren?

23:00
Zwei Optionen:

Option A — Als Hinweis in den Photoperiod-Abschnitt integrieren Den Inhalt direkt unter "Photoperiod (PhotoFactor)" als Absatz anhängen, ohne eigene Überschrift. Es erklärt ja letztlich eine Konsequenz der Photoperiod- + VPD-Interaktion — das gehört inhaltlich genau dort hin.

Option B — In die Limitations verschieben Der Abschnitt beschreibt ein Modellverhalten das man als Artefakt missverstehen könnte (warum ist September besser als August?). Das ist genau der Typ von "hier könnte man stolpern"-Erklärung, die gut in Limitations passt — eventuell unter dem VPD/Photoperiod-Limitation-Punkt.

Ich würde Option A empfehlen. Der Inhalt ist eine direkte Konsequenz der Modelllogik und gehört in die Modelldokumentation, nicht in die Limitations. Einfach die ###-Überschrift entfernen und als Absatz mit einem einleitenden Satz wie "In temperate cities, the interaction between photoperiod and VPD can produce midsummer dips..." direkt unter dem Photoperiod-Abschnitt anfügen.

### Photoperiod (PhotoFactor • *Ae. albopictus* only)
Applied **only outside the tropics (|lat| ≥ 23.5°)** as a proxy for diapause pressure. In tropical/subtropical latitudes, daylength is less seasonal and diapause is not a dominant driver, so PhotoFactor = 1.0 there.
Outside the tropics (Medlock et al. 2006; Lacour et al. 2015):
- Daylength < 11.25h → 0.0
- 11.25–13.5h → 0.5
- ≥ 13.5h → 1.0
In temperate cities, midsummer suitability for *Ae. albopictus* can drop below the season threshold even while temperatures remain high. This reflects two interacting processes: daylength falling below the diapause photoperiod threshold (≈ 13.5 h, Lacour et al. 2015) and increased desiccation stress under high VPD. Consequently, in some cities (e.g. Murcia, Athens or Damascus), September can show higher suitability than August, as slightly cooler temperatures nearer the temperature optimum (24.5°C) and recovering humidity together restore conditions above the season threshold.

kannst du das für mich machen?

Mehr anzeigen
23:00
So würde der zusammengeführte Abschnitt aussehen:

Photoperiod (PhotoFactor · Ae. albopictus only)
Applied only outside the tropics (|lat| ≥ 23.5°) as a proxy for diapause pressure. In tropical/subtropical latitudes, daylength is less seasonal and diapause is not a dominant driver, so PhotoFactor = 1.0 there.

Outside the tropics (Medlock et al. 2006; Lacour et al. 2015):

Daylength < 11.25h → 0.0
11.25–13.5h → 0.5
≥ 13.5h → 1.0
In temperate cities, midsummer suitability for Ae. albopictus can drop below the season threshold even while temperatures remain high. This reflects two interacting processes: daylength falling below the diapause photoperiod threshold (≈ 13.5 h, Lacour et al. 2015) and increased desiccation stress under high VPD. Consequently, in some cities (e.g. Murcia, Athens or Damascus), September can show higher suitability than August, as slightly cooler temperatures nearer the temperature optimum (24.5°C) and recovering humidity together restore conditions above the season threshold.

Nur die ### Midsummer suitability dips-Überschrift entfernt, der Text direkt angehängt. Sonst nichts geändert.

ok und "Notebook" Badge vs. README-Text: Der Badge verlinkt auf methodology_and_validation.ipynb, aber im Abschnitt "Views" wird das Notebook nie erwähnt — der Leser muss selbst verstehen, dass das Validierungs-Notebook ein separates Artefakt ist. Ein kurzer Satz unter "Dashboard" oder "Repository Structure" der das Notebook explizit kontextualisiert würde helfen. was machen wi hier?

23:01
Der Badge sitzt direkt unter dem Titel, aber ohne Kontext wirkt er wie ein Link ins Leere. Ich würde einen kurzen Satz unter "Repository Structure" ergänzen, weil dort die Notebooks ohnehin schon aufgelistet sind — da gehört die Erklärung inhaltlich hin.

Aktuell steht dort:

├── notebooks/
│   ├── mosquito_suitability_pipeline.ipynb   # ERA5 data pipeline and suitability model
│   └── methodology_and_validation.ipynb      # External validation against Kraemer et al. (2015)
Das ist eigentlich schon gut — die Inline-Kommentare erklären beide Notebooks. Was fehlt ist der Rückbezug vom Badge zur Struktur. Ein einziger Satz direkt unter dem Badge-Block würde reichen:

Bild anzeigen
Bild anzeigen
Bild anzeigen

The validation notebook documents the external comparison against Kraemer et al. (2015) occurrence records, including Mann-Whitney U, Cohen's d, and ROC/AUC analysis.

Kurz, faktisch, kein Redundanz mit dem späteren Validation-Abschnitt. Was denkst du?


# When is mosquito season in your city? ### Climate suitability for *Ae. aegypti* and *Ae. albopictus* across 1,421 cities worldwide > **Tableau Public dashboard** · **ERA5 climate data** · **1991–2020 climate normals** [![Dashboard](https://img.shields.io/badge/dashboard-Tableau%20Public-orange.s

pasted

so?

23:03
Ja, perfekt. Der Satz sitzt genau richtig — direkt unter den Badges, kurz, faktisch, kein Overlap mit dem späteren Validation-Abschnitt.

9/10 — ich sehe keine weiteren strukturellen Probleme mehr.

und wie kann ich es weiter verbessern?

23:04
Ehrlich gesagt: auf diesem Niveau wird es schwer, noch etwas Substantielles zu verbessern. Aber hier sind zwei echte Kandidaten:

1. "Dashboard" und "Views" sind zwei getrennte Abschnitte ohne --- dazwischen

"Views" hängt etwas lose unter dem Dashboard-Link. Entweder einen Trenner ergänzen oder "Views" als Unterabschnitt (###) von "Dashboard" machen — das würde die Hierarchie klarer machen.

2. Der Italic-Satz unter dem Badge-Block hat kein konsistentes Styling

Der neue Satz (The validation notebook documents...) ist kursiv, aber sonst gibt es im README keine kursiven Freitext-Sätze — Kursiv ist dort ausschließlich für Artnamen reserviert. Ein normaler Satz ohne Kursiv wäre stilistisch konsistenter.

Das sind aber wirklich Feinheiten. Wenn du das README morgen für die DSDE12-Bewerbung einreichst, ist es in der aktuellen Form stark genug. Ein Reviewer aus dem Data-School-Kontext wird den Validierungsabschnitt und die Limitations-Tiefe deutlich mehr gewichten als diese Formatierungspunkte.

Der Italic-Satz unter dem Badge-Block hat kein konsistentes Styling
der ist doch gar nicht italic?

23:05
Du hast recht, er ist nicht kursiv — ich hatte den Markdown falsch gelesen. Der Satz steht als normaler Fließtext, kein Styling-Problem.

Streich den Punkt. Bleibt nur Punkt 1 als echte Verbesserungsmöglichkeit.


When is mosquito season in your city? Climate suitability for Ae. aegypti and Ae. albopictus across 1,421 cities worldwide Tableau Public dashboard · ERA5 climate data · 1991–2020 climate normals Dashboard Data Notebook The validation notebook documents the external comparison against Kraemer

pasted

verbessert

23:05
Gut. Punkt 1 ist jetzt auch erledigt — "Views" ist als ### unter "Dashboard" eingerückt, die Hierarchie stimmt.

9/10 hält, und ich sehe ehrlich gesagt keine weiteren substanziellen Verbesserungen mehr. Das README ist fertig.

aber was wäre dann9,5 oer 10 von 10

23:06
Ehrlich gesagt: der Unterschied zu 10/10 wäre kein inhaltlicher Mangel, sondern fehlende externe Bestätigung — ein Peer Review, eine Publikation, oder ein öffentliches Zitat. Das README ist methodisch und strukturell auf einem Niveau, das über typische Portfolio-Projekte weit hinausgeht.

9.5/10 wäre es, wenn eine Sache vorhanden wäre:

Eine Abbildung oder Tabelle mit den Validierungsergebnissen direkt im README. Die AUC-Werte (0.72–0.83) stehen als Fließtext — eine kompakte Tabelle mit Species × Threshold × AUC würde den Validierungsabschnitt sofort scanbar machen und die Kernergebnisse für einen Leser sichtbar machen, der nicht das Notebook öffnet.

Das ist der einzige Punkt, bei dem der README-Leser etwas Wesentliches "glauben muss" statt es zu sehen.

ich hatte eine tabele mit den validierungsergebnissen, die hatten wir bewusst rausgenommen... soll sie lieber wieder rein?

23:07
Warum hatten wir sie rausgenommen? Ich erinnere mich nicht mehr an die Begründung.

also Validation against Kraemer et al. occurrence records
To test whether the suitability model assigns higher scores to cities with confirmed mosquito presence, suitability metrics were compared against occurrence records from Kraemer et al. (2015), a global compendium of 42,066 Ae. aegypti and Ae. albopictus records compiled from peer reviewed literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned where at least one point record fell within 50 km.
Cities near confirmed occurrence records showed systematically higher suitability scores than absence-labelled cities across both species. Season length was the strongest discriminator, with AUC values between 0.72 and 0.83 depending on species and threshold. Results were stable across matching radii from 25 to 150 km, supporting the robustness of the model.
Because Kraemer is a presence only dataset with uneven geographic coverage, this should be interpreted as relative validation rather than proof of true absence. Full methodology and validation code: notebooks/methodology_and_validation.ipynb

hiermit 

### External validation against Kraemer et al. occurrence records

Suitability metrics were compared against geo-positioned occurrence records from Kraemer et al. 2015/2017 — a global compendium of 42,066 *Ae. aegypti* and *Ae. albopictus* records compiled from peer-reviewed literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned if any point record fell within 50 km (point records only; polygon centroids excluded).

Cities near confirmed occurrence records showed systematically higher suitability scores. Season length was the strongest discriminator across both species and all thresholds tested:

| Species | Metric | Presence median | Absence-labelled median | AUC |
|---|---|---|---|---|
| *Ae. aegypti* | Season length (≥ 0.2) | 12 months | 6 months | **0.834** |
| *Ae. aegypti* | Season length (≥ 0.3) | 12 months | 5 months | 0.827 |
| *Ae. aegypti* | Season length (≥ 0.4) | 12 months | 5 months | 0.815 |
| *Ae. albopictus* | Season length (≥ 0.2) | 12 months | 6 months | **0.749** |
| *Ae. albopictus* | Season length (≥ 0.3) | 12 months | 5 months | 0.724 |
| *Ae. albopictus* | Season length (≥ 0.4) | 12 months | 4 months | 0.737 |

AUC values are stable across all three thresholds, supporting the robustness of the result. All Mann-Whitney U tests: p < 0.001.

Because Kraemer is a presence-only dataset with uneven geographic coverage, absence-labelled here means no record within 50 km — not confirmed biological absence. Results should be interpreted as discrimination against a noisy background, not as definitive ecological validation.

Full methodology and validation code: `notebooks/validation_kraemer.ipynb`
ersetzten?

oder ein best of both worlds aus beidem machen?

Mehr anzeigen
23:10
Die längere Version ist inhaltlich stärker — die Tabelle macht die Kernergebnisse sofort sichtbar und die Präzisierung "polygon centroids excluded" zeigt methodische Sorgfalt.

Aber es gibt zwei Probleme mit der längeren Version:

Notebook-Pfad ist wieder falsch — notebooks/validation_kraemer.ipynb statt notebooks/methodology_and_validation.ipynb
"Kraemer et al. 2015/2017" — im Rest des README steht konsequent nur "Kraemer et al. (2015)". Was ist die korrekte Zitation?
Wenn diese zwei Punkte geklärt sind, würde ich die längere Version nehmen — mit einer kleinen Kürzung: der erste Satz ("To test whether the suitability model assigns higher scores...") aus der kurzen Version ist prägnanter als der Einstieg der langen Version und könnte den Abschnitt besser eröffnen.

ok mach mir das bitte

23:11
So würde der zusammengeführte Abschnitt aussehen:

Validation against Kraemer et al. occurrence records
To test whether the suitability model assigns higher scores to cities with confirmed mosquito presence, suitability metrics were compared against occurrence records from Kraemer et al. (2015), a global compendium of 42,066 Ae. aegypti and Ae. albopictus records compiled from peer-reviewed literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned if any point record fell within 50 km (point records only; polygon centroids excluded).

Cities near confirmed occurrence records showed systematically higher suitability scores. Season length was the strongest discriminator across both species and all thresholds tested:

Species	Metric	Presence median	Absence-labelled median	AUC
Ae. aegypti	Season length (≥ 0.2)	12 months	6 months	0.834
Ae. aegypti	Season length (≥ 0.3)	12 months	5 months	0.827
Ae. aegypti	Season length (≥ 0.4)	12 months	5 months	0.815
Ae. albopictus	Season length (≥ 0.2)	12 months	6 months	0.749
Ae. albopictus	Season length (≥ 0.3)	12 months	5 months	0.724
Ae. albopictus	Season length (≥ 0.4)	12 months	4 months	0.737
AUC values are stable across all three thresholds, supporting the robustness of the result. All Mann-Whitney U tests: p < 0.001. Results were stable across matching radii from 25 to 150 km.

Because Kraemer is a presence-only dataset with uneven geographic coverage, absence-labelled here means no record within 50 km — not confirmed biological absence. Results should be interpreted as discrimination against a noisy background, not as definitive ecological validation.

Full methodology and validation code: notebooks/methodology_and_validation.ipynb

Überschrift beibehalten wie im Original ("Validation against Kraemer et al. occurrence records"), Einstiegssatz aus der kurzen Version, Tabelle und methodische Präzisierungen aus der langen Version, Notebook-Pfad korrigiert.

als markdown fürs readme

23:11
markdown
### Validation against Kraemer et al. occurrence records

To test whether the suitability model assigns higher scores to cities with confirmed mosquito presence, suitability metrics were compared against occurrence records from Kraemer et al. (2015), a global compendium of 42,066 *Ae. aegypti* and *Ae. albopictus* records compiled from peer-reviewed literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned if any point record fell within 50 km (point records only; polygon centroids excluded).

Cities near confirmed occurrence records showed systematically higher suitability scores. Season length was the strongest discriminator across both species and all thresholds tested:

| Species | Metric | Presence median | Absence-labelled median | AUC |
|---|---|---|---|---|
| *Ae. aegypti* | Season length (≥ 0.2) | 12 months | 6 months | **0.834** |
| *Ae. aegypti* | Season length (≥ 0.3) | 12 months | 5 months | 0.827 |
| *Ae. aegypti* | Season length (≥ 0.4) | 12 months | 5 months | 0.815 |
| *Ae. albopictus* | Season length (≥ 0.2) | 12 months | 6 months | **0.749** |
| *Ae. albopictus* | Season length (≥ 0.3) | 12 months | 5 months | 0.724 |
| *Ae. albopictus* | Season length (≥ 0.4) | 12 months | 4 months | 0.737 |

AUC values are stable across all three thresholds, supporting the robustness of the result. All Mann-Whitney U tests: p < 0.001. Results were stable across matching radii from 25 to 150 km.

Because Kraemer is a presence-only dataset with uneven geographic coverage, absence-labelled here means no record within 50 km — not confirmed biological absence. Results should be interpreted as discrimination against a noisy background, not as definitive ecological validation.

Full methodology and validation code: `notebooks/methodology_and_validation.ipynb`
why is the metric called season length? shouldnt it be season threshold like in the model?

23:13
No — "Season length" is the right name here. It refers to the metric being measured: the number of months above a given threshold. The threshold (≥ 0.2 / ≥ 0.3 / ≥ 0.4) is the parameter used to calculate that length, shown in the same column.

So the table is saying: "for cities labelled as presence, the median number of months above threshold X is 12" — which is the season length. That's correct.

and shouldnt we keep the longer sentence and put te table below? 

Cities near confirmed occurrence records showed systematically higher suitability scores than absence-labelled cities across both species. Season length was the strongest discriminator, with AUC values between 0.72 and 0.83 depending on species and threshold. Results were stable across matching radii from 25 to 150 km, supporting the robustness of the model.

or is the new shorter version better?

23:14
Die längere Version hat einen Vorteil: sie gibt dem Leser die Zusammenfassung bevor die Tabelle kommt — AUC-Range, beide Species, Stabilitätsaussage auf einen Blick. Das ist gutes wissenschaftliches Schreiben: erst die Aussage, dann die Evidenz.

So würde es aussehen:

markdown
Cities near confirmed occurrence records showed systematically higher suitability scores than absence-labelled cities across both species. Season length was the strongest discriminator, with AUC values between 0.72 and 0.83 depending on species and threshold. Results were stable across matching radii from 25 to 150 km, supporting the robustness of the model.

| Species | Metric | Presence median | Absence-labelled median | AUC |
|---|---|---|---|---|
| *Ae. aegypti* | Season length (≥ 0.2) | 12 months | 6 months | **0.834** |
| *Ae. aegypti* | Season length (≥ 0.3) | 12 months | 5 months | 0.827 |
| *Ae. aegypti* | Season length (≥ 0.4) | 12 months | 5 months | 0.815 |
| *Ae. albopictus* | Season length (≥ 0.2) | 12 months | 6 months | **0.749** |
| *Ae. albopictus* | Season length (≥ 0.3) | 12 months | 5 months | 0.724 |
| *Ae. albopictus* | Season length (≥ 0.4) | 12 months | 4 months | 0.737 |

All Mann-Whitney U tests: p < 0.001.
Den Satz "AUC values are stable across all three thresholds..." danach weglassen — er ist redundant, wenn die längere Zusammenfassung davor steht.

ok kannst du mir alles nochmal suaber als markdown geben. ohne gedankenstriche

23:15
markdown
### Validation against Kraemer et al. occurrence records

To test whether the suitability model assigns higher scores to cities with confirmed mosquito presence, suitability metrics were compared against occurrence records from Kraemer et al. (2015), a global compendium of 42,066 *Ae. aegypti* and *Ae. albopictus* records compiled from peer-reviewed literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned if any point record fell within 50 km (point records only; polygon centroids excluded).

Cities near confirmed occurrence records showed systematically higher suitability scores than absence-labelled cities across both species. Season length was the strongest discriminator, with AUC values between 0.72 and 0.83 depending on species and threshold. Results were stable across matching radii from 25 to 150 km, supporting the robustness of the model.

| Species | Metric | Presence median | Absence-labelled median | AUC |
|---|---|---|---|---|
| *Ae. aegypti* | Season length (≥ 0.2) | 12 months | 6 months | **0.834** |
| *Ae. aegypti* | Season length (≥ 0.3) | 12 months | 5 months | 0.827 |
| *Ae. aegypti* | Season length (≥ 0.4) | 12 months | 5 months | 0.815 |
| *Ae. albopictus* | Season length (≥ 0.2) | 12 months | 6 months | **0.749** |
| *Ae. albopictus* | Season length (≥ 0.3) | 12 months | 5 months | 0.724 |
| *Ae. albopictus* | Season length (≥ 0.4) | 12 months | 4 months | 0.737 |

All Mann-Whitney U tests: p < 0.001.

Because Kraemer is a presence-only dataset with uneven geographic coverage, absence-labelled here means no record within 50 km, not confirmed biological absence. Results should be interpreted as discrimination against a noisy background, not as definitive ecological validation.

Full methodology and validation code: `notebooks/methodology_and_validation.ipynb`

### Photoperiod parameter validation

The photoperiod thresholds used here are independently corroborated by the Copernicus Climate Change Service (C3S) dataset on climatic suitability for *Ae. albopictus* in Europe (C3S, 2019). That dataset implements the seasonal activity model of Medlock et al. (2006), which defines egg hatching in spring as requiring photoperiod > 11.25h and autumn diapause onset when photoperiod drops below 13.5h, identical to the `PHOTO_LOW` and `PHOTO_HIGH` thresholds applied here. Both thresholds originate from Lacour et al. (2015), who established the critical photoperiod (CPP) for diapause induction in a French Mediterranean *Ae. albopictus* population at 13.5h, and identified 11.25h as the minimum photoperiod required for spring egg hatching onset. The C3S model is restricted to Europe and based on climate projections (RCP4.5/8.5). Here we extend a comparable approach globally using ERA5 historical climate normals. This treatment of daylength as a seasonal constraint on activity outside the tropics is further supported by Bonizzoni et al. (2013), who document rapid adaptive evolution of critical photoperiod in temperate Ae. albopictus populations as a key driver of the species' range expansion into higher latitudes.

## Confirmed distribution in Europe

ECDC surveillance ([June 2025](https://www.ecdc.europa.eu/en/publications-data/aedes-aegypti-current-known-distribution-june-2025)) confirms that *Ae. aegypti* is established in Cyprus within the EU (Simonin 2025), and in Madeira (outermost region of Portugal), despite climate suitability extending across parts of southern Europe, highlighting the gap between climate suitability and confirmed presence.

*Ae. albopictus*, by contrast, is established in 369 regions across countries within the EU, including Germany ([ECDC, June 2025](https://www.ecdc.europa.eu/en/publications-data/aedes-albopictus-current-known-distribution-june-2025)), consistent with the broader suitability windows modelled here. The year 2025 marked an 
unprecedented level of arboviral circulation in Europe, with locally acquired 
cases of CHIKV, dengue, and West Nile virus recorded simultaneously 
across the continent (Simonin 2025).

---

## Limitations & Next Iterations

- **Climate normals (1991–2020):** Recent warming trends may shift actual suitability windows. A natural next step would be to compare 1991–2020 vs. 2001–2030 normals.
- **City size threshold:** Only cities with populations ≥ 500,000 are included. 
  Smaller cities with known vector presence, such as Madeira (*Ae. aegypti*), 
  are not represented.
- **Spatial resolution:** Suitability is modelled for individual cities, not across continuous space. This makes exposed-population estimates methodologically unsound at the city level. Meaningful exposure analysis would require gridded population data (e.g. GHS-POP) combined with spatially continuous suitability fields, which lies beyond the scope of the current dataset.
- **Suitability scores reflect climate conditions, not confirmed presence.** Thermal and humidity constraints are captured, but biotic factors such as prior establishment, competitive dynamics, or human-mediated introduction are not. Where temperatures approach the lower thermal threshold, occurrence records can diverge substantially from climate predictions, as documented for example in Mexico City (~2,242 m), where *Ae. aegypti* persists despite conditions near its thermal minimum (Doeurk et al. 2025; Lozano-Fuentes et al. 2012; Dávalos-Becerril et al. 2019; Ortega-Morales et al. 2022).
- **Photoperiod (albopictus):** A binary cutoff at |lat| ≥ 23.5° currently separates tropical from temperate photoperiod conditions. The 23.5° boundary follows the standard geographical definition of the tropics (Tropic of Capricorn/Cancer) and serves as a proxy for applying the photoperiod thresholds from Medlock et al. (2006) and Lacour et al. (2015), which were derived from temperate populations. It is not a biologically derived threshold.

  This creates edge cases near the boundary: São Paulo (23.55°S) sits just outside the tropics and triggers a photoperiod-driven reduction in suitability during the southern winter, while Rio de Janeiro (22.9°S), just 0.65° of latitude to the north, is treated as fully tropical with a constant `PhotoFactor` of 1.0. A continuous sigmoid function based on latitude would better represent the biological transition zone and avoid the abrupt transition between tropical and temperate diapause behaviour.
- **Presence data:** Suitability scores have been validated against occurrence records from Kraemer et al. (2015) (see Model Validation above). Further comparison against the Mosquito Alert citizen science platform or the VectorMap database (Laporta et al. 2023) could extend coverage, particularly for post-2014 records.
- **Virus-specific transmission modelling:** This work models general climate suitability for mosquito activity. A natural extension would be to incorporate virus-specific temperature–trait relationships (EIP, vector competence) to estimate transmission risk for specific arboviruses, as demonstrated for CHIKV by Tegar et al. (2026) and for dengue/Zika by Mordecai et al. (2017).
- **From suitability to outbreak forecasting:** A further extension would integrate confirmed case data to build a predictive layer on top of suitability scores, an approach demonstrated at country level by Sebastianelli et al. (2024) for dengue in Brazil and Peru ([ESA-PhiLab/ESA-UNICEF_DengueForecastProject](https://github.com/ESA-PhiLab/ESA-UNICEF_DengueForecastProject)).

## References

>Bonizzoni M, et al. The invasive mosquito species Aedes albopictus: current knowledge and future perspectives. Trends Parasitol. 2013; 29(9):460–468. https://doi.org/10.1016/j.pt.2013.07.003

>Copernicus Climate Change Service (C3S) Climate Data Store (CDS). (2019). Climatic suitability for the presence and seasonal activity of the Aedes albopictus mosquito for Europe derived from climate projections. [https://doi.org/10.24381/cds.d08ed09a](https://doi.org/10.24381/cds.d08ed09a)

>Dávalos-Becerril E, et al. Urban and semi-urban mosquitoes of Mexico City: A risk for endemic mosquito-borne disease transmission. PLOS ONE 2019; 14(3): e0212987. https://doi.org/10.1371/journal.pone.0212987

>Doeurk S, et al. Impact of temperature on survival, development and longevity of Ae. aegypti and Ae. albopictus. Parasites & Vectors 2025; 18:362. https://doi.org/10.1186/s13071-025-06892-y

>Hersbach, H., et al. (2023). ERA5 monthly averaged data on single levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). https://doi.org/10.24381/cds.f17050d7

>Kraemer MUG, et al. The global compendium of Aedes aegypti and Ae. albopictus occurrence. Sci Data 2015; 2:150035. https://doi.org/10.1038/sdata.2015.35

>Lacour G, et al. Seasonal Synchronization of Diapause Phases in Aedes albopictus (Diptera: Culicidae). PLOS ONE 2015; 10(12): e0145311. https://doi.org/10.1371/journal.pone.0145311

>Laporta GZ, et al. Global Distribution of Aedes aegypti and Aedes albopictus in a Climate Change Scenario of Regional Rivalry. Insects 2023; 14:49. https://doi.org/10.3390/insects14010049

>Lozano-Fuentes S, et al. The dengue virus mosquito vector Aedes aegypti at high elevation in México. American Journal of Tropical Medicine and Hygiene 2012; 87(5):902–909. https://doi.org/10.4269/ajtmh.2012.12-0244

>Medlock JM, et al. Analysis of the potential for survival and seasonal activity of Aedes albopictus (Diptera: Culicidae) in the United Kingdom. Journal of Vector Ecology 2006; 31(2):292–304. [https://doi.org/10.3376/1081-1710(2006)31[292:AOTPFS]2.0.CO;2]

>Mordecai EA, et al. Detecting the impact of temperature on transmission of Zika, dengue, and chikungunya using mechanistic models. PLOS Neglected Tropical Diseases 2017; 11(4): e0005568. https://doi.org/10.1371/journal.pntd.0005568

>Ortega-Morales AI, et al. Update on the dispersal of Aedes albopictus in Mexico: 1988–2021. Frontiers in Tropical Diseases 2022; 2:814205. https://doi.org/10.3389/fitd.2021.814205

>Pareto Software, LLC. 2024. SimpleMaps World Cities Database, Basic v1.901.
https://simplemaps.com/data/world-cities. CC BY 4.0.

>Schmidt CA, et al. Effects of desiccation stress on adult female longevity in Ae. aegypti and Ae. albopictus. Parasites & Vectors 2018; 11:267. https://doi.org/10.1186/s13071-018-2808-6

>Sebastianelli A, et al. A reproducible ensemble machine learning approach to forecast dengue outbreaks. Scientific Reports 2024; 14:3807. https://doi.org/10.1038/s41598-024-52796-9

>Simonin Y. Europe Faces Multiple Arboviral Threats in 2025. Viruses 2025; 17:1642. https://doi.org/10.3390/v17121642

>Tegar S, et al. Temperature-sensitive incubation, transmissibility and risk of Aedes albopictus-borne chikungunya virus in Europe. J. R. Soc. Interface 2026; 23:20250707. https://doi.org/10.1098/rsif.2025.0707


---

## Author

Andrés Lill · 2026  

