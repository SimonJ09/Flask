# Nombre de travailleurs (processus) pour gérer les requêtes
workers = 4

# Adresse IP et port d'écoute pour le serveur Gunicorn
bind = "0.0.0.0:8000"

# Chemin du fichier d'accès au journal (access log)
accesslog = "access.log"

# Chemin du fichier de journal des erreurs (error log)
errorlog = "error.log"

# Mode de débogage (True pour activer le débogage)
debug = True

# Désactiver la capture de la sortie standard (stdout)
capture_output = True
