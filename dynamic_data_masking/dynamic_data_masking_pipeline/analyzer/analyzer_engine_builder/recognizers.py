RECOGNIZERS = {
    'en': {
        'deny_list': {
            "GREET": ["Hello"],
            "HERO": ["Captain America"]
        },
        'regex_list': {
            "NUMBERS": ["[0-9]{5}", "[0-9]{2}"],
            "EMAIL": [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]
        }
    },
    'fr': {
        'deny_list': {
            "SALUT": ["Bonjour"],
            "HEROS": ["Capitaine America"]
        },
        'regex_list': {
            "EMAIL": [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]
        }
    },
    'nl': {
        'deny_list': {
            "GROET": ["Hallo"],
            "HELD": ["Kapitein Amerika"]
        },
        'regex_list': {
            "EMAIL": [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]
        }
    }
}