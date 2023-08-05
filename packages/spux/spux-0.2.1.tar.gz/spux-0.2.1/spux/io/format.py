# # # # # # # # # # # # # # # # # # # # # # # # # #
# Formatting routines
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

def compactify (resources):

    compact = ''
    for resource in resources:
        compact += '/' + resource ['owner'] + ('-' + str(resource ['address']) if resource ['address'] is not None else '')
    return compact if compact != '' else '/'
