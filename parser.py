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


def findlists(soup_tag):
    """ finds if a list item as a BeautifulSoup Tag has any more unordered list items as children.

        - returns Tag lists with nested hierarchy of lists if they exist
    """   
    # [African, [Afrobeat, Apala, Benga,...]]
    # [Rock, [Alternative Rock, [Britpop, [Post-Britpop]]]]
    pass

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



data = []
with open('wiki.html', 'r') as W:
    page = W.read()
    soup = BeautifulSoup(page)

graph_title = soup.title.string
soup = soup.find(id='mw-content-text')

genre_soup = soup.find_all('h3')
# for toc genre...
for heading in genre_soup:
    resultset = heading.find_all('span', {'class':'mw-headline'})
    # ...get the name of the genre...
    genre = resultset[0].string

    # ...then find the next group of lists after the genre h3 tag...
    while True:
        try:
            heading = heading.next_sibling
        except AttributeError: break

        # ...then get the subgenres listed there...
        try:
            if heading.name == 'div':
                subgenres = heading.select('ul > li')
                break
            elif heading.name == 'ul':
                subgenres = heading.select('li')
                break
        except AttributeError: pass

    # ...then iterate through the subgenres to search for subheadings
    print genre
    print subgenres
    for y in subgenres:
        data.append(genre + ' -- ' + get_string(y))


create_gv()