# LyricsAttribution

### Naive Bayes classifier that categorizes musicians from their respective song lyrics.

#### Setup
You will need to sign up and acquire a ```client_access_token``` through the [Genius API]("https://docs.genius.com/") to run the application.

#### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements:

```bash
pip install -r requirements.txt
```

#### Usage

Copy the ```client_access_token``` to the file named ```access_token.txt```.

Run the scraper and follow the prompts to pull songs from the Genius API providing a second argument ```filename``` as the name of a new ```JSON``` file where the lyrics will be stored.

Note: It is recommended to have at least 100 songs per artist for the sake of training the classifier:

```bash
python ArtistScraper.py filename
```
It may be the case where the scraper needs to be run multiple times due to the API timing out requests. Rerun the above command as necessary and inspect the respective ```filename.json``` for correctness.

Refer to ```songsArtists.json``` for example output.

Run the classifier with a second argument ```filename.json``` specifying the ```JSON``` file as to where the scraped lyrics are stored and a third argument specifying how many times to run the classifier (pass in ```1``` unless you wish to verify the precision of the model).

```bash
python ArtistClassifier.py filename.json 1
```

In the case the scraper does not work, feel free to test the classifier with  ```songsArtists.json``` or ```songsGenres.json```.

#### Support

Open an issue or contact me at <tanay.gummadi@gmail.com>