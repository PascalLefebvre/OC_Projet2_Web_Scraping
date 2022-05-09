Cursus Openclassrooms "Développeur d'applications - Python" (12 mois)
---------------------------------------------------------------------

Projet 2 : Utilisez les bases de Python pour l'analyse de marché (en utilisant le "web scraping")

	Pour une importante librairie en ligne spécialisée dans les livres d'occasion, développement
	d'une version bêta d'une application de suivi des prix des livres d'occasion sur des sites
	web concurrents. Dans ce projet, suivi des prix des livres chez Books to Scrape, un revendeur
	de livres en ligne. En pratique, dans cette version bêta, le programme n'effectue pas une
	véritable surveillance en temps réel des prix sur la durée. Il s'agit simplement d'une
	application exécutable à la demande visant à récupérer les prix au moment de son exécution.

3ème étape réalisée :

	Extrait du site "books.toscrape.com", par catégorie et pour chaque livre, les informations suivantes ...

	    product_page_url
	    universal_ product_code (upc)
	    title
	    price_including_tax
	    price_excluding_tax
	    number_available
	    product_description
	    category
	    review_rating
	    image_url

	... et les stocke dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.
	
	Lancement du programme :

		$ pip install -r "requirements.txt"
		$ python -m venv env
		$ mkdir data
		$ mkdir categories
		$ python scriptBooksToScrape.py
		
	Résultats : crée dans le répertoire "./data/categories" un fichier "< nom catégorie >.csv"
	
