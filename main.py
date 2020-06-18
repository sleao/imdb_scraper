import requests
from bs4 import BeautifulSoup

TVSHOW_ID = "tt1439629"
BASE_URL = f"https://www.imdb.com/title/{TVSHOW_ID}/episodes?season=" # we just need to add the season to the end of the line.
NUMBER_OF_SEASONS = 6

a = 'Jan. Feb. Mar. Apr. May Jun. Jul. Aug. Sep. Oct. Nov. Dec.'.split(' ')
MONTHS = {y:x for x,y in enumerate(a,1)}

# You should send the episode div and get the data back. It should work for any TV Show, btw.
# The data we want:
# Episode Number, Season, Episode Name, Rating and Air Date. At least for now
def getEpisodeData(episodeDiv):
    episode = {}
    try:
        episode['name'] = episodeDiv.find('a')['title']
        day, month, year = episodeDiv.find('div', {"class": "airdate"}).string.strip().split(' ')
        episode['airdate'] = f'{MONTHS[month]}-{day}-{year}'
        season_n, episode_n = episodeDiv.find('div', {"class": "image"}).div.div.string.split(',')
        episode['season'] = season_n
        episode['episode_number'] = episode_n.strip() 
        episode['rating'] = episodeDiv.find('span', {"class": "ipl-rating-star__rating"}).string
    except:
        pass
    return episode

# We should iterate over the "season div" and get every episode info
# For some reason, using soup.children would return some empty divs which sould return an empty episode
# So I fixed that by making sure to check if an episode is empty before adding it to our list
# I know it ain't pretty, but it works.

def getSeasonData(seasonDiv):
    season = {}
    for x in seasonDiv.children:
        epi = getEpisodeData(x)
        if epi != {}:
            season[epi['episode_number']] = epi
    return season

# Now, I know that Community only has 6 seasons, so I can run a for to get every season data like this:

def getTvShowData():
    # seasonsData = {}
    output = open('data.csv', 'w', encoding='utf-8')
    output.write('season;episode;episode_series;name;airdate;rating\n')

    counter = 1
    for x in range(1, NUMBER_OF_SEASONS+1):
        season_url = BASE_URL + str(x)
        res = requests.get(season_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Our target here is the div with class "list_detail_eplist"
        # Which is this guy right here, now we just pass him to your getSeasonData function, which should return the data we want
        # We can then export it to .csv so others can use.
        
        seasonDiv = soup.find("div",{"class":"list detail eplist"})
        season = getSeasonData(seasonDiv)
    #     seasonsData[f'S{x}'] = season
        for episode in season:
            y = season[episode]
            string = f"{y['season']};{y['episode_number']};{counter};{y['name']};{y['airdate']};{y['rating']}\n"
            output.write(string)
            counter+=1

if __name__ == "__main__":
    getTvShowData()
