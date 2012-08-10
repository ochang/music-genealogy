# BEGIN IMPORTS
import os
import sys
import codecs

from bs4 import BeautifulSoup
# END IMPORTS


# BEGIN DEFINITIONS
def get_string(tag):
    """ gets first string for hyperlinks with multpile strings """
    s = tag.string

    if s == None:
        ls = tag.find('a')
        return ls.string
    else:
        return s    
# END DEFINITIONS



# open html to parse
with open('wiki.html', 'r') as W:
    soup = BeautifulSoup(W.read())

# narrows field through css selectors to only page content
soup = soup.find(id='mw-content-text')
# further narow field by creating a list of all the h3s
# these correspond to 1.1, 1.2...1.17--i.e. the genres
genre_soup = soup.find_all('h3')

genealogy = []

for genre in genre_soup:
    # within h3 this span describes the big bold visible heading
    genre_name = genre.find_all('span', {'class':'mw-headline'})
    genre_name = get_string(genre_name[0])

    # find the grouping that describes all the sub-genres
    # i.e. the top level, the first group of <li>
    while True:
        genre = genre.next_sibling
        # can be held in next div if many or ul if few
        try:
            if genre.name == 'div':
                subgenres = genre.select('ul > li')
                subgenres = genre.find_all('li')
                break
            elif genre.name == 'ul':
                subgenres = genre.find_all('li')
                break
        # if next sibling is not a div or ul
        except AttributeError: pass

    # we now have the chunk of contents that corresponds to genre_name stored in subgenres
    # if genre_name == 'Electronic': # db
    for li in subgenres:
        li_name = get_string(li)
        # print 'Specific genre: ' + li_name

        # if li_name == 'Nu-disco': break

        while True:
            li = li.parent

            yyy = li.previous_sibling
            if yyy == '\n':
                zzz = yyy.previous_sibling

            if zzz != None:
                if zzz.name == 'a':
                    parent = get_string(zzz)
                else:
                    # print zzz
                    # <h3>
                        # <span class="editsection">
                            # [<a href="http://en.wikipedia.org/w/index.php?title=List_of_popular_music_genres&amp;action=edit&amp;section=7" title="Edit section: Country">edit</a>]
                        # </span> 
                        # <span class="mw-headline" id="Country">
                            # <a href="http://en.wikipedia.org/wiki/Country_music" title="Country music">Country</a>
                        # </span>
                    # </h3>

                    # at relative top level
                    parent = genre_name
                # print 'parent: ' + parent
                break
        uuu = (parent, li_name)
        # print uuu
        genealogy.append(uuu)
        # print '============' # db
    # elif genre_name == 'Electronica': break # db


with codecs.open('beta_out.txt', 'w', 'utf-8-sig') as z:
    z.write(str(genealogy))
