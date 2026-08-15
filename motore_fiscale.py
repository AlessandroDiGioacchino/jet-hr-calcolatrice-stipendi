
from dataclasses import dataclass


class CalcoloStipendioItaliano:
  INPS_TARIFFA_DIPENDENTI = 0.0919

  @dataclass
  class RisultatoCalcolo:
    ral: float
    mensilita: float
    tassa_inps: float
    quantita_inps: float
    imponibile_irpef: float
    lordo_irpef: float
    detrazione_lavoro_dipendente: float
    netto_irpef: float
    tassa_regionale: float  # Lombardia
    tassa_comunale: float  # Milano
    totale_tasse_deduzioni: float
    netto_annuo: float
    netto_mensile: float
    aliquota_fiscale_effettiva: float

  def __init__( self, ral: float ):
    self.ral = ral

  def calcola_inps( self ) -> float:
    return round( self.ral * self.INPS_TARIFFA_DIPENDENTI, 2 )

  def calcola( self, mensilita: int = 13 ) -> RisultatoCalcolo:
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

    lordo_irpef = self.calcola_lordo_irpef( reddito_imponibile )
    deduzione = self.calcola_detrazione_dipendenti( reddito_imponibile )
    netto_irpef = max( .0, round( lordo_irpef - deduzione ), 2 )

    tassa_regionale = self.calcola_tassa_regionale_lombardia( reddito_imponibile )
    tassa_comunale = self.calcola_tassa_milano( reddito_imponibile )

    totale_deduzioni = round( inps + lordo_irpef + tassa_regionale +
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
      lordo_irpef=lordo_irpef, detrazione_lavoro_dipendente=deduzione,
      netto_irpef=netto_irpef, tassa_regionale=tassa_regionale,
      tassa_comunale=tassa_comunale, totale_tasse_deduzioni=totale_deduzioni,
      netto_annuo=netto_annuo, netto_mensile=netto_mensile,
      aliquota_fiscale_effettiva=aliquota_fiscale_effettiva
    )


  @staticmethod
  def calcola_lordo_irpef( imponibile_irpef: float ) -> float:
    irpef = .0

    if imponibile_irpef <= 0:
      return irpef

    if imponibile_irpef <= 20000:
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
    # Art. 13 Testo Unico Imposte sui Redditi
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
    if imponibile_irpef <= 23000:
      return 0.0

    return round( imponibile_irpef * 0.008, 2)

