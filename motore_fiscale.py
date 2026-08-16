
"""Modulo per il calcolo dello stipendio italiano.

Questo modulo contiene la logica per calcolare gli stipendi dei dipendenti a
**Milano**, includendo il calcolo dell'INPS, IRPEF, e imposte
regionali/comunali.
"""
from dataclasses import dataclass


class CalcoloStipendioItaliano:
  """Calcola i componenti dello stipendio lordo di un dipendente milanese.

  Questa classe effettua il calcolo dello stipendio netto a partire dalla RAL
  (Retribuzione Annua Lorda), applicando i contributi INPS, l'imposta IRPEF e
  le imposte regionali/comunali.

  Attributi:
    ral: Retribuzione Annua Lorda in euro.
    INPS_TARIFFA_DIPENDENTI: Aliquota INPS per i dipendenti (9.19%).
  """

  INPS_TARIFFA_DIPENDENTI = 0.0919

  def __init__( self, ral: float ):
      """Inizializza la calcolatrice con la RAL.

      Args:
        ral: Retribuzione Annua Lorda in euro.
      """
      self.ral = ral

  @dataclass
  class RisultatoCalcolo:
    """Contiene il dettaglio del calcolo dello stipendio.
    Se non diversamente specificato, le quantità sono espresse in euro.

    Attributi:
      ral: Retribuzione Annua Lorda.
      mensilita: Numero di mensilità (di solito 13 o 14).
      tassa_inps: Aliquota INPS in percentuale.
      quantita_inps: Importo dei contributi INPS.
      imponibile_irpef: Reddito imponibile per l'IRPEF.
      irpef_lorda: Imposta IRPEF calcolata prima delle detrazioni.
      detrazione_lavoro_dipendente: Detrazione per lavoro dipendente.
      irpef_netta: Imposta IRPEF netta dopo le detrazioni.
      tassa_regionale: Imposta regionale **Lombardia**.
      tassa_comunale: Imposta comunale **Milano**.
      totale_tasse_deduzioni: Somma di tutte le tasse e contributi.
      netto_annuo: Stipendio netto annuale.
      netto_mensile: Stipendio netto mensile.
      aliquota_fiscale_effettiva: Percentuale di tasse effettiva sul lordo.
    """
    ral: float
    mensilita: float
    tassa_inps: float
    quantita_inps: float
    imponibile_irpef: float
    irpef_lorda: float
    detrazione_lavoro_dipendente: float
    irpef_netta: float
    tassa_regionale: float  # Lombardia
    tassa_comunale: float  # Milano
    totale_tasse_deduzioni: float
    netto_annuo: float
    netto_mensile: float
    aliquota_fiscale_effettiva: float

  def calcola_inps( self ) -> float:
    """Calcola l'importo dei contributi INPS.

    Returns:
      Importo dei contributi INPS in euro, arrotondato a 2 decimali.
    """
    return round( self.ral * self.INPS_TARIFFA_DIPENDENTI, 2 )

  def calcola( self, mensilita: int = 13 ) -> RisultatoCalcolo:
    """Calcola lo stipendio netto completo di tutte le tasse e contributi.

    Effettua il calcolo della RAL applicando:
    - Contributi INPS (9.19%)
    - Imposta IRPEF con aliquote progressive (23%, 35%, 43%)
    - Detrazioni per lavoro dipendente
    - Imposta regionale **Lombardia**
    - Imposta comunale **Milano**

    Args:
      mensilita: Numero di mensilità per il calcolo dello stipendio mensile
      (default 13).

    Returns:
      RisultatoCalcolo: Oggetto contenente tutti i dettagli del calcolo.
    """
    if self.ral <= 0:
      return self.RisultatoCalcolo(
        ral=.0, mensilita=mensilita,
        tassa_inps=self.INPS_TARIFFA_DIPENDENTI * 100, quantita_inps=.0,
        imponibile_irpef=.0, lordo_irpef=.0, detrazione_lavoro_dipendente=.0,
        netto_irpef=.0, tassa_regionale=.0, tassa_comunale=.0,
        totale_tasse_deduzioni=.0, netto_annuo=.0, netto_mensile=.0,
        aliquota_fiscale_effettiva=.0
      )

    inps = self.calcola_inps()
    reddito_imponibile = max( .0, self.ral - inps )

    irpef_lorda = self.calcola_irpef_lorda( reddito_imponibile )
    deduzione = self.calcola_detrazione_dipendenti( reddito_imponibile )
    irpef_netta = max( .0, round( irpef_lorda - deduzione ), 2 )

    tassa_regionale = self.calcola_tassa_regionale_lombardia( reddito_imponibile )
    tassa_comunale = self.calcola_tassa_milano( reddito_imponibile )

    totale_deduzioni = round( inps + irpef_lorda + tassa_regionale +
                              tassa_comunale, 2 )

    netto_annuo = round( self.ral - totale_deduzioni, 2 )
    netto_mensile = ( round( netto_annuo / mensilita, 2 ) if mensilita > 0
                      else .0 )

    aliquota_fiscale_effettiva = ( round( ( totale_deduzioni / self.ral )
                                          * 100, 2 ) if self.ral > 0 else .0 )

    return self.RisultatoCalcolo(
      ral=self.ral, mensilita=mensilita,
      tassa_inps=round( self.INPS_TARIFFA_DIPENDENTI * 100, 2),
      quantita_inps=inps, imponibile_irpef=round( reddito_imponibile, 2 ),
      lordo_irpef=irpef_lorda, detrazione_lavoro_dipendente=deduzione,
      netto_irpef=irpef_netta, tassa_regionale=tassa_regionale,
      tassa_comunale=tassa_comunale, totale_tasse_deduzioni=totale_deduzioni,
      netto_annuo=netto_annuo, netto_mensile=netto_mensile,
      aliquota_fiscale_effettiva=aliquota_fiscale_effettiva
    )


  @staticmethod
  def calcola_irpef_lorda( imponibile_irpef: float ) -> float:
    """Calcola l'IRPEF lorda con aliquote progressive secondo la normativa
    italiana.

    Applica le seguenti aliquote:
    - 23% fino a €28.000
    - 35% da €28.001 a €50.000
    - 43% oltre €50.000

    Args:
      imponibile_irpef: Reddito imponibile in euro.

    Returns:
      Importo dell'imposta IRPEF lorda, arrotondato a 2 decimali.
    """
    irpef = .0

    if imponibile_irpef <= 0:
      return irpef

    if imponibile_irpef <= 28000:
      irpef = imponibile_irpef * .23
    elif imponibile_irpef <= 50000:
      # 23% fino a 28'000, 35% sul resto
      irpef = ( 28000 * .23 ) + ( ( imponibile_irpef - 28000 ) * .35 )
    else:
      # 23% fino a 28'000, 35% fino a 50%, 43% sul resto
      irpef = ( ( 28000 * .23 ) + ( 22000 * .35 ) +
                ( ( imponibile_irpef - 50000 ) * .43 ) )

    return round( irpef, 2 )

  @staticmethod
  def calcola_detrazione_dipendenti( imponibile_irpef: float ) -> float:
    """Calcola la detrazione per lavoro dipendente secondo l'Art. 13 del Testo
    Unico delle Imposte sui Redditi.

    La detrazione varia in base al reddito imponibile:
    - €1.955 per redditi fino a €15.000
    - Importo decrescente per redditi tra €15.001 e €28.000
    - Importo decrescente per redditi tra €28.001 e €50.000
    - €0 per redditi oltre €50.000

    Args:
      imponibile_irpef: Reddito imponibile in euro.

    Returns:
      Importo della detrazione in euro, arrotondato a 2 decimali.
    """
    detrazione = 0.0

    if imponibile_irpef <= 0:
      return detrazione

    if imponibile_irpef <= 15000:
      # 1'955 fino a 15'000
      detrazione = 1955.0
    elif imponibile_irpef <= 28000:
      detrazione = ( 1910.0 +
                   ( 1190.0 * ( 28000 - imponibile_irpef ) / 13000 ) )

    elif imponibile_irpef <= 50000:
      detrazione = ( 1910.0 * ( ( 50000 - imponibile_irpef ) / 22000 ) )

    return round( detrazione, 2 )

  @staticmethod
  def calcola_tassa_regionale_lombardia( imponibile_irpef: float ) -> float:
    """Calcola l'imposta regionale della Lombardia con aliquote progressive.

    Applica le seguenti aliquote:
    - 1,23% fino a €15.000
    - 1,58% da €15.001 a €28.000
    - 1,72% da €28.001 a €50.000
    - 1,73% oltre €50.000

    Args:
      imponibile_irpef: Reddito imponibile in euro.

    Returns:
      Importo dell'imposta regionale in euro, arrotondato a 2 decimali.
    """
    tassa = 0.0

    if imponibile_irpef <= 0:
      return tassa

    if imponibile_irpef <= 15000:
      tassa = imponibile_irpef * 0.0123
    elif imponibile_irpef <= 28000:
      tassa = 15000 * 0.0123 + ( ( imponibile_irpef - 15000 ) * 0.0158 )
    elif imponibile_irpef <= 50000:
      tassa = ( 15000 * 0.0123 + 13000 * 0.0158 +
                ( ( imponibile_irpef - 28000 ) * 0.0172 ) )
    else:
      tassa = ( 15000 * 0.0123 + 13000 * 0.0158 + 22000 * 0.0172 +
                ( ( imponibile_irpef - 50000 ) * 0.0173 ) )

    return round( tassa, 2 )

  @staticmethod
  def calcola_tassa_milano( imponibile_irpef: float ) -> float:
    """Calcola l'imposta comunale di Milano all'aliquota dello 0,8%.

    L'imposta si applica solo su redditi superiori a €23.000.

    Args:
      imponibile_irpef: Reddito imponibile in euro.

    Returns:
      Importo dell'imposta comunale in euro, arrotondato a 2 decimali.
    """
    if imponibile_irpef <= 23000:
      return 0.0

    return round( imponibile_irpef * 0.008, 2)
