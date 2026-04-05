# When is mosquito season in your city?
### Climate suitability for *Ae. aegypti* and *Ae. albopictus* across 1,421 cities worldwide

> **Tableau Public dashboard** · **ERA5 climate data** · **1991–2020 climate normals**

[![Dashboard](https://img.shields.io/badge/dashboard-Tableau%20Public-orange.svg)](https://public.tableau.com/app/profile/andr.s.lill8311/viz/Whenismosquitoseasoninyourcity/Dashboard)
[![Data](https://img.shields.io/badge/data-ERA5%201991–2020-green)](https://github.com/andreslill/mosquito-season-suitability/blob/main/data/mosquito_suitability.csv)
[![Notebook: Pipeline](https://img.shields.io/badge/notebook-pipeline-blueviolet)](https://github.com/andreslill/mosquito-season-suitability/blob/main/notebooks/mosquito_suitability_pipeline.ipynb)
[![Notebook](https://img.shields.io/badge/notebook-validation-blueviolet)](https://github.com/andreslill/mosquito-season-suitability/blob/main/notebooks/methodology_and_validation.ipynb)

---

In 2025, Europe recorded simultaneous locally acquired dengue, chikungunya, and West Nile virus transmission for the first time (Simonin 2025; ECDC 2025). *Ae. albopictus* has rapidly expanded into temperate regions over recent decades (Bonizzoni et al. 2013), shifting the key question from **where** climate is suitable to **when** seasonal conditions favour mosquito activity. This project models those seasonal suitability windows for *Ae. aegypti* and *Ae. albopictus* across 1,421 cities worldwide using 1991–2020 climate normals.

---

## Overview

Which months are most suitable for mosquito activity, given a city's typical climate? Here we model climate-based suitability for *Ae. aegypti* and *Ae. albopictus* across cities with populations ≥ 500,000.

**Important:** Scores represent *climate suitability only*, not confirmed mosquito presence, disease risk, or actual population abundance. City level elevation is included as contextual information. Elevation differences within cities, microclimates, urban heat islands, and local habitat availability are not captured.

---

## Dashboard Preview

[![Dashboard screenshot showing seasonal suitability for Mexico City, Ae. albopictus](./assets/dashboard_screenshot.png)](https://public.tableau.com/app/profile/andr.s.lill8311/viz/Whenismosquitoseasoninyourcity/Dashboard?publish=yes)
*Screenshot of the Tableau Public dashboard showing Mexico City (Ae. albopictus, Moderate threshold). Select any city and species to explore seasonal suitability, and regional comparisons.*

---

## Species

*Ae. aegypti* and *Ae. albopictus* are the most epidemiologically important mosquito vectors of human arboviral diseases globally (Mordecai et al. 2017). Together, they drive transmission of dengue, Zika, chikungunya, and urban yellow fever. *Ae. aegypti* is predominantly tropical and subtropical. *Ae. albopictus* tolerates cooler conditions and has expanded rapidly into temperate regions, including Europe (Bonizzoni et al. 2013; Simonin 2025), with climate projections suggesting further northward expansion by mid-century (Laporta et al. 2023).

---

## Suitability Model

Suitability is a multiplicative score (0–1):

```
Suitability Score (*Ae. aegypti*)    = TempScore × VPDScore
Suitability Score (*Ae. albopictus*) = TempScore × VPDScore × PhotoFactor*

*PhotoFactor: sigmoid transition centered at the tropics boundary (23.5°, k = 0.5)
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
A sigmoid function (inflection = 23.5°, k = 0.5) weights the Lacour et al. 2015 photoperiod thresholds (11.25 h / 13.5 h) continuously by latitude, producing a 
~5° transition zone around the Tropic of Cancer/Capricorn. PhotoFactor approaches 1.0 near the equator and 0.0 at high latitudes in winter.

**Sensitivity analysis:** A latitudinal sensitivity check confirmed that 294 cities across 28 countries showed photo factor changes > 0.1 under the sigmoid vs. a binary cutoff. The sigmoid implementation was selected on this basis.

In temperate cities, midsummer suitability for *Ae. albopictus* can drop below the season threshold even while temperatures remain high. This reflects two interacting processes: daylength falling below the diapause photoperiod threshold (≈ 13.5 h, Lacour et al. 2015) during late summer, and increased desiccation stress under high VPD. Consequently, in some cities (e.g. Murcia, Athens or Damascus), September can show higher suitability than August, as slightly cooler temperatures nearer the temperature optimum (24.5°C) and recovering humidity together restore conditions above the season threshold.

### Precipitation
Precipitation is shown as contextual information only and does not contribute to the suitability score. The model is based on temperature suitability and VPD, with an additional photoperiod factor for *Ae. albopictus* at higher latitudes. While precipitation can affect breeding-site availability, this is not modelled here. Both *Ae. aegypti* and *Ae. albopictus* are container breeders and urban populations often rely on anthropogenic water sources, such as flowerpots, construction sites, air-conditioning condensate. A non-linear precipitation term could be added in future work to capture both drought stress and larval flushing at high rainfall.

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
| Photoperiod gate | Lacour et al. 2015 | Temperate *Ae. albopictus* populations |

---

## Repository Structure

```
├── analysis/
│   └── photoperiod_sensitivity_check.py      # Sigmoid vs. binary cutoff sensitivity check
├── assets/
│   └── dashboard_screenshot.png  
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

The seasonal suitability windows are broadly consistent with Tegar et al.'s (2026) independent transmission risk model for *Ae. albopictus*-borne chikungunya virus in Europe. Using a temperature-dependent R₀ model derived from PRISMA-guided empirical data on extrinsic incubation period and vector competence, Tegar et al. identify Germany and surrounding central European countries as moderately risky zones with 3–5 months of transmission suitability (May–September). In our model, at the Moderate threshold (0.3), major German cities show season lengths of 3 months, with peak activity falling in July, sitting at the lower end of the 3–5 month range identified by Tegar et al. At the Early warning threshold (0.2), more continental cities such as Berlin, Frankfurt, and Munich extend to 4 months, while at the Strict threshold (0.4), northern cities such as Hamburg contract to 2 months. This threshold sensitivity is expected, as season boundaries are determined by months where climatic suitability falls close to the threshold value.

Notably, Tegar et al. estimate a minimum cut-off temperature for chikungunya virus transmission by *Ae. albopictus* of 13.84°C (95% CI: 10.7–17.4°C), in line with the Tmin of 11.02°C used here for general activity suitability (Doeurk et al. 2025). The lower Tmin reflects that mosquito activity begins at temperatures below those required for virus transmission.

One limitation worth noting: the temperature optimum used here (Topt = 24.5°C) is derived from *female survival* in Doeurk et al. 2025, a single life-history trait. Tegar et al. find an optimum for chikungunya virus transmission of 25.63°C, integrating multiple traits (EIP, vector competence, biting rate, survival) into a full R₀ model. Doeurk et al. also report that blood-feeding rates in *Ae. albopictus* peak at 25°C, slightly above the survival optimum. This suggests the suitability curve used here may be marginally conservative around the peak, as it does not integrate biting rate or transmission competence. A multi-trait Topt closer to 25–26°C could be more appropriate for a transmission-oriented model.

### Validation against Kraemer et al. occurrence records

To test whether the suitability model assigns higher scores to cities with confirmed mosquito presence, suitability metrics were compared against occurrence records from Kraemer et al. (2015), a global compendium of 42,066 *Ae. aegypti* and *Ae. albopictus* records compiled from published literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned if any point record fell within 50 km (point records only; polygon centroids excluded).

Cities near confirmed occurrence records showed systematically higher suitability scores than absence-labelled cities across both species. Season length was the strongest discriminator, with AUC values between 0.72 and 0.83 depending on species and threshold. Results were stable across matching radii from 25 to 150 km, supporting the robustness of the model.

| Species | Metric | Presence median | Absence-labelled median | AUC |
|---|---|---|---|---|
| *Ae. aegypti* | Season length (≥ 0.2) | 12 months | 6 months | **0.834** |
| *Ae. aegypti* | Season length (≥ 0.3) | 12 months | 5 months | 0.827 |
| *Ae. aegypti* | Season length (≥ 0.4) | 12 months | 5 months | 0.815 |
| *Ae. albopictus* | Season length (≥ 0.2) | 12 months | 6 months | **0.743** |
| *Ae. albopictus* | Season length (≥ 0.3) | 12 months | 5 months | 0.730 |
| *Ae. albopictus* | Season length (≥ 0.4) | 12 months | 4 months | 0.747 |

All Mann-Whitney U tests: p < 0.001.

Because Kraemer is a presence-only dataset with uneven geographic coverage, absence-labelled here means no record within 50 km, not confirmed biological absence. Results should be interpreted as discrimination against a noisy background, not as definitive ecological validation.

Full methodology and validation code: `notebooks/methodology_and_validation.ipynb`

### Photoperiod parameter validation

The photoperiod thresholds applied in our model are independently corroborated by the Copernicus Climate Change Service (C3S) dataset on climatic suitability for *Ae. albopictus* in Europe (C3S, 2019). That dataset implements the seasonal activity model of Medlock et al. (2006), which defines egg hatching in spring as requiring photoperiod > 11.25 h and autumn diapause onset when photoperiod drops below 13.5 h, identical to the `PHOTO_LOW` and `PHOTO_HIGH` thresholds used here. Both thresholds originate from Lacour et al. (2015), who established the critical photoperiod (CPP) for diapause induction in a French Mediterranean *Ae. albopictus* population at 13.5 h, and identified 11.25 h as the minimum photoperiod required for spring egg hatching onset. The C3S model is restricted to Europe and based on climate projections (RCP4.5/8.5). Here we extend a comparable approach globally using ERA5 historical climate normals. This treatment of daylength as a seasonal constraint on activity outside the tropics is further supported by Bonizzoni et al. (2013), who document rapid adaptive evolution of critical photoperiod in temperate *Ae. albopictus* populations as a key driver of the species' range expansion into higher latitudes. The same thresholds are applied by Petrić et al. (2021), who implemented the Medlock et al. (2006) framework on ERA5 Land data across Europe and validated against VectorNet presence data.

## Confirmed distribution in Europe

ECDC surveillance ([June 2025](https://www.ecdc.europa.eu/en/publications-data/aedes-aegypti-current-known-distribution-june-2025)) confirms that within the EU, *Ae. aegypti* is established only in Cyprus (Simonin 2025) and on the island of Madeira (Portugal), despite climate suitability extending across parts of mainland southern Europe. Both locations fall below 500,000 population but are included as special interest cities with full suitability scores.

*Ae. albopictus*, by contrast, is established in 369 regions across countries within the EU, including Germany ([ECDC, June 2025](https://www.ecdc.europa.eu/en/publications-data/aedes-albopictus-current-known-distribution-june-2025)), consistent with the broader suitability windows modelled here. The year 2025 marked an 
unprecedented level of arboviral circulation in Europe, with locally acquired 
cases of chikungunya, dengue, and West Nile virus recorded simultaneously 
across the continent (Simonin 2025).

---

## Limitations

- **Climate normals (1991–2020):** Recent warming trends may shift actual suitability windows. Comparing 1991–2020 vs. 2001–2030 normals would show whether recent warming has already shifted season boundaries. The 2001–2030 WMO reference period will not be fully available until around 2031. A shorter period such as 2011–2024 would reduce comparability because of unequal period length, while 2001–2024 overlaps with the current baseline by 20 years and would likely limit detection of a meaningful shift.
- **Interannual variability:** Suitability scores are derived from 30-year monthly climate normals, which represent average conditions and smooth out year-to-year variability. Anomalous years such as an unusually wet August in an otherwise dry city or an exceptionally warm spring are not captured. The model describes structural seasonal suitability, not the outbreak-relevant variability that drives actual population surges in specific years.
- **Spatial resolution:** Suitability is modelled for individual cities, not across continuous space. This makes exposed-population estimates methodologically unsound at the city level. Meaningful exposure analysis would require gridded population data (e.g. GHS-POP) combined with spatially continuous suitability fields, which lies beyond the scope of the current dataset.
- **Urban heat island effect:** ERA5 climate data are provided at ~31 km spatial resolution, representing regional climate conditions rather than urban surface temperatures. Cities are systematically warmer than surrounding areas, typically by 1–3°C depending on city size, density, and season. Suitability scores may therefore underestimate urban seasonal windows in dense urban centres, where the effective thermal environment can sustain mosquito activity beyond what ERA5-derived temperatures suggest.​​​​​​​​​​​​​​​​
- **Suitability scores reflect climate conditions, not confirmed presence.** Thermal and humidity constraints are captured, but biotic factors such as prior establishment, competitive dynamics, or human-mediated introduction are not. Where temperatures approach the lower thermal threshold, occurrence records can diverge substantially from climate predictions, as documented for example in Mexico City (~2,242 m), where *Ae. aegypti* persists despite conditions near its thermal minimum (Doeurk et al. 2025; Lozano-Fuentes et al. 2012; Dávalos-Becerril et al. 2019; Ortega-Morales et al. 2022).
- **Photoperiod (*Ae. albopictus*):** The binary |lat| ≥ 23.5° cutoff has been replaced with a sigmoid transition (inflection = 23.5°, k = 0.5), eliminating edge-case artefacts near the tropics boundary (e.g. São Paulo vs. Rio de Janeiro). The inflection point follows the astronomical tropics boundary. The sigmoid produces a ~5° transition zone. The parameters used are not empirically derived from field data and remain a modelling assumption.
- **Species-specific temperature parameters:** All thermal thresholds (Tmin, Topt, Tmax) for both species were taken from Doeurk et al. (2025), who fitted a quadratic survival model to Cambodian field populations and reported explicit threshold values that can be directly mapped to a triangular suitability curve. This source was preferred over Schmidt et al. (2018), whose Cox regression approach provides relative hazard estimates rather than absolute thermal thresholds. For *Ae. albopictus*, the resulting Topt of 24.5 °C is approximately 3 °C higher than the 21.5 °C reported by Schmidt et al. (2018) from a pooled analysis of globally diverse laboratory strains. This difference may reflect local thermal adaptation in tropical populations as well as differences in study design and strain composition.
- **Presence data:** Suitability scores have been validated against occurrence records from Kraemer et al. (2015), consistent with the methodology described in the Model Validation section. Further comparison against the Mosquito Alert citizen science platform or the VectorMap database (Laporta et al. 2023) could extend coverage, particularly for post-2014 records.
- **City size threshold:** Only cities with populations ≥ 500,000 are included in the main pipeline.
   Funchal (Madeira) and Nicosia (Cyprus), the only two EU territories with confirmed *Ae. aegypti* establishment, are added as special interest cities and appear in the dashboard with full suitability scores.

## Next Iterations
- **Virus-specific transmission modelling:** This work models general climate suitability for mosquito activity. A natural extension would be to incorporate virus-specific temperature–trait relationships (EIP, vector competence) to estimate transmission risk for specific arboviruses, as demonstrated for chikungunya by Tegar et al. (2026) and for dengue/Zika by Mordecai et al. (2017).
- **From suitability to outbreak forecasting:** Integrating confirmed case data would add a predictive layer on top of suitability scores, an approach demonstrated at country level by Sebastianelli et al. (2024) for dengue in Brazil and Peru ([ESA-PhiLab/ESA-UNICEF_DengueForecastProject](https://github.com/ESA-PhiLab/ESA-UNICEF_DengueForecastProject)).

## References

>Bonizzoni M, et al. The invasive mosquito species *Aedes albopictus*: current knowledge and future perspectives. Trends Parasitol. 2013; 29(9):460–468. https://doi.org/10.1016/j.pt.2013.07.003

>Copernicus Climate Change Service (C3S) Climate Data Store (CDS). (2019). Climatic suitability for the presence and seasonal activity of the *Aedes albopictus* mosquito for Europe derived from climate projections. [https://doi.org/10.24381/cds.d08ed09a](https://doi.org/10.24381/cds.d08ed09a)

>Dávalos-Becerril E, et al. Urban and semi-urban mosquitoes of Mexico City: A risk for endemic mosquito-borne disease transmission. PLOS ONE 2019; 14(3): e0212987. https://doi.org/10.1371/journal.pone.0212987

>Doeurk S, et al. Impact of temperature on survival, development and longevity of *Ae. aegypti* and *Ae. albopictus*. Parasites & Vectors 2025; 18:362. https://doi.org/10.1186/s13071-025-06892-y

>Hersbach, H., et al. (2023). ERA5 monthly averaged data on single levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). https://doi.org/10.24381/cds.f17050d7

>Kraemer MUG, et al. The global compendium of *Aedes aegypti* and *Ae. albopictus* occurrence. Sci Data 2015; 2:150035. https://doi.org/10.1038/sdata.2015.35

>Lacour G, et al. Seasonal Synchronization of Diapause Phases in *Aedes albopictus* (Diptera: Culicidae). PLOS ONE 2015; 10(12): e0145311. https://doi.org/10.1371/journal.pone.0145311

>Laporta GZ, et al. Global Distribution of *Aedes aegypti* and *Aedes albopictus* in a Climate Change Scenario of Regional Rivalry. Insects 2023; 14:49. https://doi.org/10.3390/insects14010049

>Lozano-Fuentes S, et al. The dengue virus mosquito vector *Aedes aegypti* at high elevation in México. American Journal of Tropical Medicine and Hygiene 2012; 87(5):902–909. https://doi.org/10.4269/ajtmh.2012.12-0244

>Medlock JM, et al. Analysis of the potential for survival and seasonal activity of *Aedes albopictus* (Diptera: Culicidae) in the United Kingdom. Journal of Vector Ecology 2006; 31(2):292–304. [https://doi.org/10.3376/1081-1710(2006)31[292:AOTPFS]2.0.CO;2]

>Mordecai EA, et al. Detecting the impact of temperature on transmission of Zika, dengue, and chikungunya using mechanistic models. PLOS Neglected Tropical Diseases 2017; 11(4): e0005568. https://doi.org/10.1371/journal.pntd.0005568

>Ortega-Morales AI, et al. Update on the dispersal of *Aedes albopictus* in Mexico: 1988–2021. Frontiers in Tropical Diseases 2022; 2:814205. https://doi.org/10.3389/fitd.2021.814205

>Pareto Software, LLC. 2024. SimpleMaps World Cities Database, Basic v1.901.
https://simplemaps.com/data/world-cities. CC BY 4.0.

>Petrić M, et al. Seasonality and timing of peak abundance of Aedes albopictus in Europe: Implications to public and animal health. Geospatial Health 2021; 16:996. https://doi.org/10.4081/gh.2021.996

>Schmidt CA, et al. Effects of desiccation stress on adult female longevity in *Ae. aegypti* and *Ae. albopictus*. Parasites & Vectors 2018; 11:267. https://doi.org/10.1186/s13071-018-2808-6

>Sebastianelli A, et al. A reproducible ensemble machine learning approach to forecast dengue outbreaks. Scientific Reports 2024; 14:3807. https://doi.org/10.1038/s41598-024-52796-9

>Simonin Y. Europe Faces Multiple Arboviral Threats in 2025. Viruses 2025; 17:1642. https://doi.org/10.3390/v17121642

>Tegar S, et al. Temperature-sensitive incubation, transmissibility and risk of *Aedes albopictus*-borne chikungunya virus in Europe. J. R. Soc. Interface 2026; 23:20250707. https://doi.org/10.1098/rsif.2025.0707


---

## Author

Andrés Lill · 2026  
