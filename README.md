
# Jet HR - Calcolatrice stipendio

Prototipo software per la simulazione e scomposizione della retribuzione lorda
(RAL) in retribuzione netta, sviluppato per il team **Cost-Saving** di Jet HR.

---

## 🎯 Obiettivo del prototipo
Fornire a un dipendente o HR una stima trasparente e deterministica del netto
annuale e mensile partendo dalla RAL, evidenziando ogni voce di trattenuta
fiscale e contributiva.

---

## 📐 Fonti normative e logica di calcolo
Il simulatore implementa il modello fiscale e contributivo per un
**lavoratore dipendente del settore privato a tempo indeterminato** residente a
**Milano**:

1. **Contributi previdenziali (INPS)**:
   - Aliquota IVS a carico del dipendente: **9,19%** applicata direttamente
   sulla RAL.
   - $ \text{Imponibile fiscale IRPEF} = \text{RAL} - \text{INPS} $

2. **IRPEF lorda (scaglioni nazionali - TUIR art. 11)**:
   - Fino a €28'000: **23%**
   - Tra €28'000 e €50'000: **35%**
   - Oltre €50'000: **43%**

3. **Detrazione da lavoro dipendente (TUIR art. 13)**:
   - Fino a €15'000: €1.955
   - Tra €15'000 e €28'000: formula decrescente con base €1'910
   - Tra €28'000 e €50'000: formula decrescente fino ad azzeramento
   - $ \text{IRPEF netta} = \max(0, \text{IRPEF lorda} - \text{detrazioni}) $

4. **Addizionale regionale (Lombardia)**:
   - Aliquote progressive per scaglioni (1,23%, 1,58%, 1,72%, 1,73%).

5. **Addizionale comunale (Milano)**:
   - Aliquota ordinaria: **0,80%**
   - Esenzione totale (no-tax area comunale) per imponibili fino a **€23'000**.

---

## 🚀 Come eseguire il progetto in locale

### Prerequisiti
- Python 3.10+

### Setup Rapido
```bash
# 1. Clona il repository o entra nella cartella
cd jet-hr-calcolatrice-stipendi

# 2. Crea e attiva un virtual environment
python -m venv jet-hr
source jet-hr/bin/activate  # Su Windows: jet-hr\Scripts\activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Avvia l'applicazione Flask
python app.py
```

Apri il browser su `http://localhost:5000`

