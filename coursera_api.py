
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])

import requests_with_caching, json

#function gets the movie details from the api
def get_movies_from_tastedive(title):
    dic={"q":title, "type":"movies", "limit":5}
    page=requests_with_caching.get("https://tastedive.com/api/similar", params=dic)
    
    page=page.json()
    
    return page

#fn extracts only the similar movies titles
def extract_movie_titles(data ):
    inner=data["Similar"]["Results"]
    
    titles=[movie["Name"] for movie in inner if movie["Type"] == "movie"]
    
    return titles

#this function combines the above two functions
def get_related_titles(movies):
    titles=[]
    
    for movie in movies:
        data=get_movies_from_tastedive(movie)
        data=extract_movie_titles(data)
        
        for item in data:
            if item not in titles:
                titles.append(item)
                
                
    return titles

#this fn extracts the movie's detials like scores and etc.
def get_movie_data(title):
    dic={"t":title, "r":"json"}
    
    page=requests_with_caching.get("http://www.omdbapi.com/", params=dic)
    page=page.json()
    
    return page

#fn just gives the rotten tomatoes scores
def get_movie_rating(data):
    ratings=data["Ratings"]
    
    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            score=rating["Value"]
            
            score=score.replace("%", "")
            
            return int(score)
        
    return 0

#fn returns the sorted list of all the related movies by thei scores
def get_sorted_recommendations(movies_list):
    #final_titles=[]
    rating={}
    
    for movie in movies_list:
        data=get_movies_from_tastedive(movie)
        data=extract_movie_titles(data)
        
        for item in data:
            score=get_movie_data(item)
            score=get_movie_rating(score)
            
            rating[item]=rating.get(item, score)
            #final_list.append(item)
            
    sorted_titles=[item[0] for item in sorted(rating.items(), key= lambda value: (value[1], value[0]), reverse=True)]
    
    return sorted_titles
    

#call get_related_movies("movie_name") function to check the working

#author Deepanshu Narang
#Anti-Social