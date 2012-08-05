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

def create_gv():
    with codecs.open('out.gv', 'w', 'utf-8-sig') as X:
            X.write('graph testing {\n')
            X.write('     node [fontname=Gotham,shape=box]\n')

            for item in data:
                tmp = item.split('--')
                information = '"%s" -- "%s"' % (tmp[0].strip(), tmp[1].strip())

                pseudotab = '     '
                string = pseudotab + information + ';\n'
                X.write(string)

            X.write('}')    
# END DEFINITIONS



# open html to parse
with open('wiki.html', 'r') as W:
    soup = BeautifulSoup(W.read())

# narrows field through css selectors to only page content
soup = soup.find(id='mw-content-text')
# further narow field by creating a list of all the h3s
# these correspond to 1.1, 1.2...1.17--i.e. the genres
genre_soup = soup.find_all('h3')

for genre in genre_soup:
    # within h3 this span describes the big bold visible heading
    genre_name = genre.find_all('span', {'class':'mw-headline'})
    genre_name = genre_name[0].string

    # find the grouping that describes all the sub-genres
    # i.e. the top level, the first group of <li>
    while True:
        genre = genre.next_sibling
        # can be held in next div if many or ul if few
        try:
            if genre.name == 'div':
                subgenres = genre.select('ul > li')
                break
            elif genre.name == 'ul':
                subgenres = genre.select('li')
                break
        except AttributeError: pass

    # we now have the chunk of contents that corresponds to genre_name stored in subgenres
    # now comes the hard part