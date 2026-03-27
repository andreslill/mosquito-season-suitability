# When is mosquito season in your city?
### Climate suitability for *Ae. aegypti* and *Ae. albopictus* across 1,421 cities worldwide

> **Tableau Public dashboard** · **ERA5 climate data** · **1991–2020 climate normals**

---

## Overview

1,421 cities × 12 months × 2 species = 34,104 monthly suitability estimates.

Which months are most suitable for mosquito activity, given a city's typical climate? Here we model climate-based suitability for *Ae. aegypti* and *Ae. albopictus* across cities with populations ≥ 500,000.

**Important:** Scores represent *climate suitability only*, not confirmed mosquito presence, disease risk, or actual population abundance. City level elevation is included as contextual information. Elevation differences within cities, microclimates, urban heat islands, and local habitat availability are not captured.

---

## Dashboard


🔗 **[Tableau Public Dashboard](https://public.tableau.com/app/profile/andr.s.lill8311/viz/Whenismosquitoseasoninyourcity/Dashboard?publish=yes)**


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

### Photoperiod (PhotoFactor — *Ae. albopictus* only)
Applied **only outside the tropics (|lat| ≥ 23.5°)** as a proxy for diapause pressure. In tropical/subtropical latitudes, daylength is less seasonal and diapause is not a dominant driver, so PhotoFactor = 1.0 there.

Outside the tropics (Lacour et al. 2015; Medlock et al. 2006):
- Daylength < 11.25h → 0.0
- 11.25–13.5h → 0.5
- ≥ 13.5h → 1.0

### Midsummer suitability dips (*Ae. albopictus*)

In temperate cities, midsummer suitability for *Ae. albopictus* can drop below the season threshold even while temperatures remain high. This reflects two interacting processes: daylength falling below the diapause photoperiod threshold (≈ 13.5 h, Lacour et al. 2015) and increased desiccation stress under high VPD. Consequently, in some cities (e.g. Murcia, Athens or Damascus), September can show higher suitability than August, as slightly cooler temperatures nearer the temperature optimum (24.5°C) and recovering humidity together restore conditions above the season threshold.

### Precipitation
Precipitation is included as contextual information only and does not contribute to the suitability score. The score is based on temperature suitability and vapour pressure deficit, with an additional photoperiod factor for *Ae. albopictus* outside the tropics.

---

## Data Sources

| Dataset | Source | Notes |
|---|---|---|
| Climate normals | ERA5 monthly means, [Copernicus CDS](https://cds.climate.copernicus.eu) | 1991–2020 (WMO standard period) |
| City list | [SimpleMaps World Cities Basic v1.901](https://simplemaps.com/data/world-cities) | Filtered: population ≥ 500,000. License: CC BY 4.0 |
| Elevation | [Open-Elevation API](https://open-elevation.com) | City-level, metres above sea level |

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
│   └── mosquito_suitability.csv          # Pre-computed dataset (1,421 cities × 12 months)
│   └── kraemer_occurrences.csv           # Pre-processed from Kraemer et al. (2015); used for validation
├── notebooks/
│   ├── mosquito_suitability_pipeline.ipynb   # ERA5 data pipeline and suitability model
│   └── methodology_and_validation.ipynb           # External validation against Kraemer et al. (2015)
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

### Validation against Kraemer et al. occurrence records

To test whether the suitability model assigns higher scores to cities with confirmed mosquito presence, suitability metrics were compared against occurrence records from Kraemer et al. (2015), a global compendium of 42,066 *Ae. aegypti* and *Ae. albopictus* records compiled from peer reviewed literature and national entomological surveys between 1958 and 2014. For each city, a presence label was assigned where at least one point record fell within 50 km.

Cities near confirmed occurrence records showed systematically higher suitability scores than absence-labelled cities across both species. Season length was the strongest discriminator, with AUC values between 0.72 and 0.83 depending on species and threshold. Results were stable across matching radii from 25 to 150 km, supporting the robustness of the model.

Because Kraemer is a presence only dataset with uneven geographic coverage, this should be interpreted as relative validation rather than proof of true absence. Full methodology and validation code: `notebooks/validation_kreamer.ipynb`

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
- **Photoperiod (albopictus):** A binary cutoff at |lat| ≥ 23.5° currently separates tropical from temperate photoperiod conditions. The 23.5° boundary follows the standard geographical definition of the tropics (Tropic of Capricorn/Cancer) and serves as a practical proxy for applying the photoperiod thresholds from Medlock et al. (2006) and Lacour et al. (2015), which were derived from temperate populations. It is not a biologically derived threshold.

  This creates edge cases near the boundary: São Paulo (23.55°S) sits just outside the tropics and triggers the photoperiod penalty during the southern winter, while Rio de Janeiro (22.9°S), just 0.65° of latitude to the north, is treated as fully tropical with a constant `PhotoFactor` of 1.0. A continuous sigmoid function based on latitude would better represent the biological transition zone and smooth the step-change between tropical and temperate diapause behaviour.
- **Presence data:** Suitability scores have been validated against geo-positioned occurrence records from Kraemer et al. (2015) (see Model Validation above). Further comparison against the Mosquito Alert citizen science platform or the VectorMap database (Laporta et al. 2023) could extend coverage, particularly for post-2014 records.
- **Virus-specific transmission modelling:** This work models general climate suitability for mosquito activity. A natural extension would be to incorporate virus-specific temperature–trait relationships (EIP, vector competence) to estimate transmission risk for specific arboviruses, as demonstrated for CHIKV by Tegar et al. (2026) and for dengue/Zika by Mordecai et al. (2017).
- **From suitability to outbreak forecasting:** A further extension would integrate confirmed case data to build a predictive layer on top of suitability scores, an approach demonstrated at country level by Sebastianelli et al. (2024) for dengue in Brazil and Peru ([ESA-PhiLab/ESA-UNICEF_DengueForecastProject](https://github.com/ESA-PhiLab/ESA-UNICEF_DengueForecastProject)).

## References

>Bonizzoni M, et al. The invasive mosquito species Aedes albopictus: current knowledge and future perspectives. Trends Parasitol. 2013; 29(9):460–468. https://doi.org/10.1016/j.pt.2013.07.003

>Copernicus Climate Change Service, Climate Data Store, (2019): Climatic suitability for the presence and seasonal activity of the Aedes albopictus mosquito for Europe derived from climate projections. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). https://doi.org/10.24381/cds.d08ed09a

>Dávalos-Becerril E, et al. Urban and semi-urban mosquitoes of Mexico City: A risk for endemic mosquito-borne disease transmission. PLOS ONE 2019; 14(3): e0212987. https://doi.org/10.1371/journal.pone.0212987

>Doeurk S, et al. Impact of temperature on survival, development and longevity of Ae. aegypti and Ae. albopictus. Parasites & Vectors 2025; 18:362. https://doi.org/10.1186/s13071-025-06892-y

>Kraemer MUG, et al. The global compendium of Aedes aegypti and Ae. albopictus occurrence. Sci Data 2015; 2:150035. https://doi.org/10.1038/sdata.2015.35

>Lacour G, et al. Seasonal Synchronization of Diapause Phases in Aedes albopictus (Diptera: Culicidae). PLOS ONE 2015; 10(12): e0145311. https://doi.org/10.1371/journal.pone.0145311

>Laporta GZ, et al. Global Distribution of Aedes aegypti and Aedes albopictus in a Climate Change Scenario of Regional Rivalry. Insects 2023; 14:49. https://doi.org/10.3390/insects14010049

>Lozano-Fuentes S, et al. The dengue virus mosquito vector Aedes aegypti at high elevation in México. American Journal of Tropical Medicine and Hygiene 2012; 87(5):902–909. https://doi.org/10.4269/ajtmh.2012.12-0244

>Medlock JM, et al. Analysis of the potential for survival and seasonal activity of Aedes albopictus (Diptera: Culicidae) in the United Kingdom. Journal of Vector Ecology 2006; 31(2):292–304. https://doi.org/10.3376/1081-1710(2006)31[292:AOTPFS]2.0.CO;2

>Mordecai EA, et al. Detecting the impact of temperature on transmission of Zika, dengue, and chikungunya using mechanistic models. PLOS Neglected Tropical Diseases 2017; 11(4): e0005568. https://doi.org/10.1371/journal.pntd.0005568

>Ortega-Morales AI, et al. Update on the dispersal of Aedes albopictus in Mexico: 1988–2021. Frontiers in Tropical Diseases 2022; 2:814205. https://doi.org/10.3389/fitd.2021.814205

>Schmidt CA, et al. Effects of desiccation stress on adult female longevity in Ae. aegypti and Ae. albopictus. Parasites & Vectors 2018; 11:267. https://doi.org/10.1186/s13071-018-2808-6

>Sebastianelli A, et al. A reproducible ensemble machine learning approach to forecast dengue outbreaks. Scientific Reports 2024; 14:3807. https://doi.org/10.1038/s41598-024-52796-9

>Simonin Y. Europe Faces Multiple Arboviral Threats in 2025. Viruses 2025; 17:1642. https://doi.org/10.3390/v17121642

>Tegar S, et al. Temperature-sensitive incubation, transmissibility and risk of Aedes albopictus-borne chikungunya virus in Europe. J. R. Soc. Interface 2026; 23:20250707. https://doi.org/10.1098/rsif.2025.0707


---

## Author

Andrés Lill · 2026  

