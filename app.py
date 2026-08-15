
from flask import Flask, render_template, request, jsonify
from motore_fiscale import CalcoloStipendioItaliano

app = Flask( __name__ )


@app.route( '/', methods=[ 'GET', 'POST' ] )
def index():
  risultato = None
  errore = None
  ral_default = "35'000,00"
  mensilita_default = 13

  if request.method == 'POST':
    try:
      ral_input = request.form.get( 'ral', '' ).strip()
      mensilita_input = int( request.form.get( 'mensilita', 13 ) )

      if not ral_input:
        errore = 'inserisci una Retribuzione Annua Lorda (RAL) valida.'
      else:
        ral = valuta2float( ral_input )
        if ral < 0:
          errore = 'La Retribuzione Annua Lorda (RAL) deve essere un valore ' \
                   'positivo.'

        else:
          ral_default = ral
          mensilita_default = mensilita_input
          csi = CalcoloStipendioItaliano( ral )
          risultato = csi.calcola( mensilita_input )
    except ValueError:
      errore = "Formato numerico non valido. Esempi: 35'000,00 o 35000"

  ral_default = filtro_valuta( ral_default )

  return render_template(
    'index.html', risultato=risultato, errore=errore, ral_default=ral_default,
    mensilita_default=mensilita_default
  )

@app.template_filter( 'valuta' )
def filtro_valuta( val: float ) -> str:
  if val is None:
    return '0,00'

  try:
    formattato = f'{float( val ):,.2f}'
    return formattato.replace( ',', "'" ).replace( '.', ',' )
  except ( ValueError, TypeError ):
    return str( val )

def valuta2float( val_str: str ) -> float:
  if not val_str:
    return .0

  pulita = val_str.replace( "'", '' ).replace( ' ', '' ).replace( '.', '' )
  pulita = pulita.replace( ',', '.' )

  return float( pulita )


if __name__ == '__main__':
  app.run( debug=True, host='0.0.0.0', port=5000 )
