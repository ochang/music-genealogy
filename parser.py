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

def gv_generate(t):
    tab = u'    '
    manual_head = (
        u'graph beta{\n',
        u'%spage="8.5,11";\n'%tab,
        u'%sratio=fill;\n'%tab,
        u'%sshape=box;\n'%tab,)
    manual_foot = u'}'

    

    for element in t:
        genre_name = element[0]
        genre_list = element[1]
        filename = 'z_' + genre_name + '_beta.gv'

        with codecs.open(filename, 'w', 'utf-8-sig') as p:
            for x in manual_head:
                p.write(x)

            for tup in genre_list:
                if tup[0] != tup[1]:
                    line = u'%s"%s" -- "%s";\n' % (tab, tup[0], tup[1])
                    p.write(line)

            p.write(manual_foot)

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
    genre_specific_list = []

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
    for li in subgenres:
        li_name = get_string(li)
        # print 'Specific genre: ' + li_name

        while True:
            # honestly, I do not know how this works
            li = li.parent
            yyy = li.previous_sibling

            if yyy == '\n':
                zzz = yyy.previous_sibling

            if zzz != None:
                if zzz.name == 'a':
                    parent = get_string(zzz)
                else:
                    # at h3, the name of the genre
                    parent = genre_name
                # print 'parent: ' + parent
                break
        uuu = (parent, li_name)


        genre_specific_list.append(uuu)

    genealogy.append((genre_name, genre_specific_list))
    # go to next genre

gv_generate(genealogy)

