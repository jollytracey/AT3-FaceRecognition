import flickrapi
import flickrapi.shorturl
import webbrowser
import json
import urllib
from FlickrDAL import FlickrDAL
import os
import sys
from resizeScript import *



def downloadPhotos():
    f=open('FlickrConnect/apiKey.txt','r')
    """Create your own apiKey.txt file with api key and secret. The format of apiKey.txt should be like this:
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n
    XXXXXXXXXXXXXXXXXX
    """
    api_key=u'{}'.format(f.readline()[:-1])
    api_secret=u'{}'.format(f.readline())
    print('key={} secret={}'.format(api_key,api_secret))
    f.close()
    flickr = flickrapi.FlickrAPI(api_key, api_secret,format='parsed-json',cache=True)
    print('Authenticating...')

    # Only do this if we don't have a valid token already
    if not flickr.token_valid(perms='read'):

        # Get a request token
        flickr.get_request_token(oauth_callback='oob')

        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms='read')
        webbrowser.open_new_tab(authorize_url)

        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = str(input('Verifier code: '))

        # Trade the request token for an access token
        flickr.get_access_token(verifier)
    
    database=[("FlickrPhotos","163308125@N07")]
    #print(database)
    
    existSet=set(os.listdir(os.getcwd()+"/FlickrPhotos"))
    print('Importing images from Flickr....')
    for name,id in database:
        if not os.path.exists(os.getcwd() +'/{}'.format(name)):
            os.mkdir(os.getcwd() +'/{}'.format(name))
        if id==None:
            continue
        photos = flickr.photos.search(user_id=id)
        photolist=photos['photos']['photo']
        #print(photolist)
        for image in photolist:
            #print(flickrapi.shorturl.url(image['id']))
            try:
                link=flickr.photos.getSizes(photo_id=image['id'])['sizes']['size'][-2]['source'] #-1 index to get the original image
                
                filename=link.split('/')[-1]
                if filename in existSet:
                    continue
                path=os.getcwd() +'/{}/{}'.format(name,filename)
                #print(path)
                print(link)
                urllib.request.urlretrieve(link, path)
            except:
                e = sys.exc_info()[0]
                print("Something happened: {}".format(e))
    resizeFlickr()

if __name__=="__main__":
    downloadPhotos()
