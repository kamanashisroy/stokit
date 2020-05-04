#!python

from portfolio import portfolio
from portfolio_chart import chart
import argparse

def select_portfolio(filename):
    '''
    TODO write the filename in .stock/current
    '''
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='STOKIT stock monitoring tool.')
    parser.add_argument('--action')

    subcommands = parser.add_subparsers(help='Sub-commands', dest='action')

    # port
    port_command_parser = subcommands.add_parser('port', help='Select portfolio file')
    port_command_parser.add_argument('portfile', type=argparse.FileType('r'))
    port_command_parser.set_defaults(func=select_portfolio)

    # pull
    pull_command_parser = subcommands.add_parser('pull', help='pull history')
    pull_command_parser.add_argument('-y', help='full year')

    # show
    show_command_parser = subcommands.add_parser('show', help='show portfolio')
    show_command_parser.add_argument('--fillme', help='fillme')

    # status
    status_command_parser = subcommands.add_parser('status', help='Show loss/gain')
    status_command_parser.add_argument('--chart', help='Display charts pie or doughnut',choices=['pie','doughnut'])
    
    args = parser.parse_args()
    print(args)

    port = './portfolio.csv'
    tool = portfolio(port)
    tool_chart = chart(tool)
    if args.action == 'show':
        tool.show()
    if args.action == 'status':
        if args.chart:
            tool_chart.status(args.chart)
        else:
            tool.status()
    if args.action == 'pull':
        tool.pull()
