#!/usr/bin/env python

from flipkart import get_act_url,get_details


if __name__ == '__main__':
	book = str(raw_input('Book Name:'))
	print '####### FLIPKART BOOK SEARCH RESULT #######'
	link = get_act_url(book)
	get_details(link)
