# Openclassrooms - Projet 2 : Utilisez les bases de Python pour l'analyse de marché (en utilisant le "web scraping")

	Pour une importante librairie en ligne spécialisée dans les livres d'occasion, développement
	d'une version bêta d'une application de suivi des prix des livres d'occasion sur des sites
	web concurrents. Dans ce projet, suivi des prix des livres chez Books to Scrape, un revendeur
	de livres en ligne. En pratique, dans cette version bêta, le programme n'effectue pas une
	véritable surveillance en temps réel des prix sur la durée. Il s'agit simplement d'une
	application exécutable à la demande visant à récupérer les prix au moment de son exécution.


## Informations générales

* Extrait du site "books.toscrape.com", par catégorie et pour chaque livre, les informations suivantes ...

	product_page_url,
	universal_product_code (upc),
	title,
	price_including_tax,
	price_excluding_tax,
	number_available,
	product_description,
	category,
	review_rating,
	image_url

... et les stocke dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.

* Pour chaque livre, télécharge le fichier image correspondant et le stocke dans un répertoire local
	

## Installation et exécution

	$ mkdir data data/categories data/images
	$ python -m venv env
	$ source env/bin/activate
	$ pip install -r "requirements.txt"
	$ python scriptBooksToScrape.py
		

### Données générées

* Crée dans le répertoire "./data/categories" un fichier "<nom catégorie>.csv" par catégorie

* Télécharge dans le répertoire "./data/images" un fichier "<universal product code>.jpg" pour chaque livre
	
