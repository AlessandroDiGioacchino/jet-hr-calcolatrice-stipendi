
from flask import Flask, render_template, request, jsonify
from motore_fiscale import CalcoloStipendioItaliano

app = Flask( __name__ )


@app.route( '/', methods=[ 'GET', 'POST' ] )
def index():
  risultato = None
  errore = None
  ral_default = '35000'
  mensilita_default = 13

  if request.method == 'POST':
    try:
      ral_input = request.form.get( 'ral', '' ).replace( ',', '.' ).strip()
      mensilita_input = int( request.form.get( 'mensilita', 13 ) )

      if not ral_input:
        errore = 'inserisci una Retribuzione Annua Lorda (RAL) valida.'
      else:
        ral = float( ral_input )
        if ral < 0:
          error = 'La Retribuzione Annua Lorda (RAL) deve essere un valore' \
                  'positivo.'

        else:
          ral_default = ral
          mensilita_default = mensilita_input
          csi = CalcoloStipendioItaliano( ral )
          risultato = csi.calcola( mensilita_input )
    except ValueError:
      errore = 'Formato numerico non valido. Esempi: 35000 o 35000.00'

  return render_template(
    'index.html', risultato=risultato, errore=errore, ral_default=ral_default,
    mensilita_default=mensilita_default
  )


if __name__ == '__main__':
  app.run( debug=True, host='0.0.0.0', port=5000 )
