===========
Spark Safe Delta
===========

Tool that allows to automatically update schema of DataBricks Delta in case of Changes in data structure

    #!/usr/bin/env python

	from sparksafedelta import sparksafedelta
	sparksafedelta.delta_write_safe(sp_df_to_write, SP_CONTEXT, DATABRICKS_TABLE_NAME)

(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


A Section
=========

Lists look like this:

* First

* Second. Can be multiple lines
  but must be indented properly.

A Sub-Section
-------------

Numbered lists look like you'd expect:

1. hi there

2. must be going

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.