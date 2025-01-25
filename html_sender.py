import os
from flask import Flask, render_template

app = Flask(__name__)

DATA_FOLDER = "data"

@app.route("/")
def show():
    # Inicjalizacja pustego słownika na dane
    data = []
    try:
        # Przechodzimy po plikach w folderze "data"
        files = os.listdir(DATA_FOLDER)
        
        # Sprawdzamy, czy folder jest pusty
        if not files:
            data.append("Brak plików w folderze data.")

        # Dodajemy zawartość każdego pliku do słownika
        for file in files:
            filepath = os.path.join(DATA_FOLDER, file)
            with open(filepath, 'r') as f:
                file_contents = f.readlines()
                data.extend([f"{file}: {line.strip()}" for line in file_contents])
        # Debugowanie: wyświetlanie przekazanych danych
        print(f"Dane przekazane do szablonu: {data}")

    except Exception as e:
        # W przypadku błędu, zapisujemy szczegóły błędu w słowniku
        data = [f"Błąd: {str(e)}"]

    # Zwracamy szablon, przekazując dane
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    