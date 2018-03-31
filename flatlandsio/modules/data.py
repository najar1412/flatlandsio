"""fake data"""

software = {
    1: {
        'title': 'devgear',
        'author': '',
        'tags': [],
        'summary': 'thd',
        'tech': [],
        'code': 'https://github.com/flatlands/devgear',
        'goal': 'tbd',
        'type': 'web',
        'screenshot': ['screenshot01.jpg']
    }
}

def get_software_by_tag():
    pass


def get_software_by_title(title):
    for code, data in software.items():
        if data['title'] == title:
            return data


def get_software_types(software):
    types = []
    for code, data in software.items():
        types.append(data['type'])

    return sorted(list(set(types)))


about = {
    1: {
        'title': 'what is flatlands?',
        'content': {
            1: {
                'title': '',
                'content': "hello! I'm Rory a software developer from sunny England residing in New York. flatlands is considered a portfolio of open source projects as well as a collection of articles that are either original content or shamelessly stolen from others (credited were applicable) and condensed for quick reference. any and all stolen content are from genuine code heroes. i appreciate and learn from them every day."
            },
            2: {
                'title': '',
                'content': "as technical director in the field of architecture visualisation. my day-to-day consists of building out our studios pipeline, hacking on proprietary software and developing tooling for our visualisation artists to producing stunning renderings."
            }
        }
    },
    2: {
        'title': 'faq',
        'content': {
            1: {
                'title': 'can i use the software on your site?',
                'content': "all software on Flatlands is complete with a licence file, that are mainly under the MIT umbrella unless otherwise stated."
            },
            2: {
                'title': 'where do you host your sites?',
                'content': "i predominately use digitalocean for most of my hosting with some aws sprinkled in here and there."
            },
            3: {
                'title': 'whats the best way to contact you for possible work?',
                'content': "my plate is pretty full currently, but room can always be made for interesting projects. the best place to enquire would be hello@flatlands.io"
            },
        }
    }
}
