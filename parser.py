# -*- coding: utf-8 -*-

"""
theoretically, this script can be used for any wikipedia list
which is laid out in the same manner

also, this would probably be a lot easier if it used the mediawiki api since
normal wikipedia pages are whack
"""

# BEGIN IMPORTS
from __future__ import unicode_literals
import os
import codecs
from subprocess import call

# import requests  # UNCOMMENT for web fetching
from bs4 import BeautifulSoup
# END IMPORTS


# BEGIN DEFINITIONS
def get_string(tag):
    """gets first string for hyperlinks with multpile strings
    """
    s = tag.string

    if s == None:
        ls = tag.find('a')
        return ls.string
    else:
        return s


def gv_generate(t):
    """given output of parser(), generates gv files using the template
    described in ugly detail below
    """
    manual_foot = '}'

    for element in t:
        genre_name = element[0]
        genre_list = element[1]
        filename = genre_name + '.gv'

        header = (
            'graph "' + genre_name + '" {\n',
            '\tpage="8.5,11";\n',
            '\tratio=fill;\n',
            '\toverlap=false;\n',
            '\t"' + genre_name + '"[shape=box];\n'
        )

        with codecs.open(filename, 'w', 'utf-8-sig') as p:
            for x in header:
                p.write(x)

            for tup in genre_list:
                if tup[0] != tup[1]:
                    line = '\t"%s" -- "%s";\n' % (tup[0], tup[1])
                    p.write(line)

            p.write(manual_foot)


def parser(soup):
    """
    parses hierarchy out of files like wiki.html
    theoreticaly any other wiki page of the same style as well

    returns a list of lists of direct parent-child rels stored in tuples for each genre
    """

    # narrows field through css selectors to only page content
    soup = soup.find(id='mw-content-text')
    # further narow field by creating a list of all the h3s
    # these correspond to 1.1, 1.2...1.17--i.e. the genres
    genre_soup = soup.find_all('h3')

    genealogy = []

    for genre in genre_soup:
        genre_specific_list = []

        # within h3 this span describes the big bold visible heading
        genre_name = genre.find_all('span', {'class': 'mw-headline'})
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
            except AttributeError:
                pass

        # we now have the chunk of contents that corresponds to genre_name stored in subgenres
        for li in subgenres:
            li_name = get_string(li)
            # print 'Specific genre: ' + li_name

            subgenre_data = None
            while True:
                # honestly, I do not know how this works

                # reassign li to it's parent node
                li = li.parent
                prev_sib = li.previous_sibling

                # if we still don't have actual content, go to next prev sib
                # keep iterating through loop until we get some data
                if prev_sib == '\n':
                    subgenre_data = prev_sib.previous_sibling

                if subgenre_data != None:
                    # different cases for long and short lists of subgenres
                    if subgenre_data.name == 'a':
                        parent = get_string(subgenre_data)
                    else:
                        # at h3, the name of the genre
                        parent = genre_name
                    # print 'parent: ' + parent
                    break

            subgenre_genealogy = (parent, li_name)
            # append all subgenres to a genre list
            # then go to the next subgenre
            genre_specific_list.append(subgenre_genealogy)

        # append all genre stuff to megalist
        # then go to the next genre
        genealogy.append((genre_name, genre_specific_list))

    return genealogy


def gen_png():
    """
    generates graphviz output by using command in CALL_ARGS
    """
    filelist = os.listdir('.')

    for gv in filelist:
        input_path = os.path.abspath(gv)
        output_path = os.path.splitext(gv)[0] + '.png'
        args = [
            'twopi', '-Gconcentrate=true', '-Tpng', input_path,
            '-o', output_path
        ]
        call(args)
# END DEFINITIONS


if __name__ == '__main__':
    # open html to parse
    with open('wiki.html', 'r') as W:
        soup = BeautifulSoup(W.read())

    # optionally, fetch page
    # remember to uncomment requests import at top
    # print "Wiki URL or [ENTER]Break"
    # print "Page better be formatted correctly!"
    # earl = raw_input('> ')
    # if earl == "":
    #     print "query blank; assuming bad things"
    #     raise SystemExit(0)
    # else:
    #     Page = requests.get(earl)
    #     soup = BeautifulSoup(Page.content)

    # parse
    genealogy = parser(soup)

    # save to gv files
    os.chdir(os.path.join(os.getcwd(), 'output'))
    gv_generate(genealogy)
    # generate png output
    gen_png()
