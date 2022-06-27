def child_content_query_result(pages: list, args: dict) -> list:
    if args['key'] != 'menu.link':
        return pages
    iterator = 0
    for key, page in pages:
        pages[iterator][1]['menu.separator'] = '&bull;'
        if iterator == len(pages) - 1:
            pages[iterator][1]['menu.separator'] = ''
        iterator += 1
    return pages
