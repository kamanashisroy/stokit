#!python

from portfolio import portfolio
from portfolio_chart import chart
import argparse

CURRENT = '.stock/CURRENT'
def select_portfolio(filename):
    '''
    Write the filename in .stock/current
    '''
    f = open(CURRENT, 'w')
    f.write(filename)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='STOKIT stock monitoring tool.')
    parser.add_argument('--action')

    subcommands = parser.add_subparsers(help='Sub-commands', dest='action')

    # port
    port_command_parser = subcommands.add_parser('port', help='Select portfolio file')
    port_command_parser.add_argument('portfile')
    #port_command_parser.add_argument('portfile', type=argparse.FileType('r'))

    # pull
    pull_command_parser = subcommands.add_parser('pull', help='pull history')
    pull_command_parser.add_argument('-y', help='full year')

    # show
    show_command_parser = subcommands.add_parser('show', help='show portfolio')
    show_command_parser.add_argument('--fillme', help='fillme')

    # status
    status_command_parser = subcommands.add_parser('status', help='Show loss/gain')
    status_command_parser.add_argument('--chart', help='Display charts pie or doughnut',choices=['pie','doughnut','bar','polar'], nargs='+')
    
    # compare
    compare_command_parser = subcommands.add_parser('compare', help='Compare loss/gain')
    compare_command_parser.add_argument('--chart', help='Display charts',choices=['table','candlestick'])

    # quote
    symbol_command_parser = subcommands.add_parser('quote', help='Show company quote')
    symbol_command_parser.add_argument('symbol', help='Company symbol')
    symbol_command_parser.add_argument('--local', help='Show cached information', default=False, action='store_const', const=True)

    args = parser.parse_args()
    print(args)

    if args.action == 'port':
        select_portfolio(args.portfile)
    
    port = './portfolio.csv'
    try:
        with open(CURRENT, 'r') as curfp:
            port = curfp.read()
    except:
        print("current portfolio is not set")

    tool = portfolio(port)
    tool_chart = chart(tool)

    #if 'port' == args.action and 'portfile' not in args.keys():
    #    tool.show()

    if 'show' == args.action:
        tool.show()

    if 'status' == args.action:
        if args.chart:
            tool_chart.status(args.chart)
        else:
            tool.status()

    if 'pull' == args.action:
        tool.pull()

    if 'compare' == args.action:
        if args.chart:
            tool_chart.compare(args.chart)
        else:
            tool.compare()

    if 'quote' == args.action:
        tool_chart.quote(args.symbol, args.local)
