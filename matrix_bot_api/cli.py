def get_command(text):
    if text:
        args = text.split()
        if args[0][0] == '/':
            return dict(command=args[0][1:], args=" ".join(args[1:]))
    return None