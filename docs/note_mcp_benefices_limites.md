# Note MCP : système d'analyse vidéo board-to-FEN

## Bénéfices et limites

### Périmètre du système

Le système étudié est un serveur MCP dédié à l'analyse vidéo : stockage de vidéos pédagogiques d'échecs, extraction de frames, détection d'échiquier et conversion en notation FEN via un modèle de vision, puis recherche d'une position exacte dans le catalogue avec retour du lien et du timestamp précis. Ce système est distinct de l'agent ReAct existant (Lichess, Stockfish, RAG, YouTube), qui reste hors de ce périmètre.

### Bénéfices attendus

**Une base de connaissance ancrée dans la pratique réelle.** Contrairement au RAG actuel, qui s'appuie sur des articles théoriques, ce système capture des positions issues de vraies parties commentées, avec la logique du formateur expliquant pourquoi telle variante est choisie plutôt qu'une autre. Ce niveau d'explication contextuelle dépasse ce que les statistiques Lichess (taux de victoire, fréquence) peuvent fournir.

**Une progression pédagogique pas à pas.** Les tutoriels vidéo suivent généralement une logique d'enseignement (introduction de l'ouverture, variantes principales, pièges courants), ce qui correspond bien à la cible FFE : des jeunes joueurs en phase d'apprentissage, plutôt qu'une base de données brute de coups.

**Une couverture qualitative forte sur les ouvertures populaires.** Les ouvertures les plus enseignées (Italienne, Ruy Lopez, Sicilienne) bénéficient d'un volume important de contenu pédagogique de qualité, ce qui rend le système particulièrement solide sur le socle dont un jeune joueur a le plus besoin.

**Une fonctionnalité différenciante pour la FFE.** Pouvoir renvoyer la vidéo et le moment exact où un maître explique une position donnée est un service que ni Lichess ni un RAG textuel ne proposent.

### Limites techniques

**Couverture partielle par vidéo.** Une vidéo donnée ne couvre généralement qu'une ligne de jeu parmi les variantes possibles d'une ouverture. Le système hérite du biais de couverture du formateur, sans offrir de vue exhaustive de l'arbre d'ouverture.

**Déséquilibre de couverture entre ouvertures.** Les ouvertures populaires, accessibles ou à la mode disposent d'un volume de contenu disponible largement supérieur aux ouvertures techniques ou peu enseignées. Le catalogue final reflète ce biais d'offre vidéo plutôt qu'une couverture théorique équilibrée.

**Dépendance critique au type d'échiquier source.** Ce point structure directement l'architecture technique, avec deux familles de cas appelant des solutions disjointes :
- *Échiquier numérique* (capture d'écran chess.com, Lichess) : détection quasi déterministe, des outils comme chessimg2pos exploitent la régularité du rendu numérique (assets graphiques fixes, absence de perspective, éclairage constant).
- *Échiquier physique filmé en 3D* : nécessite des modèles de vision plus lourds (chesscog, fenify-3D), avec des contraintes fortes sur l'angle de prise de vue, le type de pièces, les ombres portées des pièces du fond masquant celles de devant, et la qualité variable de l'éclairage en vidéo amateur.

Le choix du périmètre source, contenu numérique uniquement ou extension au contenu physique filmé, doit être tranché en amont : il change le budget de développement d'un ordre de grandeur.

**Volume de données nécessaire pour une couverture utile.** Une couverture pertinente du catalogue exige l'ingestion d'un nombre conséquent de vidéos par ouverture, avec un travail de dédoublonnage pour éviter d'indexer plusieurs vidéos couvrant exactement la même ligne sans valeur ajoutée différenciante.

**Robustesse de la détection.** Un taux d'erreur sur la conversion frame vers FEN (pièce mal détectée, mauvaise orientation de l'échiquier) pollue le catalogue avec de fausses correspondances de position, ce qui dégrade la confiance dans l'ensemble du système si le taux d'erreur n'est pas maîtrisé.

### Limites business

**Coût de traitement concentré en amont, pas en continu.** L'architecture pipeline limite les coûts récurrents : téléchargement de la vidéo, extraction des frames, détection et conversion FEN, écriture d'un fichier d'index léger associant chaque timestamp à une position (sur le modèle d'un fichier de sous-titres), puis suppression de la vidéo brute. Le stockage long terme ne porte que sur l'index, la vidéo restant streamée depuis YouTube via lien direct au timestamp.

**Coût de mise à jour du catalogue.** Chaque nouvelle vidéo à ingérer répète le pipeline complet (téléchargement, extraction, détection). C'est un coût récurrent à chaque enrichissement du catalogue, non un coût ponctuel.

**Dépendance à la disponibilité des vidéos sources.** Le système pointe vers des vidéos YouTube tierces. Une vidéo supprimée ou rendue privée invalide le lien retourné par le système, sans action corrective possible côté FFE.

**Risque d'adoption lié à la qualité perçue.** Une détection FEN comportant des erreurs visibles par l'utilisateur dégrade rapidement la confiance dans l'outil, plus rapidement qu'avec un outil purement textuel où l'erreur est moins immédiatement vérifiable par l'utilisateur final.

### Évolution possible : format de sortie augmenté par la transcription

L'index de sortie envisagé initialement associe chaque timestamp à une position FEN, sur le modèle d'un fichier de sous-titres. Une limite de ce format simple apparaît sur les vidéos où le formateur explore une variante secondaire puis revient à sa ligne principale : deux timestamps peuvent partager la même position FEN tout en ayant un rôle pédagogique différent, sans que l'index seul permette de les distinguer.

L'ajout de la transcription au format de sortie répond à ce point. Le triplet devient timestamp, position FEN, texte transcrit. YouTube expose les sous-titres automatiques via l'API Data v3 (endpoint captions), déjà mobilisée par ailleurs dans le projet pour la recherche de vidéos. La récupération de la transcription ne nécessite donc pas de pipeline de transcription audio dédié (type Whisper), elle s'obtient directement depuis l'API au même titre que les métadonnées de la vidéo.

Ce format augmenté ouvre une capacité de recherche hybride : non seulement retrouver une position FEN précise, mais aussi retrouver le moment où un concept donné est évoqué à l'oral, en recherchant sur le texte transcrit. Cette extension rapproche le sous-système d'un mini-RAG vidéo, et reste positionnée comme une évolution du format plutôt qu'un prérequis du MVP de l'étude.