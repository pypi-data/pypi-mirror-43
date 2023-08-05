r'''
Usage:
    detk-filter [options] <command> <counts_fn> [<cov_fn>]

Options:
    -o <out_fn> --output=<out_fn>    Name of output file [default: stdout]
    --column-data=<column_data_fn>   DEPRECATED: pass cov_fn as positional
                                     command line argument instead
'''

import csv
from docopt import docopt
import numpy as np
import pandas as pd
import os.path
import ply.lex as lex
import ply.yacc as yacc
import sys
from tempfile import TemporaryDirectory
from warnings import warn

from .common import CountMatrixFile, DetkModule, _cli_doc
from .report import DetkReport

#Available tokens for mini language
reserved = ('ALL','OR','AND','MEDIAN','MEAN','ZERO','NONZERO','MAX','MIN')
tokens = ('LPAREN','RPAREN','LBRACKET','RBRACKET',
          'OP','WORD','NUMBER'
         ) + reserved
reserved = dict((_,)*2 for _ in reserved)

#Definitions of the mini language tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_OP = r'>=|<=|==|!=|<|>'
t_NUMBER = r'-?[0-9]+([.][0-9]+)?'

# http://www.dabeaz.com/ply/ply.html#ply_nn6
def t_WORD(t) :
    r'[a-zA-Z_.][a-zA-Z0-9_.]+'
    t.type = reserved.get(t.value.upper(),'WORD')
    return t

#Mini language ignores spaces, tabs, brackets, and parentheses
t_ignore = ' '

#Prints an error message if there's an invalid token
def t_error(t):
    raise Exception('Illegal character {}'.format(t.value[0]))

# mini language is like:
#
# expression : spec OP NUMBER
#            | expression OR expression
#            | expression AND expression
#            | LPAREN expression RPAREN
# spec       : FUNC LPAREN ALL RPAREN
#            | FUNC LPAREN word RPAREN
#            | FUNC LPAREN word LBRACKET word RBRACKET RPAREN
class Expr(object) : pass
class And(Expr) :
    def __init__(self,a,b) :
        self.a = a
        self.b = b
    def __call__(self,mat) :
        # inner join
        return self.a(mat).intersection(self.b(mat))
    def __repr__(self) :
        return 'And({},{})'.format(
                repr(self.a),
                repr(self.b)
            )

class Or(Expr) :
    def __init__(self,a,b) :
        self.a = a
        self.b = b
    def __call__(self,mat) :
        # outer join
        return self.a(mat).union(self.b(mat))
    def __repr__(self) :
        return 'Or({},{})'.format(
                repr(self.a),
                repr(self.b)
            )

class Group(Expr) :
    def __init__(self,member) :
        self.member = member
    def __call__(self,mat) :
        return self.member(mat)
    def __repr__(self) :
        return 'Group({})'.format(repr(self.member))

class Clause(Expr) :
    def __init__(self,func,spec,op,val) :
        self.func = func.lower()
        self.spec = spec
        self.op = op
        self.val = float(val)
    def __call__(self,mat) :
        dfs = self.spec(mat)
        idx = set()
        for df in dfs :

            # aggregate
            if self.func == 'median' :
                val = df.median(axis=1)
            elif self.func == 'mean' :
                val = df.mean(axis=1)
            elif self.func == 'min' :
                val = df.min(axis=1)
            elif self.func == 'max' :
                val = df.max(axis=1)
            elif self.func == 'zero' :
                val = (df==0).sum(axis=1)
                if 0 < self.val < 1 :
                    val /= df.shape[1]
            elif self.func == 'nonzero' :
                val = (df!=0).sum(axis=1)
                if 0 < self.val < 1 :
                    val /= df.shape[1]

            # compare
            if self.op == '>=' :
                idx.update(set(val[val>=self.val].index))
            elif self.op == '>' :
                idx.update(set(val[val>self.val].index))
            elif self.op == '<=' :
                idx.update(set(val[val<=self.val].index))
            elif self.op == '<' :
                idx.update(set(val[val<self.val].index))
            elif self.op == '==' :
                idx.update(set(val[val==self.val].index))
            elif self.op == '!=' :
                idx.update(set(val[val!=self.val].index))

        return idx
    def __repr__(self) :
        return 'Clause({},{},{},{})'.format(
                repr(self.func),
                repr(self.spec),
                repr(self.op),
                repr(self.val)
            )

class ColSpec(Expr) :
    def __init__(self,field=None,group=None) :
        self.field = field
        self.group = group
    def __call__(self,mat) :
        # return a list of dataframes containing the column subsets that the
        # Clause will use to filter
        if self.field is None and self.group is None :
            # no column filters
            return [mat.counts]
        elif self.field is not None :
            if mat.column_data is None :
                raise Exception('Field specified, but no column data supplied, '
                        'include a column data file with this call to filter '
                        'using field and group value')
            if self.group is not None :
                # only one group is selected, return just that subset
                # of rows for the given column
                # throw a warning if the group is not found in the column, as
                # this is probably not intended
                cols = mat.column_data.index[mat.column_data[self.field]==self.group]
                if cols.size == 0 :
                    warn(('Specified group value {}=="{}" was not found in '
                          'column values ({}). This is probably not what you '
                          'want to do, give that filter command a good look.').format(
                                self.field,
                                self.group,
                                mat.column_data[self.field].unique()
                                )
                            )
                return [mat.counts[cols]]
            else :
                # return a list of dataframe slices, one per
                # group
                dfs = []
                for v,df in mat.column_data.groupby(self.field) :
                    dfs.append(mat.counts[df.index])
                return dfs
    def __repr__(self) :
        return 'ColSpec(field={},group={})'.format(
                    repr(self.field),
                    repr(self.group)
                )


def p_expression(p) :
    '''expression : clause
                  | expression OR expression
                  | expression AND expression
                  | LPAREN expression RPAREN'''
    if len(p) == 2 :
        p[0] = p[1]
    else :
        if issubclass(p[2].__class__,Expr) :
            p[0] = Group(p[2])
        elif p[2].lower() == 'and' :
            p[0] = And(p[1],p[3])
        elif p[2].lower() == 'or' :
            p[0] = Or(p[1],p[3])
        else :
            raise Exception('unrecognized expression:',p)

def p_clause(p) :
    '''clause : func LPAREN colspec RPAREN OP NUMBER'''
    p[0] = Clause(p[1],p[3],p[5],p[6])

def p_func(p) :
    '''func : MEAN
            | MEDIAN
            | ZERO
            | NONZERO
            | MIN
            | MAX
        '''
    p[0] = p[1]

def p_spec(p) :
    '''colspec : ALL
               | WORD
               | WORD LBRACKET WORD RBRACKET'''
    if p[1].lower() == 'all' :
        obj = ColSpec()
    else :
        if len(p) == 5 :
            obj = ColSpec(p[1],p[3])
        else :
            obj = ColSpec(p[1])
    p[0] = obj

def p_error(p) :
    raise Exception(p)

def parse_filter_command(cmd) :

    # lex and yacc write out some files when they run
    # put them in a tempdir to keep things tidy
    with TemporaryDirectory() as tmpdir :

        lexer = lex.lex(outputdir=tmpdir)

        parser = yacc.yacc(outputdir=tmpdir)


    parsed = parser.parse(cmd)
    if parsed is None : # failed to parse
        raise Exception('Could not parse filter command, check syntax: {}'.format(cmd))

    return parsed

def filter_counts(counts_obj, command) :
    obj = FilterCounts(counts_obj,command)
    return obj.output

class FilterCounts(DetkModule) :
    def __init__(self, counts_obj, command) :
        self['params'] = {'command': command}
        parser = parse_filter_command(command)
        self.counts_obj = counts_obj
        self.kept = parser(counts_obj)
    @property
    def output(self):
        return self.counts_obj.counts.loc[self.counts_obj.counts.index.isin(self.kept)]
    @property
    def properties(self):
        return {
                'num_kept': len(self.kept),
                'num_filtered': self.counts_obj.counts.shape[0]-len(self.kept)
               }

def main(argv=sys.argv):

    if '--version' in argv :
        from .version import __version__
        print(__version__)
        return

    if argv[0].endswith('detk') :
        argv = argv[2:]
    elif argv[0].endswith('detk-filter') :
        argv = argv[1:]

    #Create command line arguments to pass in data and filter command
    args = docopt(_cli_doc(__doc__), argv=argv)

    #Create CountMatrixFile object from given data
    count_fn = args.get('<counts_fn>')

    #Get column data, if provided
    cov_fn = None
    if args['--column-data'] is not None :
        warn('The --column-data command line argument is deprecated. '
                'Use the optional [<cov_fn>] positional argument instead.'
            )
        cov_fn = args['--column-data']

    # cov_fn might have been initialized with --column-data before
    # only override the value if <cov_fn> was provided on the CLI
    cov_fn = args.get('<cov_fn>',cov_fn)

    counts_obj = CountMatrixFile(args['<counts_fn>'],column_data_f=cov_fn)

    filtered = FilterCounts(counts_obj, args['<command>'])

    outf = sys.stdout
    if args['--output'] != 'stdout' :
        outf = open(args['--output'],'wt')

    filtered.output.to_csv(outf)

    # write out the report json
    with DetkReport(args['--report-dir']) as r :
        r.add_module(
                filtered,
                in_file_path=args['<counts_fn>'],
                out_file_path=args['--output'],
                column_data_path=args.get('--column-data'),
                workdir=os.getcwd()
            )


if __name__ == '__main__':
    main()
