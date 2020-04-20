#Credit to News API for API Key 
import requests
class news_object:
    url = ''
    response = ''
    data = ''
    def __init__(self):
        
        try:
            self.url = ('http://newsapi.org/v2/top-headlines?'
                'country=us&'
                'apiKey=02f90cf35f2b4176a559db2847011096')
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            self.data = self.response.json()

        except requests.exceptions.HTTPError as err:
            print(err)
            return None

    #Return the total number of articles in JSON
    def num_of_articles(self):
        return self.data['totalResults']

    #Collect array of titles
    def titles(self):
        titles = []
        for a in self.data['articles']:
            titles.append(a['title'])
        return titles

    #Collect array of content
    def content(self):
        content = []
        for a in self.data['articles']:
            content.append(a['content'])
        return content

    #Collect array of sources
    def source(self):
        sources = []
        for a in self.data['articles']:
            sources.append(a['source']['name'])
        return sources

    #Collect array of urls
    def urls(self):
        url = []
        for a in self.data['articles']:
            url.append(a['url'])
        return url

    #Collect tuple of title, content, and url at entry i
    def display_index_data(self, index):
        if index > self.data['totalResults']:
            print("Index is greater than the number of articles")
            return None
        else:
            title = self.data['articles'][index]['title']
            content = self.data['articles'][index]['content']
            url = self.data['articles'][index]['url']
            return (title, content, url)

    #Collect array of tuples of title, content, and url of all entries
    def display_all_data(self):
        pairs = []
        for pair in self.data['articles']:
            newTuple = (pair['title'], pair['description'], pair['url'])
            pairs.append(newTuple)
        return pairs

def main():
    print("Begin testing")


if __name__ =='__main__':
    main()