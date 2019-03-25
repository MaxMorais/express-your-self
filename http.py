from expr import *

do([
    re := require('re'),

    for_each := lambda iterable, callback: consume(
        callback(entry) for entry in iterable
    ),

    Header := t('Header', ['name', 'value']),

    parse_header := lambda header: do([
        split_header := re.split(': ', header),
        Header(split_header[0], split_header[1])
    ]),

    Request := t('Request', [
        'method',
        'path',
        'headers',
    ]),

    parse := lambda message: do([
        lines := re.split('\r?\n', message),
        
        request_line := lines[0].split(' '),
        method := request_line[0],
        path := request_line[1],

        headers := [] if len(lines) == 1 else \
            [parse_header(header) for header in lines[1:]],

        Request(method, path, headers),
    ]),

    print(parse("""GET / HTTP/1.1\r\nAccept: *""")),
    print(parse("""GET / HTTP/1.1\nAccept: *""")),
    print(parse("""GET / HTTP/1.1
Host: localhost:3000
User-Agent: HTTPie/1.0.2
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive""")),

    export(__name__, parse)
])
