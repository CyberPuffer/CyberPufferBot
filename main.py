def main():
    from argparse import ArgumentParser
    from os import environ
    from utils.jobs import start_jobs
    parser = ArgumentParser(
        prog='CyberPuffer', description='CyberPuffer - Just yet another telegram bot')
    parser.add_argument('--secret', '-s', dest='api_secret')
    parser.add_argument('--config', '-c', dest='config_file')
    parser.add_argument('--proxy', '-x', dest='proxy')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()
    if args.verbose:
        environ["COLOREDLOGS_LOG_LEVEL"] = "DEBUG"
    args.api_list = []
    args.config_list = []
    if args.api_secret is not None:
        for item in args.api_secret.split(';'):
            args.api_list.append(item)
    if 'API_SECRET' in environ.keys():
        for item in environ['API_SECRET'].split(';'):
            args.api_list.append(item)
    if args.config_file is not None:
        args.config_list.append(args.config_file)
    if 'CONFIG_FILE' in environ.keys():
        args.config_list.append(environ['CONFIG_FILE'])
    if len(args.api_list) == 0:
        raise RuntimeError('Please provide at least one API')
    start_jobs(args)

if __name__ == "__main__":
    main()