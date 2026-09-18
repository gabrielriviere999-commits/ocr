# -*- coding: utf-8 -*-

"""
Installation locale de Tesseract.js 5.1.1

Crée :

libs/
└── tesseract/
    ├── tesseract.min.js
    ├── worker.min.js
    └── core/
        ├── tesseract-core.wasm.js
        ├── tesseract-core-simd.wasm.js
        ├── tesseract-core-lstm.wasm.js
        └── tesseract-core-simd-lstm.wasm.js

tessdata/
├── fra.traineddata.gz
├── eng.traineddata.gz
├── spa.traineddata.gz
├── deu.traineddata.gz
├── ita.traineddata.gz
└── por.traineddata.gz

Le script peut être lancé plusieurs fois.
Les fichiers déjà présents ne sont pas retéléchargés.
"""

from __future__ import print_function

import os
import sys
import urllib.request
import urllib.error


# ============================================================
# Configuration
# ============================================================

TESSERACT_VERSION = "5.1.1"
CORE_VERSION = "5.1.1"

# Dossier où se trouve ce script
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TESSERACT_DIR = os.path.join(
    BASE_DIR,
    "libs",
    "tesseract"
)

CORE_DIR = os.path.join(
    TESSERACT_DIR,
    "core"
)

TESSDATA_DIR = os.path.join(
    BASE_DIR,
    "tessdata"
)


# Langues à installer
LANGUAGES = [
    "fra",
    "eng",
    "spa",
    "deu",
    "ita",
    "por"
]


# ============================================================
# URLs
# ============================================================

TESSERACT_BASE_URL = (
    "https://cdn.jsdelivr.net/npm/"
    "tesseract.js@"
    + TESSERACT_VERSION
    + "/dist/"
)

CORE_BASE_URL = (
    "https://cdn.jsdelivr.net/npm/"
    "tesseract.js-core@"
    + CORE_VERSION
    + "/"
)

# Les données linguistiques utilisées par Tesseract.js.
#
# Le nom du fichier est :
#
# langue.traineddata.gz
#
# Exemple :
#
# fra.traineddata.gz
#
# On utilise ici les données officielles Project Naptha.
TESSDATA_BASE_URL = (
    "https://tessdata.projectnaptha.com/4.0.0/"
)


# ============================================================
# Affichage
# ============================================================

def print_line():
    print("-" * 60)


def info(message):
    print("[INFO] " + message)


def ok(message):
    print("[OK]   " + message)


def error(message):
    print("[ERREUR] " + message)


# ============================================================
# Téléchargement
# ============================================================

def download_file(url, destination):

    # Si le fichier existe déjà, on ne le télécharge pas.
    if os.path.isfile(destination):

        ok(
            "Déjà présent : "
            + destination
        )

        return True


    directory = os.path.dirname(destination)

    if not os.path.isdir(directory):

        os.makedirs(directory)


    info(
        "Téléchargement : "
        + url
    )


    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "(Tesseract.js offline installer)"
            }
        )


        response = urllib.request.urlopen(
            request,
            timeout=60
        )


        data = response.read()


        response.close()


        if not data:

            error(
                "Fichier vide : "
                + url
            )

            return False


        output = open(
            destination,
            "wb"
        )


        output.write(data)

        output.close()


        ok(
            "Installé : "
            + destination
        )


        return True


    except urllib.error.HTTPError as e:

        error(
            "HTTP "
            + str(e.code)
            + " : "
            + url
        )

        return False


    except urllib.error.URLError as e:

        error(
            "Erreur réseau : "
            + str(e.reason)
        )

        return False


    except Exception as e:

        error(
            str(e)
        )

        return False


# ============================================================
# Installation de Tesseract.js
# ============================================================

def install_tesseract():

    print_line()

    print(
        "Installation de Tesseract.js "
        + TESSERACT_VERSION
    )

    print_line()


    files = [
        "tesseract.min.js",
        "worker.min.js"
    ]


    success = True


    for filename in files:

        url = (
            TESSERACT_BASE_URL
            + filename
        )


        destination = os.path.join(
            TESSERACT_DIR,
            filename
        )


        if not download_file(
            url,
            destination
        ):

            success = False


    return success


# ============================================================
# Installation du core
# ============================================================

def install_core():

    print_line()

    print(
        "Installation du core "
        + CORE_VERSION
    )

    print_line()


    # IMPORTANT :
    #
    # Tesseract.js v5 demande les 4 fichiers.
    #
    # Il choisit ensuite automatiquement
    # la variante adaptée à l'appareil.
    #
    # Ne pas supprimer les variantes SIMD/LSTM.
    core_files = [
        "tesseract-core.wasm.js",
        "tesseract-core-simd.wasm.js",
        "tesseract-core-lstm.wasm.js",
        "tesseract-core-simd-lstm.wasm.js"
    ]


    success = True


    for filename in core_files:

        url = (
            CORE_BASE_URL
            + filename
        )


        destination = os.path.join(
            CORE_DIR,
            filename
        )


        if not download_file(
            url,
            destination
        ):

            success = False


    return success


# ============================================================
# Installation des langues
# ============================================================

def install_languages():

    print_line()

    print("Installation des langues OCR")

    print_line()


    success = True


    for language in LANGUAGES:

        filename = (
            language
            + ".traineddata.gz"
        )


        url = (
            TESSDATA_BASE_URL
            + filename
        )


        destination = os.path.join(
            TESSDATA_DIR,
            filename
        )


        if not download_file(
            url,
            destination
        ):

            success = False


    return success


# ============================================================
# Vérification finale
# ============================================================

def check_installation():

    print_line()

    print("Vérification")

    print_line()


    required = [
        os.path.join(
            TESSERACT_DIR,
            "tesseract.min.js"
        ),

        os.path.join(
            TESSERACT_DIR,
            "worker.min.js"
        ),

        os.path.join(
            CORE_DIR,
            "tesseract-core.wasm.js"
        ),

        os.path.join(
            CORE_DIR,
            "tesseract-core-simd.wasm.js"
        ),

        os.path.join(
            CORE_DIR,
            "tesseract-core-lstm.wasm.js"
        ),

        os.path.join(
            CORE_DIR,
            "tesseract-core-simd-lstm.wasm.js"
        )
    ]


    for language in LANGUAGES:

        required.append(
            os.path.join(
                TESSDATA_DIR,
                language
                + ".traineddata.gz"
            )
        )


    missing = []


    for filename in required:

        if os.path.isfile(filename):

            ok(
                "Présent : "
                + filename
            )

        else:

            error(
                "MANQUANT : "
                + filename
            )

            missing.append(
                filename
            )


    print_line()


    if missing:

        error(
            str(len(missing))
            + " fichier(s) manquant(s)."
        )

        return False


    ok(
        "Installation complète."
    )

    return True


# ============================================================
# Programme principal
# ============================================================

def main():

    print()

    print_line()

    print(
        "INSTALLATEUR TESSERACT.JS "
        + TESSERACT_VERSION
    )

    print_line()

    print(
        "Dossier : "
        + BASE_DIR
    )

    print()


    # Création des dossiers
    if not os.path.isdir(TESSERACT_DIR):

        os.makedirs(
            TESSERACT_DIR
        )


    if not os.path.isdir(CORE_DIR):

        os.makedirs(
            CORE_DIR
        )


    if not os.path.isdir(TESSDATA_DIR):

        os.makedirs(
            TESSDATA_DIR
        )


    success_tesseract = \
        install_tesseract()


    success_core = \
        install_core()


    success_languages = \
        install_languages()


    print()


    success_check = \
        check_installation()


    print()


    if (
        success_tesseract
        and success_core
        and success_languages
        and success_check
    ):

        print_line()

        print(
            "INSTALLATION TERMINEE"
        )

        print_line()

        print(
            "Vous pouvez maintenant utiliser :"
        )

        print()

        print(
            "libs/tesseract/tesseract.min.js"
        )

        print(
            "libs/tesseract/worker.min.js"
        )

        print(
            "libs/tesseract/core/"
        )

        print(
            "tessdata/"
        )

        print()

        print(
            "L'OCR peut maintenant fonctionner"
        )

        print(
            "sans connexion Internet."
        )

        print_line()

        return 0


    else:

        print_line()

        print(
            "INSTALLATION INCOMPLETE"
        )

        print_line()

        print(
            "Relancez simplement le script."
        )

        print(
            "Les fichiers déjà téléchargés"
        )

        print(
            "ne seront pas retéléchargés."
        )

        print_line()

        return 1


if __name__ == "__main__":

    sys.exit(
        main()
    )
