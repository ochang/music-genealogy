# BEGIN IMPORTS
import os
import sys

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

    abs_base = get_string(soup_tag)
    mixins = ''
    conns = []
    
    while True:
        snake = abs_base + mixins

        print 'NEW LOOP CYCLE'
        print soup_tag

        new_tag = soup_tag.select('ul > li')
        # if there are no more lists
        if new_tag == []:
            conns.append(snake)
            print 'FINISHED CYCLE'
            print conns
            return conns
        else:
            for x in new_tag:
                statement = ' -- ' + get_string(soup_tag) + ' -- ' + get_string(x)
                print statement
                mixins += statement

        soup_tag = new_tag

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

    # ...then find the next div after the genre h3 tag...
    div_after = heading.find_next('div')
    # ...then get the subgenres listed there...
    subgenres = div_after.select('ul > li')

    # ...then iterate through the subgenres to search for subheadings
    for y in subgenres:
        data.append(genre + get_string(y))

        print '\n'
        print y
        z = findlists(y)
        
        for p in z:
            data.append(p)

print data
