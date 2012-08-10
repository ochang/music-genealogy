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
    if genre_name == 'Country':
        for li in subgenres:
            li_name = get_string(li)
            print 'Node name:' + li_name
            if li_name == 'Bluegrass': break

            while True:
                li = li.parent
                # print get_string(li)

                yyy = li.previous_sibling
                if yyy == '\n':
                    zzz = yyy.previous_sibling

                if zzz != None:
                    print 'parent:'
                    if zzz.name == 'a':
                        print get_string(zzz)
                    else:
                        # we are already at top sublevel!
                        print genre_name
                    break

            print '============'
    elif genre_name == 'Easy listening':break


# with codecs.open('draft_out.txt', 'w', 'utf-8-sig') as z:
#     z.write(str(genealogy))
