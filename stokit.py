#!python

from portfolio import portfolio
from portfolio_chart import chart
import pandas as pd
import argparse

CURRENT_PORT = '.stock/CURRENT_PORT'
#CURRENT_HOLDING = '.stock/CURRENT_HOLDING'

def update_current(current, filename):
    '''
    Write the filename in .stock/current_X
    '''
    f = open(current, 'w')
    f.write(filename)
    f.close()

def import_portfolio(filename):
    '''
    build a portfolio named filename+'_imported.csv'
    
    Currently we only support chase imported files

    TODO calculate footer

    '''

    outfile = filename+'_imported.csv'
    skiplines = []
    with open(filename, 'r') as src:
        for i,line in enumerate(src.readlines(),1):
            if 1 == i:
                continue # do not skip header
            if not line or not ('"' == line[0]):
                print('skipping',line[0], line)
                skiplines.append(i)
    print('skipping lines', skiplines)
    data = pd.read_csv(filename,quotechar='"',skiprows=skiplines)
    data = data[data['Ticker'] != 'QACDS']

    #data['TotalCost'] = data['Cost']*data['Quantity']
    #data.dropna(inplace=True)
    data.filter(items=['Ticker','Quantity','Cost']).groupby(['Ticker']).sum().to_csv(outfile,header=False,sep='|')
    update_current(CURRENT_PORT, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='STOKIT stock monitoring tool.')
    parser.add_argument('--action')

    subcommands = parser.add_subparsers(help='Sub-commands', dest='action')

    # port
    port_command_parser = subcommands.add_parser('port', help='Select portfolio file')
    port_command_parser.add_argument('portfile')
    #port_command_parser.add_argument('portfile', type=argparse.FileType('r'))

    # import
    import_command_parser = subcommands.add_parser('import', help='Import portfolio/Holdings file')
    import_command_parser.add_argument('holdingfile')
    import_command_parser.add_argument('--broker', help='File exported from broker', choices=['chase','yahoo'])
    #import_command_parser.add_argument('portfile', type=argparse.FileType('r'))

    # pull
    pull_command_parser = subcommands.add_parser('pull', help='pull history')
    pull_command_parser.add_argument('-y', help='full year')

    # show
    show_command_parser = subcommands.add_parser('show', help='show portfolio')
    #show_command_parser.add_argument('--fillme', help='fillme')

    # status
    status_command_parser = subcommands.add_parser('status', help='Show loss/gain')
    status_command_parser.add_argument('--chart', help='Display charts pie or doughnut',choices=['pie','doughnut','bar','polar','sigmabar', 'sigmapolar', 'costpolar'], nargs='+')
    
    # compare
    compare_command_parser = subcommands.add_parser('compare', help='Compare loss/gain')
    compare_command_parser.add_argument('--chart', help='Display charts',choices=['heat','table','polar','bar'], nargs='+')

    # quote
    quote_command_parser = subcommands.add_parser('quote', help='Show company quote')
    quote_command_parser.add_argument('symbol', help='Company symbol')
    quote_command_parser.add_argument('--local', help='Show cached information', default=False, action='store_const', const=True)

    # bullweek
    bullweek_command_parser = subcommands.add_parser('bullweek', help='Show company quote')
    bullweek_command_parser.add_argument('symbol', help='Company symbol')
    bullweek_command_parser.add_argument('--local', help='Show cached information', default=False, action='store_const', const=True)
    bullweek_command_parser.add_argument('--tm', help='Select time', default='3mo', choices=['3mo','1mo','1y'])

    args = parser.parse_args()
    print(args)

    if args.action == 'port':
        update_current(CURRENT_PORT,args.portfile)

    if args.action == 'import':
        import_portfolio(args.holdingfile)
    
    port = './portfolio.csv'
    try:
        with open(CURRENT_PORT, 'r') as curfp:
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

    if 'bullweek' == args.action:
        tool_chart.bullweek(args.symbol, args.local, args.tm)

