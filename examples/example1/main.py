from py_makefile_dbparse.makefile import MakeFile


def main():
    mk1 = MakeFile('src')

    # Read in / parse the make database output
    mk1.read_db()
    mk1.dump_db('build/db_dump.txt')
    mk1.parse_vars()
    mk1.parse_targets()

    # Read the makefile text
    mktxt = mk1.launcher.read_makefile()

    # Results of the database output from make
    dbtxt = mk1.dbtxt
    vars1 = mk1.vars.values

    # Examples of expanding variables using the database extracted from make in memory
    test1_1 = mk1.vars.expand_var('OBJ')
    test1_2 = mk1.vars.expand_var(['OBJ', 'DEPS', 'CFLAGS'])
    test1_3 = mk1.vars.expand_expr('$(OBJ) teststring')
    test1_4 = mk1.vars.expand_expr(['$(OBJ) teststring', '$(DEPS) teststring2'])

    # Examples of expanding variables using make to output the results via an info target
    test2_1 = mk1.vars.expand_var('OBJ', usemake=True)
    test2_2 = mk1.vars.expand_var(['OBJ', 'DEPS', 'CFLAGS'], usemake=True)
    test2_3 = mk1.vars.expand_expr('$(OBJ) teststring', usemake=True)
    test2_4 = mk1.vars.expand_expr(['$(OBJ) teststring', '$(DEPS) teststring2'], usemake=True)

    # The first line won't be able to handle make functions, the second can but is slower
    test3_1 = mk1.vars.expand_expr('$(patsubst %,$(IDIR)/%,$(_DEPS))')
    test3_2 = mk1.vars.expand_expr('$(patsubst %,$(IDIR)/%,$(_DEPS))', usemake=True)

    # Targets
    tgts = mk1.targets
    test3_1 = tgts[0]
    test3_2 = tgts[0].target
    test3_3 = tgts[0].sources
    test3_4 = tgts[0].cmds_raw
    test3_5 = tgts[0].cmds_expand()
    test3_6 = tgts[0].cmds_expand(usemake=True)

    print("done")


if __name__ == '__main__':
    main()
