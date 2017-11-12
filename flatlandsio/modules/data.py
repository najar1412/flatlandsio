software = {
    1: {
        'title': 'glance',
        'author': 'rory jarrel',
        'tags': ['library'],
        'summary': 'solution to the mangement and sharing of 1000s of 3d assets across multiple offices.',
        'tech': 'python, flask and aws.',
        'code': 'http://github.com/example',
        'goal': 'glance needed to able to serve visual assets including video, picture 3d geometry to various offices around the global for the production of visualisation renderings. The system needed to incorparate some machine learning to the tune of item detection in both stills and video.',
        'type': 'web'
    },
    2: {
        'title': 'gallery',
        'author': 'rory jarrel',
        'tags': ['photo'],
        'summary': 'personally managed cloud photo galleries.',
        'tech': 'python, flask, postgresql and aws',
        'code': 'http://github.com/example',
        'goal': 'This system is aimed at your everyday tourists. A simple system of managing hoilday snaps, that are simple to share with friends and family.',
        'type': 'web'
    },
    3: {
        'title': 'rorender',
        'author': 'rory jarrel',
        'tags': ['backburner', 'vray'],
        'summary': 'A cli tool to allow the user to quicky see which renders nodes are free and avalialbe for distrubuted rendering.',
        'tech': 'python, cli',
        'code': 'http://github.com/example',
        'goal': 'A cli interface to various render managers within a farm. Tool comes complete with features to enabled/disable different types of render software as well as checking current and recently finished rendering information',
        'type': 'desktop'
    },
    4: {
        'title': 'copy paste',
        'author': 'rory jarrel',
        'tags': ['3ds max', 'python', 'maxscript'],
        'summary': 'Copy and paste 3d assets',
        'tech': 'python, maxscript',
        'code': 'http://github.com/example',
        'goal': 'extending fucntionality of 3ds max with copy and paste between open 3ds max files.',
        'type': 'script'
    },
    5: {
        'title': 'auto comp',
        'author': 'rory jarrel',
        'tags': ['3ds max', 'vray', 'python', 'nuke'],
        'summary': 'quick basic composition of render passes',
        'tech': 'python, flask and aws.',
        'code': 'http://github.com/example',
        'goal': 'automates the compositing all standard vray passes, for quick visualisation within Nuke.',
        'type': 'script'
    },
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
    },
    3: {
        'title': 'follow me',
        'content': {
            1: {
                'title': 'social 01',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
            },
            2: {
                'title': 'social 02',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
            }
        }
    }
}
